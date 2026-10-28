#!/usr/bin/env python3
"""Auditoria offline de MDR/fixed fee versus condições explicitamente aprovadas."""
import argparse
import csv
import json
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

def D(v):
    if v is None or isinstance(v,bool) or (isinstance(v,str) and not v.strip()):return None
    try:
        d=Decimal(str(v));return d if d.is_finite() else None
    except (TypeError, ValueError, InvalidOperation):return None

def iso(v):
    try: return date.fromisoformat(str(v))
    except (ValueError,TypeError):return None

def compatible(r,t):
    if r.get('approved_by_user') is not True:return False
    d=iso(t.get('occurred_at'));s=iso(r.get('effective_from'));e=iso(r.get('effective_to'))
    if not d or not s or not e or s>d or e<d:return False
    for f in ('currency','channel','modality','installments','provider','brand'):
        val=r.get(f)
        if val is None or val=='':
            if f in ('currency','channel','modality','installments') or (f in ('provider','brand') and t.get(f)):return False
            continue
        if f in ('provider','brand') and val=='*':continue
        if str(val)!=str(t.get(f)):return False
    return True

def analyse_one(t, rates, duplicated):
    tid=str(t.get('id') or t.get('transaction_id') or '?');src=str(t.get('source') or tid)
    base={'transaction_id':tid,'source_locations':[src],'contract_source':None,'expected_mdr':None,'charged_mdr':str(t.get('charged_mdr')) if t.get('charged_mdr') is not None else None,'difference':None,'gaps':[], 'components':{},'external_provider_checked':False,'confirmed_refund_right':False}
    def ret(state,reason):base['state']=state;base['gaps'].append(reason);return base
    if duplicated:return ret('unverifiable_duplicate_record','Mesmo identificador transacional apareceu mais de uma vez; revisar exportações')
    if D(t.get('gross')) is None or D(t.get('gross'))<0 or not iso(t.get('occurred_at')):return ret('unverifiable','Valor bruto ou data de movimento inválidos')
    if D(t.get('charged_mdr')) is None:return ret('unverifiable','Componente MDR não identificado; líquido não basta')
    matches=[r for r in rates if compatible(r,t)]
    if not matches:return ret('unverifiable','Não há condição contratual aprovada com vigência, moeda e modalidade compatíveis')
    defs={(str(r.get('mdr_percent')),str(r.get('fixed_fee')),str(r.get('rounding_rule')),str(r.get('contract_id')),str(r.get('version'))) for r in matches}
    if len(matches)>1 and len(defs)>1:return ret('unverifiable_conflicting_contract','Duas ou mais condições compatíveis conflitantes; esclarecer vigência/contrato')
    r=matches[0];base['contract_source']=str(r.get('source') or r.get('contract_id') or 'contrato sem origem')
    base['source_locations'].append(base['contract_source'])
    pct=D(r.get('mdr_percent'));fixed=D(r.get('fixed_fee'))
    if pct is None or pct<0 or fixed is None or fixed<0 or r.get('rounding_rule')!='HALF_UP':return ret('unverifiable','MDR, tarifa fixa ou arredondamento contratual não confirmado')
    expected=(D(t['gross'])*pct/Decimal('100')).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
    charged=D(t.get('charged_mdr'));delta=charged-expected
    base['expected_mdr']=str(expected);base['difference']=str(delta.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))
    base['components']={'gross':str(D(t.get('gross'))),'currency':t.get('currency'),'mdr_percent':str(pct),'expected_mdr':str(expected),'charged_mdr':str(charged),'fixed_fee_contract':str(fixed),'rounding_rule':'HALF_UP','formula':'quantize(gross * mdr_percent / 100, 0.01, HALF_UP)'}
    if fixed!=0 and D(t.get('charged_fixed')) is None:
        return ret('unverifiable','Tarifa fixa contratual sem lançamento separável para comparação')
    if D(t.get('charged_fixed')) is not None:
        base['components']['charged_fixed']=str(D(t.get('charged_fixed')))
        if D(t.get('charged_fixed'))!=fixed:
            base['state']='discrepancy_candidate'
            base['gaps'].append('Tarifa fixa lançada difere do contrato aprovado')
            return base
    # Quando MDR é diferente, manter divergência mesmo se houver outras componentes não validadas.
    if delta!=0:
        base['state']='discrepancy_candidate';base['gaps'].append('Possível divergência no componente MDR; confirmar a base contratual e a natureza do lançamento');return base
    if D(t.get('charged_anticipation')) not in (None,Decimal('0')):
        return ret('mdr_consistent_anticipation_unverifiable','MDR consistente; regra de antecipação não fornecida')
    if D(t.get('chargeback')) not in (None,Decimal('0')):
        return ret('consistent_mdr_separate_chargeback','MDR consistente; chargeback identificado como componente separado')
    base['state']='consistent_with_confirmed_contract';return base

def investigate(data):
    rates=data.get('rates',[]);transactions=data.get('transactions',[])
    if not isinstance(rates,list) or not isinstance(transactions,list) or any(not isinstance(x,dict) for x in rates+transactions):raise ValueError('rates e transactions devem ser arrays de objetos')
    ids=[str(t.get('id') or t.get('transaction_id') or '') for t in transactions]
    dupes={id for id,count in Counter(ids).items() if id and count>1}
    items=[analyse_one(t,rates,str(t.get('id') or t.get('transaction_id') or '') in dupes) for t in transactions]
    if items and len({x['state'] for x in items})==1:state=items[0]['state']
    elif not items:state='unverifiable'
    elif any(x['state'].startswith('unverifiable') for x in items):state='requires_review'
    elif any(x['state']=='discrepancy_candidate' for x in items):state='review_candidates'
    else:state='all_consistent_or_component_gaps'
    return {'state':state,'items':items,'source_locations':sorted({src for x in items for src in x['source_locations']}),'external_provider_checked':False,'confirmed_refund_right':False,'note':'A comparação se limita aos componentes e contratos enviados; não comprova cobrança ilegal, erro do adquirente ou direito de restituição.'}

def read(path):
    p=Path(path)
    if p.suffix.lower()=='.csv':
        with p.open(encoding='utf-8-sig',newline='') as f:
            v=list(csv.DictReader(f))
        for x in v:
            if 'approved_by_user' in x:x['approved_by_user']=x['approved_by_user'].strip().lower()=='true'
        return v
    v=json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(v,list):raise ValueError('Entrada precisa ser lista de registros')
    return v

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',help='JSON com rates e transactions')
    p.add_argument('--rates',help='Contratos JSON/CSV aprovados')
    p.add_argument('--transactions',help='Lançamentos JSON/CSV')
    p.add_argument('--out',required=True)
    a=p.parse_args()
    if not a.input and not(a.rates and a.transactions):p.error('Use --input ou --rates e --transactions')
    d=json.loads(Path(a.input).read_text(encoding='utf-8')) if a.input else {'rates':read(a.rates),'transactions':read(a.transactions)}
    result=investigate(d)
    out=Path(a.out)
    for f in (a.input,a.rates,a.transactions):
        if f and out.resolve()==Path(f).resolve():p.error('Saída não pode sobrescrever entrada')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    lines=['# Auditoria de tarifas — evidências locais','',f"**Estado geral:** {result['state']}",'','Nenhuma conta foi consultada. Comparação contratual não comprova cobrança indevida.','','## Movimentos']
    for x in result['items']:
        lines.append(f"- {x['transaction_id']}: {x['state']}; MDR esperado {x['expected_mdr']}; observado {x['charged_mdr']}; diferença {x['difference']}; fontes {', '.join(x['source_locations'])}")
        lines.extend('  - '+g for g in x['gaps'])
    out.with_suffix('.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'state':result['state'],'json':str(out),'markdown':str(out.with_suffix('.md'))},ensure_ascii=False))
if __name__=='__main__':main()

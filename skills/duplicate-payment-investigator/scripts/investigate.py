#!/usr/bin/env python3
"""Investiga potencial duplicação da mesma obrigação, offline e sem realizar pagamentos."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def dec(v):
    try:
        d=Decimal(str(v));return d if d.is_finite() else None
    except (TypeError,InvalidOperation,ValueError):return None

def read(path):
    p=Path(path)
    if p.suffix.lower()=='.csv':
        with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
    v=json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(v,list):raise ValueError(f'{p.name}: esperado array de registros')
    return v

def source(x, default):return str(x.get('source') or x.get('source_location') or default)

def investigate(data):
    obligations=data.get('obligations',[]); payments=data.get('payments',[]); refunds=data.get('refunds',[])
    if any(not isinstance(x,list) for x in (obligations,payments,refunds)) or any(not isinstance(x,dict) for x in obligations+payments+refunds):
        raise ValueError('obligations, payments e refunds devem ser arrays de objetos')
    o_by_ref={str(o.get('reference')):o for o in obligations if o.get('reference')}
    group={}; excluded=[]; unresolved=[]; candidates=[]; problems=[]; all_sources=[]
    for n,p in enumerate(payments):
        all_sources.append(source(p,f'payments:{n+1}'))
        ref=str(p.get('obligation_ref') or '')
        if not ref or ref not in o_by_ref:
            unresolved.append({'why':'obligation_missing','payment':p.get('payment_id'),'source':source(p,f'payments:{n+1}')});continue
        group.setdefault(ref,[]).append(p)
    refunds_by_payment={}
    for r in refunds:
        if r.get('status')=='settled':refunds_by_payment.setdefault(str(r.get('payment_id')),[]).append(r)
    saw_refund=False
    for ref,rows in group.items():
        o=o_by_ref[ref];amount=dec(o.get('amount'));curr=o.get('currency');creditor=o.get('creditor_id');src=source(o,f'obligation:{ref}')
        all_sources.append(src)
        # Identificador de transação não é identificador da obrigação. Estágios da mesma transação se consolidam.
        unique={}; colliding=False
        for i,p in enumerate(rows):
            pid=str(p.get('end_to_end_id') or p.get('payment_id') or '')
            if not pid:
                unresolved.append({'why':'transaction_id_missing','reference':ref,'source':source(p,f'payment:{i+1}')}); continue
            if pid in unique:
                prev=unique[pid]
                if any(str(prev.get(k))!=str(p.get(k)) for k in ('amount','currency','payee_id','obligation_ref')):
                    colliding=True
                    unresolved.append({'why':'same_bank_id_conflicting_details','reference':ref,'source':source(p,'payment')})
                elif p.get('status')=='settled' and prev.get('status')!='settled':unique[pid]=p
                else:excluded.append({'why':'same_transaction_reexported','reference':ref,'source':source(p,'payment')})
            else:unique[pid]=p
        distinct=list(unique.values())
        inconsistent=colliding or amount is None or not curr or not creditor
        for p in distinct:
            if dec(p.get('amount')) is None or p.get('currency')!=curr or p.get('payee_id')!=creditor:
                inconsistent=True
        if inconsistent:
            unresolved.append({'why':'identity_amount_or_currency_conflict','reference':ref,'sources':[src]+[source(p,'payment') for p in distinct]});continue
        settled=[p for p in distinct if p.get('status')=='settled']
        uncertain=[p for p in distinct if p.get('status') not in ('settled','failed','cancelled','reversed')]
        if uncertain and len(distinct)>1:
            unresolved.append({'why':'settlement_unconfirmed','reference':ref,'sources':[source(p,'payment') for p in uncertain]});continue
        if len(settled)<2:
            excluded.append({'why':'fewer_than_two_independent_settled_transactions','reference':ref,'sources':[source(p,'payment') for p in distinct]}); continue
        fully_refunded=any(
            any(
                (dec(r.get('amount')) is not None and dec(r.get('amount')) >= dec(p.get('amount'))
                 and (not r.get('currency') or r.get('currency')==p.get('currency')))
                for r in refunds_by_payment.get(str(p.get('payment_id')),[])
            ) for p in settled
        )
        if fully_refunded:
            saw_refund=True
            excluded.append({'why':'one_transaction_refunded','reference':ref,'sources':[source(p,'payment') for p in settled]});continue
        total=sum((dec(p.get('amount')) for p in settled),Decimal('0'))
        # Duas parcelas que juntas quitam o título não são duplicidade.
        if total<=amount:
            excluded.append({'why':'total_fits_obligation_or_legitimate_installments','reference':ref,'paid_total':str(total),'obligation_amount':str(amount),'sources':[source(p,'payment') for p in settled]});continue
        if any(p.get('status')!='settled' for p in distinct):
            unresolved.append({'why':'mixed_statuses','reference':ref});continue
        candidates.append({'reference':ref,'reason':'total de duas ou mais transações liquidadas excede o valor da mesma obrigação','obligation_amount':str(amount),'settled_total':str(total),'currency':curr,'payment_ids':[str(p.get('payment_id')) for p in settled], 'sources':[src]+[source(p,'payment') for p in settled]})
    if candidates:state='review_candidate'
    elif unresolved:state='insufficient_evidence'
    elif saw_refund:state='no_active_duplicate_with_refund_flag'
    else:state='no_duplicate_evidence'
    if not obligations or not payments:
        state='insufficient_evidence'
        problems.append('Obrigações e/ou pagamentos ausentes')
    return {'state':state,'candidates':candidates,'excluded':excluded,'unresolved':unresolved,'gaps':problems, 'source_locations':sorted(set(all_sources+[source(r,'refund') for r in refunds])), 'verification_questions':['Confirmar em extrato bancário independente que cada identificador corresponde a débito liquidado','Confirmar com o credor a mesma obrigação e eventual estorno antes de qualquer solicitação de devolução'] if state in ('review_candidate','insufficient_evidence') else [],'confirmed_duplicate_payment':False,'note':'Candidatura para revisão; não prova erro bancário ou direito a restituição. Nenhum banco foi consultado.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',help='JSON contendo obligations, payments e refunds')
    p.add_argument('--payments',help='CSV/JSON de pagamentos')
    p.add_argument('--obligations',help='CSV/JSON de obrigações')
    p.add_argument('--refunds',help='CSV/JSON de estornos')
    p.add_argument('--out',required=True)
    a=p.parse_args()
    if not a.input and not (a.payments and a.obligations):p.error('Use --input ou --payments e --obligations')
    d=json.loads(Path(a.input).read_text(encoding='utf-8')) if a.input else {'payments':read(a.payments),'obligations':read(a.obligations),'refunds':read(a.refunds) if a.refunds else []}
    result=investigate(d)
    out=Path(a.out)
    for f in [a.input,a.payments,a.obligations,a.refunds]:
        if f and out.resolve()==Path(f).resolve():p.error('Saída não pode sobrescrever entrada')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    lines=['# Pagamentos potencialmente repetidos','',f"**Estado:** {result['state']}",'','Nenhuma consulta a banco foi realizada. Candidatos não são duplicidades confirmadas.','','## Candidatos']
    lines.extend('- '+str(c['reference'])+': '+c['reason']+' ('+', '.join(c['sources'])+')' for c in result['candidates'])
    lines+=['','## Incertezas'];lines.extend('- '+u['why']+' '+str(u.get('reference','')) for u in result['unresolved'])
    lines+=['','## Verificações'];lines.extend('- '+q for q in result['verification_questions'])
    out.with_suffix('.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'state':result['state'],'json':str(out),'markdown':str(out.with_suffix('.md'))},ensure_ascii=False))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Correlacionador offline de evidências NF-e. Não consulta SEFAZ nem transmite documentos."""
import argparse
import csv
import json
from pathlib import Path

AUTH_CODES = {100, 150}

def load_rows(path):
    p = Path(path)
    if p.suffix.lower() == '.csv':
        with p.open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))
    if p.suffix.lower() == '.jsonl':
        return [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]
    data = json.loads(p.read_text(encoding='utf-8'))
    return data if isinstance(data, list) else data.get('events', [])

def ccode(x):
    try: return int(x)
    except (TypeError, ValueError): return None

def source_of(e, index):
    s = e.get('source') or e.get('source_location') or e.get('event_id') or e.get('id')
    return s if isinstance(s, str) else f'events:{index+1}'

def investigate(data):
    target = str(data.get('target') or data.get('key') or '').strip()
    env = data.get('target_env') or data.get('env')
    raw = data.get('events', [])
    if not isinstance(raw, list): raise ValueError('events deve ser uma lista')
    if not (target.isdigit() and len(target) == 44 and env in ('producao', 'homologacao')):
        return {'state':'indeterminate','reported_state':'indeterminate','subject':{'key':target,'environment':env},'basis':[],'timeline':[], 'source_locations':[], 'conflicts':[], 'gaps':['Chave de 44 dígitos ou ambiente indisponível/inválido'], 'safe_checks':['Confirmar chave e ambiente em fonte confiável; consultar chave externamente'], 'external_sefaz_checked':False}
    receipt_to_keys = {}
    for e in raw:
        if not isinstance(e, dict): continue
        if e.get('env') != env: continue
        rec = e.get('receipt') or e.get('receipt_id')
        if rec and e.get('key') and e.get('kind') in ('send','batch_send','lot_send'):
            receipt_to_keys.setdefault(str(rec),set()).add(str(e['key']))
    timeline=[]; relevant=[]; conflicts=[]; gaps=[]
    for i,e in enumerate(raw):
        if not isinstance(e, dict): continue
        if e.get('env') != env: continue
        rec = str(e.get('receipt') or e.get('receipt_id') or '')
        direct = e.get('key') == target
        linked = bool(rec and receipt_to_keys.get(rec) == {target})
        valid_doc = False
        if direct or linked:
            src=source_of(e,i)
            ev={'id':str(e.get('id') or e.get('event_id') or i+1), 'source':src,'kind':e.get('kind'),'timestamp':e.get('timestamp'),'cstat':ccode(e.get('cstat')),'receipt':rec or None,'protocol':e.get('protocol'),'key':e.get('key')}
            relevant.append((e, ev))
            timeline.append(ev)
        # Documentos internos apenas se a consulta do recibo estiver ligada inequivocamente à chave.
        if linked and ccode(e.get('cstat')) == 104:
            for j,doc in enumerate(e.get('docs') or []):
                if not isinstance(doc,dict) or doc.get('key') != target: continue
                d={'id':str(e.get('id') or i+1)+f'/doc{j+1}', 'source':source_of(e,i)+f'/docs/{j+1}', 'kind':'receipt_document','timestamp':e.get('timestamp'),'cstat':ccode(doc.get('cstat')),'receipt':rec,'protocol':doc.get('protocol'),'key':target}
                relevant.append((doc,d));timeline.append(d)
    reports=[]; protocols=set()
    for _,ev in relevant:
        if ev['cstat'] in AUTH_CODES and ev['protocol'] and ev['key']==target and ev['kind'] in ('key_query','receipt_document','send_result'):
            protocols.add(str(ev['protocol']))
            reports.append(ev)
    if len(protocols)>1: conflicts.append('Protocolos distintos reportados para a mesma chave e ambiente')
    if not relevant: gaps.append('Nenhum evento vinculado à chave/ambiente alvo')
    if not reports: gaps.append('Nenhum retorno individual de autorização com protocolo vinculável à chave')
    if any(ev['cstat']==204 for _,ev in relevant): gaps.append('Código 204 indica duplicidade, não autorização')
    if any(ev['cstat']==104 for _,ev in relevant) and not reports: gaps.append('104 informa processamento do lote, não resultado individual')
    if any(ev['cstat']==105 for _,ev in relevant): gaps.append('105 indica lote em processamento no registro fornecido')
    if len(protocols)>1: state='conflict'
    elif reports: state='reported_authorization'
    else: state='indeterminate'
    try: timeline.sort(key=lambda x:(str(x['timestamp'] or ''), str(x['source'])))
    except (TypeError,ValueError): pass
    return {'state':state,'reported_state':state,'subject':{'key':target,'environment':env},'basis':reports if reports else timeline,'timeline':timeline,'source_locations':sorted({x['source'] for x in timeline}),'conflicts':conflicts,'gaps':gaps,'safe_checks':['Conferir a situação na consulta por chave da SEFAZ competente no mesmo ambiente antes de decidir por reenvio'], 'external_sefaz_checked':False,'note':'Resultados refletem apenas eventos fornecidos, cuja autenticidade não foi verificada.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',help='JSON com target, target_env e events')
    p.add_argument('--events',help='Eventos JSONL/JSON/CSV (alternativa a --input)')
    p.add_argument('--target',help='Chave NF-e de 44 dígitos')
    p.add_argument('--env',default='producao',choices=['producao','homologacao'])
    p.add_argument('--out',required=True,help='JSON de saída; não sobrescreve input')
    args=p.parse_args()
    if not args.input and not args.events: p.error('Informe --input ou --events')
    data=json.loads(Path(args.input).read_text(encoding='utf-8')) if args.input else {'target':args.target,'target_env':args.env,'events':load_rows(args.events)}
    result=investigate(data)
    out=Path(args.out)
    if out.resolve()==Path(args.input or args.events).resolve():p.error('Output não pode sobrescrever input')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    out.with_suffix('.md').write_text('# Investigação NF-e (evidências locais)\n\n**Estado reportado:** '+result['state']+'\n\n**Atenção:** Não foi realizada consulta externa à SEFAZ.\n\n## Fontes\n'+''.join('- '+s+'\n' for s in result['source_locations'])+'\n## Lacunas\n'+''.join('- '+g+'\n' for g in result['gaps'])+'\n',encoding='utf-8')
    print(json.dumps({'state':result['state'],'json':str(out),'markdown':str(out.with_suffix('.md'))},ensure_ascii=False))
if __name__=='__main__':main()

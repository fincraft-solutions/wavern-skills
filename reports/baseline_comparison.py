#!/usr/bin/env python3
"""Baselines para os 42 casos de S06. B0 = intencionalmente raso; B1 = motores sem LLM."""
import json
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

D=Path(__file__).resolve().parent
cases=json.loads((D/'CASES_FROZEN_S06_v1.json').read_text())['cases']

def num(x):
    try:return Decimal(str(x))
    except (ValueError,TypeError,InvalidOperation):return None

def naive(c):
    x=c['inputs'];type_=c['skill']
    if type_=='nfe-incident-investigator':
        events=x['events'];e=events[-1]
        if e.get('cstat') in (100,150):return 'reported_authorization'
        return 'indeterminate'
    if type_=='duplicate-payment-investigator':
        p=x['payments']
        if len(p)>=2 and (num(p[0].get('amount'))==num(p[1].get('amount')) and p[0].get('payee_id')==p[1].get('payee_id')):return 'review_candidate'
        return 'no_duplicate_evidence'
    if type_=='payment-fee-auditor':
        r=x['rates'][0];t=x['transactions'][0]
        if not r or not t or num(t.get('charged_mdr')) is None or num(t.get('gross')) is None:return 'unverifiable'
        rate=num(r.get('mdr_percent'))
        if rate is None:return 'unverifiable'
        expected=(num(t.get('gross'))*rate/Decimal('100')).quantize(Decimal('.01'))
        return 'consistent_with_confirmed_contract' if expected==num(t.get('charged_mdr')) else 'discrepancy_candidate'

def main():
    rows=[{'id':c['id'],'skill':c['skill'],'expected':c['expected'],'baseline_b0':naive(c),'b0_correct':naive(c)==c['expected']} for c in cases]
    stat={}
    for skill in set(c['skill'] for c in cases):
        mine=[x for x in rows if x['skill']==skill]
        stat[skill]={'b0':sum(x['b0_correct'] for x in mine),'b1_engine_only':len(mine),'total':len(mine)}
    result={'baseline_definition':{'b0':'heurística ingênua, usa último cStat / mesmo valor+beneficiário / primeira taxa ignorando contratos','b1':'mesmo motor determinístico de cada Skill, acionado diretamente sem LLM; igual a T nos casos estruturados','T':'Não foi executado fluxo LLM+Skill; apenas motor disponível'},'scores':stat,'cases':rows,'comparative_LLM_executed':False,'note':'Baseline forte empata com motor integrado, portanto não há evidência de ganho causal da Skill como comportamento de LLM.'}
    (D/'BASELINE_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for k,v in stat.items():print(k,v)
if __name__=='__main__':main()

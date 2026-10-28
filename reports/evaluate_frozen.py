#!/usr/bin/env python3
"""Avalia exatamente os casos congelados da S06, sem modificá-los."""
import importlib.util
import json
import hashlib
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
CASES=HERE/'CASES_FROZEN_S06_v1.json'
EXPECTED_SHA='c5dfd03cd32c997dc37cae195a6ad9b19ef9bef00cb28664307879eefe8f85a9'
MAPPING={'nfe-incident-investigator':'NF','duplicate-payment-investigator':'DP','payment-fee-auditor':'FE'}

def load(name):
    src=ROOT/'skills'/name/'scripts'/'investigate.py'
    spec=importlib.util.spec_from_file_location(name.replace('-','_'),str(src));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def run():
    sha=hashlib.sha256(CASES.read_bytes()).hexdigest()
    if sha!=EXPECTED_SHA:raise RuntimeError('STOP: gabarito alterado '+sha)
    cases=json.loads(CASES.read_text(encoding='utf-8'))['cases']
    modules={name:load(name) for name in MAPPING}
    results=[]
    for c in cases:
        try:
            answer=modules[c['skill']].investigate(c['inputs']);actual=answer.get('state')
            err=None
        except Exception as ex:
            answer={};actual='EXCEPTION';err=f'{type(ex).__name__}: {ex}'
        results.append({'id':c['id'],'category':c['category'],'skill':c['skill'],'expected':c['expected'],'actual':actual,'pass':actual==c['expected'],'critical':c.get('critical'),'error':err,'evidence_sources':answer.get('source_locations',[]),'gaps':answer.get('gaps',[]),'note':'Deterministic engine only; no LLM invocation.'})
    overview={name:{'passed':sum(r['pass'] for r in results if r['skill']==name),'total':sum(r['skill']==name for r in results)} for name in MAPPING}
    summary={'frozen_sha256':sha,'score':sum(r['pass'] for r in results),'total':len(results),'critical_failures':[r['id'] for r in results if r['critical'] and not r['pass']],'per_skill':overview,'LLM_COMPARATIVE_NOT_EXECUTED':True,'cases':results}
    (HERE/'FROZEN_RESULTS.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    for r in results:
        print(f"{r['id']} {'PASS' if r['pass'] else 'FAIL'} expected={r['expected']} actual={r['actual']} {r['error'] or ''}")
    print(f"TOTAL {summary['score']}/{summary['total']} critical={summary['critical_failures']}")
    return summary
if __name__=='__main__':
    s=run();sys.exit(0 if s['score']==s['total'] else 1)

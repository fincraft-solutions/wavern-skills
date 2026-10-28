import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('feeengine',P/'scripts/investigate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
base=json.loads((P/'examples/fee-discrepancy.json').read_text())
def clone():return json.loads(json.dumps(base))

class FeeTest(unittest.TestCase):
    def check(self,inp,state):
        r=m.investigate(inp)
        self.assertEqual(r['state'],state);self.assertFalse(r['external_provider_checked']);self.assertFalse(r['confirmed_refund_right']);return r
    def test_discrepancy(self):
        r=self.check(clone(),'discrepancy_candidate')
        self.assertEqual(r['items'][0]['difference'],'4.00')
    def test_consistency(self):
        inp=clone();inp['transactions'][0]['charged_mdr']='25.00'
        self.check(inp,'consistent_with_confirmed_contract')
    def test_unapproved_contract(self):
        inp=clone();inp['rates'][0]['approved_by_user']=False
        self.check(inp,'unverifiable')
    def test_wrong_currency(self):
        inp=clone();inp['transactions'][0]['currency']='USD'
        self.check(inp,'unverifiable')
    def test_no_mdr_components(self):
        inp=clone();inp['transactions'][0].pop('charged_mdr');inp['transactions'][0]['net']='965.00'
        self.check(inp,'unverifiable')
    def test_expired_contract(self):
        inp=clone();inp['rates'][0]['effective_to']='2026-10-02'
        self.check(inp,'unverifiable')
    def test_fixed_fee_unexpected(self):
        inp=clone();inp['transactions'][0]['charged_mdr']='25.00';inp['transactions'][0]['charged_fixed']='2.00'
        self.check(inp,'discrepancy_candidate')
    def test_anticipation_separate(self):
        inp=clone();inp['transactions'][0]['charged_mdr']='25.00';inp['transactions'][0]['charged_anticipation']='11.00'
        self.check(inp,'mdr_consistent_anticipation_unverifiable')
    def test_chargeback_separate(self):
        inp=clone();inp['transactions'][0]['charged_mdr']='25.00';inp['transactions'][0]['chargeback']='50.00'
        self.check(inp,'consistent_mdr_separate_chargeback')
    def test_duplicate_export(self):
        inp=clone();inp['transactions'].append(inp['transactions'][0])
        self.check(inp,'unverifiable_duplicate_record')
    def test_conflicting_versions(self):
        inp=clone();other=dict(inp['rates'][0]);other['mdr_percent']='2.60';inp['rates'].append(other)
        self.check(inp,'unverifiable_conflicting_contract')
    def test_provider_not_wildcard(self):
        inp=clone();inp['transactions'][0]['provider']='EX'
        self.check(inp,'unverifiable')
    def test_cli(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'report.json'
            x=subprocess.run([sys.executable,str(P/'scripts/investigate.py'),'--input',str(P/'examples/fee-discrepancy.json'),'--out',str(out)],capture_output=True,text=True)
            self.assertEqual(x.returncode,0,x.stderr);self.assertEqual(json.loads(out.read_text())['state'],'discrepancy_candidate');self.assertTrue(out.with_suffix('.md').exists())
    def test_refuse_overwrite(self):
        inp=P/'examples/fee-discrepancy.json'
        x=subprocess.run([sys.executable,str(P/'scripts/investigate.py'),'--input',str(inp),'--out',str(inp)],capture_output=True,text=True)
        self.assertNotEqual(x.returncode,0)

if __name__=='__main__':unittest.main()

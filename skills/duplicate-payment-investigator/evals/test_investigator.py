import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('dpengine',P/'scripts/investigate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def pay(pid,ref='F1',status='settled',amount='100.00',currency='BRL',payee_id='P1'):
    return {'payment_id':pid,'end_to_end_id':pid,'obligation_ref':ref,'status':status,'amount':amount,'currency':currency,'payee_id':payee_id,'source':'payments:'+pid}

def data(payments):
    return {'obligations':[{'reference':'F1','amount':'100.00','currency':'BRL','creditor_id':'P1','source':'invoice:1'}],'payments':payments}

class DupTest(unittest.TestCase):
    def check(self,inp,state):
        r=m.investigate(inp);self.assertEqual(r['state'],state);self.assertFalse(r['confirmed_duplicate_payment']);return r
    def test_two_settled(self):
        x=self.check(data([pay('A'),pay('B')]),'review_candidate')
        self.assertIn('invoice:1',x['candidates'][0]['sources'])
    def test_duplicate_export(self):self.check(data([pay('A'),pay('A')]),'no_duplicate_evidence')
    def test_pending_then_settled_same_id(self):self.check(data([pay('A',status='pending'),pay('A')]),'no_duplicate_evidence')
    def test_two_months(self):
        x=data([pay('A'),pay('B',ref='F2')]);x['obligations'].append({'reference':'F2','amount':'100.00','currency':'BRL','creditor_id':'P1'})
        self.check(x,'no_duplicate_evidence')
    def test_receipt_only(self):self.check(data([pay('A'),pay('B',status='receipt_only')]),'insufficient_evidence')
    def test_beneficiary_conflict(self):self.check(data([pay('A'),pay('B',payee_id='P2')]),'insufficient_evidence')
    def test_cross_currency(self):self.check(data([pay('A'),pay('B',currency='USD')]),'insufficient_evidence')
    def test_installments(self):
        x=data([pay('A',amount='50.00'),pay('B',amount='50.00')]);x['obligations'][0]['installments']=2
        self.check(x,'no_duplicate_evidence')
    def test_refund(self):
        x=data([pay('A'),pay('B')]);x['refunds']=[{'payment_id':'B','status':'settled','amount':'100.00','source':'refunds:1'}]
        self.check(x,'no_active_duplicate_with_refund_flag')
    def test_partial_refund_remains_candidate(self):
        x=data([pay('A'),pay('B')]);x['refunds']=[{'payment_id':'B','status':'settled','amount':'1.00','source':'refunds:1'}]
        self.check(x,'review_candidate')
    def test_no_obligations(self):self.check({'obligations':[],'payments':[pay('A'),pay('B')]},'insufficient_evidence')
    def test_cli(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'test.json'
            x=subprocess.run([sys.executable,str(P/'scripts/investigate.py'),'--input',str(P/'examples/double-payment-candidate.json'),'--out',str(out)],capture_output=True,text=True)
            self.assertEqual(x.returncode,0,x.stderr)
            self.assertEqual(json.loads(out.read_text())['state'],'review_candidate');self.assertTrue(out.with_suffix('.md').exists())
    def test_refuse_overwrite(self):
        inp=P/'examples/double-payment-candidate.json'
        x=subprocess.run([sys.executable,str(P/'scripts/investigate.py'),'--input',str(inp),'--out',str(inp)],capture_output=True,text=True)
        self.assertNotEqual(x.returncode,0)

if __name__=='__main__':unittest.main()

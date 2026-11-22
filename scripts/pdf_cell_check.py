"""Every cell in the PDF vs values recomputed from raw (verification/pdf_gate_raw_counts.json, built by pdf_gate_raw.py)."""
import json,subprocess,re
from decimal import Decimal, ROUND_HALF_UP
PDF='/workspace/south-carolina-elections/pdf/South_Carolina_46_County_Democratic_Primary_Proxy_and_Vote_Change.pdf'
g=json.load(open('/workspace/south-carolina-elections/verification/pdf_gate_raw_counts.json'))
txt=subprocess.run(['pdftotext','-layout',PDF,'-'],capture_output=True,text=True).stdout
num=r'[+-]?[\d,]+(?:\.\d+)?%?'
rows={}; order=[]
for l in txt.splitlines():
    m=re.match(r'^\s*([A-Z][A-Za-z .]+?)\s{2,}('+num+r'(?:\s+'+num+r'){8})\s*$',l)
    if m: rows[m.group(1).strip()]=m.group(2).split(); order.append(m.group(1).strip())
def r1(x): return Decimal(x).quantize(Decimal('0.1'),rounding=ROUND_HALF_UP)
def share(d,r): return r1(Decimal(100*d)/Decimal(d+r))
def pct(a,b): return r1(Decimal(100*(b-a))/Decimal(a))
def P(s): return Decimal(s.replace(',','').replace('%','').replace('+',''))
def expect(x):
    return [share(x['pd_2026'],x['pr_2026']),x['dem_2022'],x['dem_2026'],x['dem_2026']-x['dem_2022'],pct(x['dem_2022'],x['dem_2026']),
            x['ballots_2022'],x['ballots_2026'],x['ballots_2026']-x['ballots_2022'],pct(x['ballots_2022'],x['ballots_2026'])]
tot={k:sum(v[k] for v in g.values()) for k in next(iter(g.values()))}
cols=['DemShare2026','DemVotes2022','DemVotes2026','VoteChg#','VoteChg%','Ballots2022','Ballots2026','BallotChg#','BallotChg%']
out=[]; checked=0; bad=[]
for c,x in list(g.items())+[('Statewide total',tot)]:
    if c not in rows: bad.append((c,'MISSING ROW')); continue
    for col,got,exp in zip(cols,rows[c],expect(x)):
        checked+=1; ok=P(got)==Decimal(exp)
        # sign check for changes
        if col.endswith('Chg#') or col.endswith('Chg%'):
            ok=ok and ((exp>0)==got.startswith('+'))
        if not ok: bad.append((c,col,got,str(exp)))
        out.append(f'{c}\t{col}\tPDF={got}\tRAW={exp}\t{"OK" if ok else "MISMATCH"}')
counties=[c for c in order if c!='Statewide total']
srt=sorted(g,key=lambda c:-g[c]['pd_2026']/(g[c]['pd_2026']+g[c]['pr_2026']))
checked+=46; sort_ok=counties==srt
hdr=f'Counties in PDF: {len(counties)} (expected 46); county cells checked incl. names/sort: {checked}; mismatches: {len(bad)}; sort order matches raw: {sort_ok}'
open('/workspace/south-carolina-elections/verification/pdf_cell_check.txt','w').write(hdr+'\n'+'\n'.join(out)+'\nMISMATCHES:\n'+'\n'.join(map(str,bad))+'\n')
print(hdr); print(bad[:10])

"""Compare pass A (state detail.xml, ElementTree) vs pass B (county sub-site files, csv/regex) figure by figure, plus
a third raw check: state status.json R (registered) and B (ballots) arrays for the general elections."""
import csv, json, gzip
V='/workspace/south-carolina-elections/verification/'; R='/workspace/south-carolina-elections/raw/'
A={r['county']:r for r in csv.DictReader(open(V+'passA_counties.csv'))}
B={r['county']:r for r in csv.DictReader(open(V+'passB_counties.csv'))}
assert set(A)==set(B) and len(A)==46
F=[k for k in next(iter(A.values())) if k!='county']
rows=[]; mm=[]
for c in sorted(A):
    for f in F:
        a,b=int(A[c][f]),int(B[c][f]); ok=a==b
        rows.append(dict(county=c,figure=f,passA=a,passB=b,match=ok))
        if not ok: mm.append(dict(county=c,figure=f,passA=a,passB=b,diff=a-b))
with open(V+'compare_A_B_figure_by_figure.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# status.json cross-check
st={}
for y in ('2022','2026'):
    b=open(R+y+'/json_status.json','rb').read()
    if b[:2]==b'\x1f\x8b': b=gzip.decompress(b)
    s=json.loads(b); d={p:(r,bb) for p,r,bb in zip(s['P'],s['R'],s['B'])}
    st[y]=dict(reg_mismatch_vs_A=[(c,d[c][0],int(A[c][f'reg_{y}'])) for c in A if d[c][0]!=int(A[c][f'reg_{y}'])],
               ballots_mismatch_vs_A=[(c,d[c][1],int(A[c][f'ballots_{y}'])) for c in A if d[c][1]!=int(A[c][f'ballots_{y}'])])
crit=[m for m in mm if not m['figure'].startswith(('reg_','prim_reg_'))]
rep=dict(counties=46,figures_per_county=len(F),total_comparisons=len(rows),matched=sum(r['match'] for r in rows),mismatched=len(mm),
         mismatches=mm,mismatches_in_analysis_figures=crit,status_json_check=st,CLEAN_analysis_figures=len(crit)==0)
json.dump(rep,open(V+'compare_report.json','w'),indent=1)
print(json.dumps({k:v for k,v in rep.items()},indent=0)[:4000])

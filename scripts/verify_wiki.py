"""Check every integer in the Reverse-Math full county table against PASS B (county-site files) and every
computed share against a recomputation from PASS B. Exit 1 on any mismatch."""
import csv,re,sys
W='/workspace/south-carolina-elections/'
B={r['county']:{k:int(v) for k,v in r.items() if k!='county'} for r in csv.DictReader(open(W+'verification/passB_counties.csv'))}
t=open(W+'wiki/Reverse-Math.md').read().split('## Full county table')[1]
rows=[l for l in t.splitlines() if l.startswith('| ') and not l.startswith('| County')]
n=0;bad=[]
num=lambda s:float(s.replace(',','').replace('−','-').replace('+',''))
for l in rows:
    c=[x.strip() for x in l.strip('|').split('|')]
    name=c[0].rstrip('†'); b=B[name]
    exp=[('prim_dem_2022',3),('prim_rep_2022',4),('dem_2022',6),('ballots_2022',7),('prim_dem_2026',10),('prim_rep_2026',11),('dem_2026',13),('ballots_2026',14)]
    for k,i in exp:
        n+=1
        if int(num(c[i]))!=b[k]: bad.append((name,k,c[i],b[k]))
    P22=100*b['prim_dem_2022']/(b['prim_dem_2022']+b['prim_rep_2022']); S22=100*b['dem_2022']/b['ballots_2022']
    P26=100*b['prim_dem_2026']/(b['prim_dem_2026']+b['prim_rep_2026']); S26=100*b['dem_2026']/b['ballots_2026']
    for v,i in ((P22,5),(S22,8),(S22-P22,9),(P26,12),(S26,15),(S26-P26,16),((S26-P26)-(S22-P22),17)):
        n+=1
        if abs(round(v,2)-num(c[i]))>0.0051: bad.append((name,i,c[i],v))
print(f'wiki table rows {len(rows)}, checks {n}, FAIL {len(bad)}'); [print(x) for x in bad]
sys.exit(1 if bad or len(rows)!=46 else 0)

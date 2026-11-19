"""Check every number in the Reverse-Math full county tables (2022 inputs, 2026 inputs, shares and ΔG) against PASS B
(county-site files): integers exactly, shares recomputed from Pass B to 2 decimals. Exit 1 on any mismatch."""
import csv,re,sys
W='/workspace/south-carolina-elections/'
B={r['county']:{k:int(v) for k,v in r.items() if k!='county'} for r in csv.DictReader(open(W+'verification/passB_counties.csv'))}
t=open(W+'wiki/Reverse-Math.md').read().split('## Full county table')[1]
secs=re.split(r'^### ',t,flags=re.M)[1:]
num=lambda s:float(s.replace(',','').replace('−','-').replace('+','').replace('\\*','').replace('%',''))
def rows(sec): return [[x.strip() for x in l.strip().strip('|').split('|')] for l in sec.splitlines() if l.startswith('| ') and not l.startswith('| County')]
n=0;bad=[];seen=[]
for sec in secs:
    title=sec.splitlines()[0]; R=rows(sec); seen.append((title,len(R)))
    for c in R:
        name=c[0].rstrip('†'); b=B[name]
        if title.startswith('2022'):
            spec=[(3,b['prim_dem_2022']),(4,b['prim_rep_2022']),(5,b['dem_2022']),(6,b['ballots_2022'])]
        elif title.startswith('2026'):
            spec=[(1,b['prim_dem_2026']),(2,b['prim_rep_2026']),(3,b['dem_2026']),(4,b['ballots_2026'])]
        else:
            P22=100*b['prim_dem_2022']/(b['prim_dem_2022']+b['prim_rep_2022']); S22=100*b['dem_2022']/b['ballots_2022']
            P26=100*b['prim_dem_2026']/(b['prim_dem_2026']+b['prim_rep_2026']); S26=100*b['dem_2026']/b['ballots_2026']
            spec=[(1,S22),(2,P22),(3,S22-P22),(4,S26),(5,P26),(6,S26-P26),(7,(S26-P26)-(S22-P22))]
        for i,v in spec:
            n+=1
            ok = int(num(c[i]))==v if isinstance(v,int) else abs(round(v,2)-num(c[i]))<=0.0051
            if not ok: bad.append((title,name,i,c[i],v))
print('tables',seen); print(f'checks {n}, FAIL {len(bad)}'); [print(x) for x in bad]
sys.exit(1 if bad or [r for _,r in seen]!=[46,46,46] else 0)

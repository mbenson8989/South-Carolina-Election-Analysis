"""PASS A: parse the STATE-level Clarity detail.xml (one file per election) with ElementTree.
Outputs verification/passA_counties.csv : one row per county, every figure used downstream."""
import zipfile, xml.etree.ElementTree as ET, csv, json
R='/workspace/south-carolina-elections/raw/'; V='/workspace/south-carolina-elections/verification/'
def root(d): return ET.fromstring(zipfile.ZipFile(R+d+'/reports_detailxml.zip').read('detail.xml'))
def turnout(rt):
    return {c.get('name'):(int(c.get('totalVoters')),int(c.get('ballotsCast'))) for c in rt.find('ElectionVoterTurnout').find('Counties')}
def contest(rt,text):
    cs=[c for c in rt.findall('Contest') if c.get('text').strip()==text]; assert len(cs)==1,text
    out={}
    for ch in cs[0].findall('Choice'):
        p=ch.get('party')
        for vt in ch.findall('VoteType'):
            for c in vt.findall('County'):
                out.setdefault(c.get('name'),{}).setdefault(p,0); out[c.get('name')][p]+=int(c.get('votes'))
    tot={}
    for ch in cs[0].findall('Choice'): tot[ch.get('party')]=tot.get(ch.get('party'),0)+int(ch.get('totalVotes'))
    return out, tot
rows={}; SW={}
for y in ('2022','2026'):
    rt=root(y); t=turnout(rt); g,sw=contest(rt,'Governor and Lieutenant Governor'); SW[y]=dict(gov=sw,ballots=int(rt.find('ElectionVoterTurnout').get('ballotsCast')),reg=int(rt.find('ElectionVoterTurnout').get('totalVoters')),timestamp=rt.findtext('Timestamp'))
    for c,(reg,bal) in t.items():
        r=rows.setdefault(c,{'county':c}); v=g[c]
        r[f'reg_{y}']=reg; r[f'ballots_{y}']=bal; r[f'dem_{y}']=v.get('DEM',0); r[f'rep_{y}']=v.get('REP',0)
        r[f'other_{y}']=sum(n for p,n in v.items() if p not in ('DEM','REP')); r[f'govtotal_{y}']=sum(v.values())
    rp=root(y+'_primary'); tp=turnout(rp); d,swd=contest(rp,'Governor - DEM'); rr,swr=contest(rp,'Governor - REP')
    SW[y+'_primary']=dict(dem=sum(swd.values()),rep=sum(swr.values()),ballots=int(rp.find('ElectionVoterTurnout').get('ballotsCast')),timestamp=rp.findtext('Timestamp'))
    for c,(reg,bal) in tp.items():
        r=rows[c]; r[f'prim_dem_{y}']=sum(d[c].values()); r[f'prim_rep_{y}']=sum(rr[c].values()); r[f'prim_ballots_{y}']=bal;
assert len(rows)==46
F=list(next(iter(rows.values())).keys())
with open(V+'passA_counties.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=F); w.writeheader(); [w.writerow(rows[c]) for c in sorted(rows)]
# internal consistency: county sums == statewide totals in the same file
chk={}
for y in ('2022','2026'):
    chk[y]=dict(dem=sum(r[f'dem_{y}'] for r in rows.values())==SW[y]['gov']['DEM'],rep=sum(r[f'rep_{y}'] for r in rows.values())==SW[y]['gov']['REP'],
       ballots=sum(r[f'ballots_{y}'] for r in rows.values())==SW[y]['ballots'],reg=sum(r[f'reg_{y}'] for r in rows.values())==SW[y]['reg'],
       primdem=sum(r[f'prim_dem_{y}'] for r in rows.values())==SW[y+'_primary']['dem'],primrep=sum(r[f'prim_rep_{y}'] for r in rows.values())==SW[y+'_primary']['rep'])
json.dump(dict(statewide=SW,county_sum_equals_statewide=chk),open(V+'passA_statewide.json','w'),indent=1)
print(json.dumps(chk)); print(len(rows),'counties x',len(F)-1,'figures')

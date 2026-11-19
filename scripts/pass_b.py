"""PASS B: independent of pass A. Parses each COUNTY's own Clarity ENR sub-site file (46 counties x 4 elections),
primarily summary.csv with the csv module (regex/string matching on contest names, no XML).
Fallbacks where the county summary.zip is not served (HTTP 404):
  - 2022 general, Clarendon: county detail.txt (fixed-width text, 'Total:' row), both the state-listed version 313514 and current 319025
  - 2026 primary, Lee: county detail.xml parsed with regex (not ElementTree)
Outputs verification/passB_counties.csv"""
import zipfile, csv, io, re, glob, os, json
R='/workspace/south-carolina-elections/raw/'; V='/workspace/south-carolina-elections/verification/'
def summ(path):
    t=zipfile.ZipFile(path).read('summary.csv').decode('utf-8-sig')
    return list(csv.DictReader(io.StringIO(t)))
def norm(s): return re.sub(r'\s+',' ',s).strip()
def from_summary(rows, contest_re):
    sel=[r for r in rows if re.fullmatch(contest_re, norm(r['contest name']))]
    byp={}
    for r in sel: byp[r['party name']]=byp.get(r['party name'],0)+int(r['total votes'])
    reg={int(r['registered voters']) for r in sel}; bal={int(r['ballots cast']) for r in sel}
    return byp, reg, bal, len(sel)
def from_detailtxt(path, contest_word):
    lines=zipfile.ZipFile(path).read('detail.txt').decode('latin-1').splitlines()
    # turnout block: Total: row
    tot=[l for l in lines[:400] if l.startswith('Total:')][0].split()
    reg,bal=int(tot[1]),int(tot[2])
    i=[k for k,l in enumerate(lines) if norm(l).startswith(contest_word)][0]
    cand=lines[i+1]; hdr=lines[i+2]
    # candidate names are placed over column groups; each group = 6 vote types + Choice Total (7 cols); final col = Total
    names=re.findall(r'(REP|DEM|LIB|GRN|UNC|CON|ALI|WFM|IND|NON)\s[^ ].*?(?=\s{3,}|$)|Write-In',cand)
    parties=re.findall(r'\b(REP|DEM|LIB|GRN|UNC|CON|ALI|WFM|IND)\s|Write-In',cand)
    parties=['NON' if p=='' else p for p in parties]
    k=i+3
    while not lines[k].startswith('Totals:'): k+=1
    nums=[int(x) for x in lines[k].split()[1:]]
    ngrp=(len(nums)-2)//7
    assert len(parties)==ngrp,(parties,ngrp,len(nums))
    byp={}
    for g,p in enumerate(parties): byp[p]=byp.get(p,0)+nums[1+g*7+6]
    assert sum(byp.values())==nums[-1]
    return byp,{reg},{bal},ngrp
def from_detailxml_regex(path, contest_text):
    x=zipfile.ZipFile(path).read('detail.xml').decode('utf-8')
    vt=re.search(r'<(?:Election)?VoterTurnout totalVoters="(\d+)" ballotsCast="(\d+)"',x)
    m=re.search(r'<Contest key="\d+" text="'+re.escape(contest_text)+r'".*?</Contest>',x,re.S)
    byp={}
    for p,tv in re.findall(r'<Choice key="\d+" text="[^"]*" party="([^"]*)" totalVotes="(\d+)"',m.group(0)):
        byp[p]=byp.get(p,0)+int(tv)
    return byp,{int(vt.group(1))},{int(vt.group(2))},1
def turnout_b(d,c):
    '''registered + ballots cast from the county's own detail.xml <VoterTurnout> (regex); fallback county detail.txt Total: row'''
    px=sorted(glob.glob(R+d+f'/counties/{c}_*_detailxml.zip'))
    if px:
        x=zipfile.ZipFile(px[0]).read('detail.xml').decode('utf-8','replace')
        m=re.search(r'<VoterTurnout totalVoters="(\d+)" ballotsCast="(\d+)"',x); return int(m.group(1)),int(m.group(2)),'county detail.xml VoterTurnout'
    pt=sorted(glob.glob(R+d+f'/counties/{c}_*_detailtxt.zip'))[-1]
    lines=zipfile.ZipFile(pt).read('detail.txt').decode('latin-1').splitlines()
    t=[l for l in lines if l.startswith('Total:')][0].split(); return int(t[1]),int(t[2]),'county detail.txt Total: row '+os.path.basename(pt)
SUMCOL=[]
out={}; notes=[]
GOV=r'Governor and Lieutenant Governor \(Vote For 1\)'
for y in ('2022','2026'):
    for d,kind in ((y,'gen'),(y+'_primary','prim')):
        names=sorted({os.path.basename(p).split('_')[0] for p in glob.glob(R+d+'/counties/*')})
        assert len(names)==46,(d,len(names))
        for c in names:
            r=out.setdefault(c,{'county':c})
            sm=glob.glob(R+d+f'/counties/{c}_*_summary.zip')
            if kind=='gen':
                if sm: byp,reg,bal,n=from_summary(summ(sm[0]),GOV); src='county summary.csv'
                else:
                    res=[]
                    for p in sorted(glob.glob(R+d+f'/counties/{c}_*_detailtxt.zip')):
                        res.append((os.path.basename(p),from_detailtxt(p,'Governor and Lieutenant Governor')))
                    byp,reg,bal,n=res[-1][1]  # current county version 319025 (313514 shows Registered Voters = 0 on its Total row; votes and ballots identical)
                    if len(res)>1: notes.append(dict(county=c,election=d,versions_compared=[(a,b[0],sorted(b[1]),sorted(b[2])) for a,b in res],identical=all(b[:3]==res[0][1][:3] for a,b in res)))
                    src='county detail.txt'
                assert len(reg)==1 and len(bal)==1,(c,d,reg,bal)
                SUMCOL.append(dict(county=c,election=d,summary_reg=sorted(reg),summary_ballots=sorted(bal))); tr,tb,tsrc=turnout_b(d,c); r[f'reg_{y}']=tr; r[f'ballots_{y}']=tb; r.setdefault('_tsrc',{})[d]=tsrc; r[f'dem_{y}']=byp.get('DEM',0); r[f'rep_{y}']=byp.get('REP',0)
                r[f'other_{y}']=sum(v for p,v in byp.items() if p not in('DEM','REP')); r[f'govtotal_{y}']=sum(byp.values())
            else:
                if sm:
                    rows=summ(sm[0]); bd,reg,bal,_=from_summary(rows,r'Governor - DEM \(Vote For 1\)'); br,reg2,bal2,_=from_summary(rows,r'Governor - REP \(Vote For 1\)'); assert reg==reg2 and bal==bal2,(c,reg,reg2,bal,bal2); src='county summary.csv'
                else:
                    p=glob.glob(R+d+f'/counties/{c}_*_detailxml.zip')[0]
                    bd,reg,bal,_=from_detailxml_regex(p,'Governor - DEM'); br,_,_,_=from_detailxml_regex(p,'Governor - REP'); src='county detail.xml (regex)'
                assert len(reg)==1 and len(bal)==1,(c,d,reg,bal)
                r[f'prim_dem_{y}']=sum(bd.values()); r[f'prim_rep_{y}']=sum(br.values()); tr,tb,tsrc=turnout_b(d,c); r[f'prim_ballots_{y}']=tb; r.setdefault('_tsrc',{})[d]=tsrc
            r.setdefault('_src',{})[d]=src
F=['county']+[k for k in next(iter(out.values())) if k not in('county','_src','_tsrc')]
with open(V+'passB_counties.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=F,extrasaction='ignore'); w.writeheader(); [w.writerow(out[c]) for c in sorted(out)]
json.dump(dict(vote_sources={c:out[c]['_src'] for c in out},turnout_sources={c:out[c]['_tsrc'] for c in out},notes=notes,summary_csv_contest_level_reg_ballots=SUMCOL),open(V+'passB_sources.json','w'),indent=1)
print(len(out),'counties'); print(json.dumps(notes,indent=0)); print({c:s for c,s in ((c,out[c]['_src']) for c in out) if any('summary' not in v for v in s.values())})

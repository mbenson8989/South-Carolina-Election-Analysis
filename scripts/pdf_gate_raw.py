"""Independent raw recompute for the county PDF gate.
General: per-county detail.xml files (raw/<y>/counties), regex parsing.
Primary: state-level detail.txt (raw/<y>_primary/reports_detailtxt.zip), fixed-width text parsing.
Imports nothing from the other pipeline scripts and reads no summary CSV/JSON."""
import zipfile,re,glob,os,json
R='/workspace/south-carolina-elections/raw/'
def general(y):
    out={}
    files={}
    for f in glob.glob(R+y+'/counties/*_detailxml.zip'):
        c,_,ver=os.path.basename(f).rsplit('_',3)[0],None,int(os.path.basename(f).split('_')[-2])
        c=os.path.basename(f).rsplit('_',3)[0].replace('_',' ')
        if c not in files or ver>files[c][0]: files[c]=(ver,f)
    for c,(v,f) in files.items():
        s=zipfile.ZipFile(f).read('detail.xml').decode()
        bal=int(re.search(r'<VoterTurnout [^>]*ballotsCast="(\d+)"',s).group(1))
        i=s.index('text="Governor and Lieutenant Governor"'); j=s.find('</Contest>',i)
        dem=sum(int(x) for x in re.findall(r'<Choice [^>]*party="DEM" totalVotes="(\d+)"',s[i:j]))
        out[c]=dict(ballots=bal,dem=dem)
    # counties published only as detail.txt (2022 Clarendon): parse the fixed-width Total rows, latest version
    tf={}
    for f in glob.glob(R+y+'/counties/*_detailtxt.zip'):
        c=os.path.basename(f).rsplit('_',3)[0].replace('_',' '); ver=int(os.path.basename(f).split('_')[-2])
        if c in out: continue
        if c not in tf or ver>tf[c][0]: tf[c]=(ver,f)
    for c,(v,f) in tf.items():
        s=zipfile.ZipFile(f).read('detail.txt').decode('utf-8','replace')
        bal=int([re.split(r'\s{2,}',l.strip()) for l in s.splitlines() if re.match(r'\s*Total:',l)][0][2])
        i=s.index('Governor and Lieutenant Governor (Vote For 1)'); hdr=s[i:].splitlines()[1]
        names=re.split(r'\s{2,}',hdr.strip()); k=[n for n in names].index([n for n in names if n.startswith('DEM ')][0])
        blk=s[i:s.find('(Vote For',i+50)]
        tot=[re.split(r'\s{2,}',l.strip()) for l in blk.splitlines() if re.match(r'\s*Totals?:',l)][0]
        out[c]=dict(ballots=bal,dem=int(tot[1+7*k+7]))
    return out
def primary(y,party):
    s=zipfile.ZipFile(R+y+'_primary/reports_detailtxt.zip').read('detail.txt').decode('utf-8','replace')
    i=s.index('Governor - %s (Vote For 1)'%party); j=s.find('(Vote For',i+30); blk=s[i:j if j>0 else None]
    out={}
    for line in blk.splitlines():
        parts=re.split(r'\s{2,}',line.strip())
        if len(parts)>3 and all(re.fullmatch(r'\d+',p) for p in parts[1:]) and parts[0] not in ('Total',):
            out[parts[0]]=int(parts[-1])
    return out
res={}
for y in ('2022','2026'):
    g=general(y); pd=primary(y,'DEM'); pr=primary(y,'REP')
    for c in g:
        res.setdefault(c,{})
        res[c].update({f'dem_{y}':g[c]['dem'],f'ballots_{y}':g[c]['ballots'],f'pd_{y}':pd[c],f'pr_{y}':pr[c]})
assert len(res)==46,len(res)
json.dump(res,open('/workspace/south-carolina-elections/verification/pdf_gate_raw_counts.json','w'),indent=1)
print(len(res),'counties'); print(res['Abbeville'])

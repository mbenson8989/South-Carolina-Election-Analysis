"""Download each county's own Clarity ENR sub-site (summary.zip + detailxml.zip) for the 4 elections.
County election IDs/versions come from the state electionsettings.json 'electiondetails' list."""
import json,gzip,re,os,subprocess,datetime
R='/workspace/south-carolina-elections/raw/'
EL={'2022':'115412','2026':'127300','2022_primary':'114143','2026_primary':'126294'}
log=[]
for d,eid in EL.items():
    b=open(R+d+'/json_en_electionsettings.json','rb').read()
    if b[:2]==b'\x1f\x8b': b=gzip.decompress(b)
    s=json.loads(b); det=s['settings']['electiondetails']
    items=det if isinstance(det,list) else json.loads(det) if isinstance(det,str) else det
    txt=json.dumps(items)
    ents=re.findall(r'([A-Za-z]+)\|(\d+)\|(\d+)\|([^|"]+)\|(\d+)',txt)
    os.makedirs(R+d+'/counties',exist_ok=True)
    for name,cid,ver,ts,code in ents:
        for f in ['reports/summary.zip','reports/detailxml.zip']:
            url=f'https://www.enr-scvotes.org/SC/{name}/{cid}/{ver}/{f}'
            out=R+d+f'/counties/{name}_{cid}_{ver}_{f.split("/")[1]}'
            c=subprocess.run(['curl','-sL','-A','Mozilla/5.0','-o',out,'-w','%{http_code}',url],capture_output=True,text=True).stdout
            log.append(dict(election=d,county=name,cid=cid,ver=ver,updated=ts,code=code,file=f,url=url,http=c,retrieved=datetime.datetime.now().isoformat()))
            if c!='200': os.remove(out)
    print(d,len(ents))
json.dump(log,open(R+'county_sites_download_log.json','w'),indent=1)
print(sum(1 for l in log if l['http']!='200'),'failures')

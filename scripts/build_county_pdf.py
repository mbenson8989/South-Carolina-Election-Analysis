"""Build the SC 46-county PDF from repo/data CSV (pass A counts, re-verified against raw by pdf_gate_raw.py)."""
import csv
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
OUT='/workspace/south-carolina-elections/pdf/South_Carolina_46_County_Democratic_Primary_Proxy_and_Vote_Change.pdf'
rows=list(csv.DictReader(open('/workspace/south-carolina-elections/repo/data/SC_Governor_2022_2026_DeltaG_by_County.csv')))
def n(x): return f'{x:,}'
def sg(x): return ('+' if x>0 else '') + f'{x:,}'
def pc(a,b): v=100*(b-a)/a; return ('+' if v>0 else '')+f'{v:.1f}%'
def sh(d,r): return f'{100*d/(d+r):.1f}%'
data=[]
for r in rows:
    I=lambda k:int(r[k])
    data.append(dict(c=r['county'],pd=I('prim_dem_2026'),pr=I('prim_rep_2026'),d22=I('dem_2022'),d26=I('dem_2026'),b22=I('ballots_2022'),b26=I('ballots_2026')))
data.sort(key=lambda x:-x['pd']/(x['pd']+x['pr']))
T={k:sum(x[k] for x in data) for k in ('pd','pr','d22','d26','b22','b26')}
hdr=['County','Dem Share\n2026* %\n(primary proxy)','Dem Gov Votes\n2022','Dem Gov Votes\n2026*','Vote Change\n#','Vote Change\n%','Total Ballots\n2022','Total Ballots\n2026*','Ballot Change\n#','Ballot Change\n%']
def line(x,name): return [name,sh(x['pd'],x['pr']),n(x['d22']),n(x['d26']),sg(x['d26']-x['d22']),pc(x['d22'],x['d26']),n(x['b22']),n(x['b26']),sg(x['b26']-x['b22']),pc(x['b22'],x['b26'])]
body=[hdr]+[line(x,x['c']) for x in data]+[line(T,'Statewide total')]
ss=getSampleStyleSheet(); small=ParagraphStyle('s',parent=ss['Normal'],fontSize=7.5,leading=9.5)
title=ParagraphStyle('t',parent=ss['Title'],fontSize=13,leading=16,spaceAfter=4)
story=[Paragraph('South Carolina 46 Counties: Democratic Primary-Share Proxy, Democratic Governor Votes and Total Ballots, 2022 vs 2026*',title),
 Paragraph('Sorted by 2026 Democratic share, highest first. <b>PROXY:</b> South Carolina has no party registration, so "Dem Share" is the Democratic share of governor-primary voters: Democratic governor-primary votes \u00f7 (Democratic + Republican governor-primary votes), June 2026 primary. It is a stand-in for party registration, not official registration.',small),
 Paragraph('Source: South Carolina State Election Commission official results (scvotes.gov / enr-scvotes.org): 2022 and 2026 general-election governor results and ballots cast, 2022 and 2026 governor primaries. Dem Gov Votes are votes for the Democratic governor candidate. Changes are 2026* minus 2022; percent changes use 2022 as the base. *2026 figures are unofficial.',small),Spacer(1,6)]
t=Table(body,repeatRows=1,colWidths=[100,70,68,68,62,58,68,68,64,58])
st=[('FONT',(0,0),(-1,-1),'Helvetica',8),('FONT',(0,0),(-1,0),'Helvetica-Bold',7.5),('ALIGN',(1,0),(-1,-1),'RIGHT'),('VALIGN',(0,0),(-1,0),'BOTTOM'),
    ('LINEBELOW',(0,0),(-1,0),0.8,colors.black),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eef5')),('FONT',(0,-1),(-1,-1),'Helvetica-Bold',8),
    ('LINEABOVE',(0,-1),(-1,-1),0.8,colors.black),('TOPPADDING',(0,0),(-1,-1),1.6),('BOTTOMPADDING',(0,0),(-1,-1),1.6)]
for i in range(1,len(body)-1):
    if i%2==0: st.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#f6f6f6')))
t.setStyle(TableStyle(st)); story.append(t)
def foot(cv,doc):
    cv.saveState(); cv.setFont('Helvetica',7.5)
    cv.drawString(36,20,'*2026 figures unofficial. Dem Share is a governor-primary proxy, not party registration (SC has none).')
    cv.drawRightString(756,20,f'Page {doc.page}'); cv.restoreState()
SimpleDocTemplate(OUT,pagesize=landscape(letter),leftMargin=36,rightMargin=36,topMargin=30,bottomMargin=34,title='South Carolina 46 County Democratic Primary Proxy and Vote Change',author='Morissa Benson').build(story,onFirstPage=foot,onLaterPages=foot)
print(OUT)

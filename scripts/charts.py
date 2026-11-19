import pandas as pd, numpy as np, json, textwrap
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
O='/workspace/south-carolina-elections/repo/'; o=pd.read_pickle('/tmp/sc_o.pkl'); J=json.load(open(O+'data/SC_results_summary.json'))
N=len(o); x=np.arange(N); names=list(o.index); DPI=150
FOOT=("PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration). P = Dem governor-primary votes ÷ (Dem + Rep governor-primary votes), June primaries.\n"
      "S = Dem governor votes ÷ total ballots cast. G = S − P. Source: SC Election Commission ENR (enr-scvotes.org) elections 115412, 127300, 114143, 126294. "
      "2022 official; 2026 UNOFFICIAL (SEC results version 386661, 11/10/2026). Population: Census Vintage 2025 (sort order only).")
def foot(fig):
    wd=int(fig.get_figwidth()*17); fig.text(0.01,0.005,'\n'.join(textwrap.fill(l,wd) for l in FOOT.split('\n')),fontsize=7,color='#444',va='bottom')
CEIL=J['K']['ceiling']; FLOOR=J['K']['floor']; NAR=J['narrow']['counties']
RC={'Upstate':'#2e7d32','Midlands':'#6a1b9a','Pee Dee':'#ef6c00','Lowcountry':'#0277bd'}
WIDE=(22,8.5)
# 1 slope
fig,ax=plt.subplots(figsize=(10,13)); LAB=[]
for c,r in o.iterrows():
    col='#c0392b' if c in CEIL else ('#1f4e9a' if c in FLOOR else '#9aa5b1'); lw=2 if col!='#9aa5b1' else 0.7
    ax.plot([0,1],[r.G22,r.G26],color=col,lw=lw,alpha=0.9 if lw>1 else 0.5)
    if lw>1: LAB.append((r.G26,f"{c} (ΔG {r.dG:+.2f})",col))
LAB.sort(); last=-999
for y,t,col in LAB:
    yy=max(y,last+2.2); last=yy; ax.annotate(t,(1,y),xytext=(1.04,yy),fontsize=8,va='center',color=col,arrowprops=dict(arrowstyle='-',color=col,lw=0.5))
ax.axhline(0,color='#333',lw=0.6); ax.set_xticks([0,1]); ax.set_xticklabels(['2022','2026']); ax.set_xlim(-0.1,1.45)
ax.set_ylabel('G = S − P (points)'); ax.set_title('South Carolina governor: county G, 2022 → 2026 (46 counties)\nRed = 5 ceiling counties (largest ΔG); blue = 5 floor counties (lowest 2022 proxy share)')
fig.subplots_adjust(bottom=0.1); foot(fig); fig.savefig(O+'SC_Slope_G2022_to_G2026.png',dpi=DPI); plt.close()
# 2 dG by population
fig,ax=plt.subplots(figsize=WIDE)
cols=['#c0392b' if c in CEIL else ('#1f4e9a' if c in FLOOR else ('#e67e22' if v>0 else '#7f8c8d')) for c,v in o.dG.items()]
ax.bar(x,o.dG,color=cols); ax.axhline(0,color='#333',lw=0.7)
for i,(c,v) in enumerate(o.dG.items()):
    if c in CEIL or c in FLOOR: ax.text(i,v+(0.6 if v>0 else -0.6),f'{v:+.1f}',ha='center',va='bottom' if v>0 else 'top',fontsize=7)
ax.set_xticks(x); ax.set_xticklabels(names,rotation=90,fontsize=8); ax.set_xlim(-1,N); ax.set_ylabel('ΔG = G2026 − G2022 (points)')
ax.set_title(f'South Carolina governor: ΔG by county, largest population (left) to smallest. Ceiling (red): {", ".join(CEIL)}. Floor (blue): {", ".join(FLOOR)}.',fontsize=10)
fig.subplots_adjust(bottom=0.25); foot(fig); fig.savefig(O+'SC_DeltaG_by_Population.png',dpi=DPI); plt.close()
# 3 components: dS and -dP
fig,ax=plt.subplots(figsize=WIDE); w=0.4
ax.bar(x-w/2,o.dS,w,color='#2c7fb8',label='ΔS: change in Dem share of ballots (2026 − 2022)')
ax.bar(x+w/2,-o.dP,w,color='#d95f0e',label='−ΔP: minus change in proxy Dem primary share')
ax.plot(x,o.dG,'k_',ms=10,mew=2,label='ΔG = ΔS − ΔP'); ax.axhline(0,color='#333',lw=0.7)
ax.set_xticks(x); ax.set_xticklabels(names,rotation=90,fontsize=8); ax.set_xlim(-1,N); ax.set_ylabel('points'); ax.legend(loc='lower left')
ax.set_title(f'What drives ΔG in South Carolina: ΔS is +0.0 to +10.9 in every county (median {o.dS.median():+.2f}); the proxy change ΔP ranges {o.dP.min():+.1f} to {o.dP.max():+.1f}. Largest population left.',fontsize=10)
fig.subplots_adjust(bottom=0.25); foot(fig); fig.savefig(O+'SC_DeltaG_Components_dS_vs_dP_by_Population.png',dpi=DPI); plt.close()
# 4 stacked share by population
fig,ax=plt.subplots(figsize=WIDE)
base=np.minimum(o.S22,o.S26); ax.bar(x,base,color='#5b8bd0',label='Dem share of ballots kept (lower of 2022/2026)')
ax.bar(x,np.maximum(o.dS,0),bottom=base,color='#e67e22',label='2026 gain in Dem share of ballots')
ax.scatter(x,o.P22,marker='v',color='#1f4e9a',zorder=3,label='Proxy P 2022'); ax.scatter(x,o.P26,marker='^',color='#c0392b',zorder=3,label='Proxy P 2026')
ax.set_xticks(x); ax.set_xticklabels(names,rotation=90,fontsize=8); ax.set_xlim(-1,N); ax.set_ylim(0,100); ax.set_ylabel('%'); ax.legend(loc='upper right',fontsize=8)
ax.set_title('South Carolina governor: Democratic share of ballots (bars) and proxy Democratic primary share (markers), largest population left',fontsize=10)
fig.subplots_adjust(bottom=0.25); foot(fig); fig.savefig(O+'SC_Stacked_Share_and_Proxy_by_Population.png',dpi=DPI); plt.close()
# 5 forward fit
fig,axs=plt.subplots(1,2,figsize=(18,8.5),sharey=True)
for ax,t,y in ((axs[0],'22','2022'),(axs[1],'26','2026')):
    f=J['fits'][y]; fn=J['fits'][y+'_narrowed']
    for c,r in o.iterrows():
        ax.scatter(r['P'+t],r['G'+t],color=RC[r.region],s=40,edgecolor='k' if c in NAR else 'none',lw=1.5,zorder=3)
        if c in NAR or c in CEIL or c in FLOOR: ax.annotate(c,(r['P'+t],r['G'+t]),fontsize=7,xytext=(3,3),textcoords='offset points')
    xx=np.linspace(0,100,10); ax.plot(xx,f['m']*xx/100+f['b'],'k-',label=f"all 46: G = {f['m']:.2f}·(P/100) + {f['b']:.2f}, R² {f['r2']:.2f}")
    ax.plot(xx,fn['m']*xx/100+fn['b'],'k--',label=f"narrowed (n={fn['n']}): m {fn['m']:.2f}, b {fn['b']:.2f}, R² {fn['r2']:.2f}")
    ax.axhline(0,color='#999',lw=0.5); ax.set_xlabel('Proxy P: Dem share of governor-primary votes (%)'); ax.set_title(f'{y}'); ax.legend(fontsize=8,loc='lower left')
for g,cl in RC.items(): axs[1].scatter([],[],color=cl,label=g)
axs[1].legend(fontsize=8,loc='lower left'); axs[0].set_ylabel('G = S − P (points)')
fig.suptitle('South Carolina forward fit (SC-only constants): G vs proxy P. Black outline = narrowed-out counties.'); fig.subplots_adjust(bottom=0.16); foot(fig)
fig.savefig(O+'SC_Forward_Fit_G_vs_P_2022_2026.png',dpi=DPI); plt.close()
# 6 dG vs dP
fig,ax=plt.subplots(figsize=(11,9)); f=J['fits']['dG_on_dP']
for c,r in o.iterrows():
    ax.scatter(r.dP,r.dG,color=RC[r.region],s=40); ax.annotate(c,(r.dP,r.dG),fontsize=6,xytext=(2,2),textcoords='offset points')
xx=np.linspace(o.dP.min()-1,o.dP.max()+1,10); ax.plot(xx,f['m']*xx/100+f['b'],'k-',label=f"ΔG = {f['m']/100:.3f}·ΔP + {f['b']:.2f}  (R² {f['r2']:.2f})")
for g,cl in RC.items(): ax.scatter([],[],color=cl,label=g)
ax.axhline(0,color='#999',lw=0.5); ax.axvline(0,color='#999',lw=0.5); ax.legend(fontsize=8)
ax.set_xlabel('ΔP: change in proxy Dem primary share (points)'); ax.set_ylabel('ΔG (points)')
ax.set_title('South Carolina: ΔG is almost entirely the proxy change.\nA slope near −1 and an intercept near +7 means ΔS rose about 7 points nearly everywhere.')
fig.subplots_adjust(bottom=0.14); foot(fig); fig.savefig(O+'SC_DeltaG_vs_DeltaP_Scatter.png',dpi=DPI); plt.close()
# 7 regional fits
fig,axs=plt.subplots(2,4,figsize=(22,10),sharex=True,sharey='row')
for i,(t,y) in enumerate((('22','2022'),('26','2026'))):
    for j,g in enumerate(['Upstate','Midlands','Pee Dee','Lowcountry']):
        ax=axs[i,j]; d=o[o.region==g]; pr=J['regions'][t]['per_region'][g]
        ax.scatter(d['P'+t],d['G'+t],color=RC[g]); [ax.annotate(c,(r['P'+t],r['G'+t]),fontsize=6) for c,r in d.iterrows()]
        xx=np.linspace(0,100,10); ax.plot(xx,pr['m']*xx/100+pr['b'],color=RC[g],label=f"region: m {pr['m']:.1f}, b {pr['b']:.1f}, R² {pr['r2']:.2f}")
        f=J['fits'][y]; ax.plot(xx,f['m']*xx/100+f['b'],'k--',lw=0.8,label='statewide line'); ax.legend(fontsize=7); ax.set_title(f'{g} {y} (n={pr["n"]})')
fig.suptitle(f"Regional constants test (regions from SC Councils of Governments). Separate regional lines vs one line: 2022 p = {J['regions']['22']['p_full']:.3f}; 2026 p = {J['regions']['26']['p_full']:.5f}, but {J['regions']['26']['p_full_narrowed']:.2f} after narrowing out {', '.join(NAR)}")
fig.subplots_adjust(bottom=0.12); foot(fig); fig.savefig(O+'SC_Regional_Fits.png',dpi=DPI); plt.close()
# 8 overballot margin
fig,ax=plt.subplots(figsize=WIDE); w=0.4
m22=100*(o.ballots_2022-o.dem_2022-o.rep_2022)/o.ballots_2022; m26=100*(o.ballots_2026-o.dem_2026-o.rep_2026)/o.ballots_2026
ax.bar(x-w/2,m22,w,color='#7f8c8d',label='2022'); ax.bar(x+w/2,m26,w,color='#2c7fb8',label='2026'); ax.axhline(0,color='r',lw=1,label='over-ballot line (D + R = ballots)')
ax.set_xticks(x); ax.set_xticklabels(names,rotation=90,fontsize=8); ax.set_xlim(-1,N); ax.set_ylabel('(ballots − D − R) as % of ballots'); ax.legend()
ax.set_title('Texas-style check: ballots cast minus (Dem + Rep governor votes). Every bar is above zero: no South Carolina county has D + R > ballots in either year. Largest population left.',fontsize=10)
fig.subplots_adjust(bottom=0.25); foot(fig); fig.savefig(O+'SC_Overballot_Check_by_Population.png',dpi=DPI); plt.close()
print('ok')

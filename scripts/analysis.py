"""South Carolina governor 2022 vs 2026 county analysis. Runs ONLY on the pass-A table after asserting pass B is identical
on every figure used here. PROXY: Democratic primary-ballot share (governor primary race votes), not party registration."""
import pandas as pd, numpy as np, json, statsmodels.api as sm, statsmodels.formula.api as smf
from scipy import stats
W='/workspace/south-carolina-elections/'; V=W+'verification/'; O=W+'repo/'
A=pd.read_csv(V+'passA_counties.csv',index_col='county'); B=pd.read_csv(V+'passB_counties.csv',index_col='county')
USED=['ballots_2022','dem_2022','rep_2022','other_2022','govtotal_2022','prim_dem_2022','prim_rep_2022','prim_ballots_2022',
      'ballots_2026','dem_2026','rep_2026','other_2026','govtotal_2026','prim_dem_2026','prim_rep_2026','prim_ballots_2026','reg_2026']
assert (A[USED]==B.loc[A.index,USED]).all().all(), 'pass A/B disagree on an analysis figure'
o=A.copy()
# population (Census Vintage 2025, plus April 1 2020 estimates base)
c=pd.read_csv(W+'raw/census/co-est2025-alldata.csv',encoding='latin-1',dtype={'STATE':str,'COUNTY':str,'SUMLEV':str})
c=c[(c.SUMLEV=='050')&(c.STATE=='45')]; c.index=c.CTYNAME.str.replace(' County','')
o['pop2025']=c.POPESTIMATE2025.reindex(o.index); o['pop2020base']=c.ESTIMATESBASE2020.reindex(o.index); assert o.pop2025.notna().all()
o=o.sort_values('pop2025',ascending=False)
COG={'Appalachian':['Anderson','Cherokee','Greenville','Oconee','Pickens','Spartanburg'],'Upper Savannah':['Abbeville','Edgefield','Greenwood','Laurens','McCormick','Saluda'],
 'Catawba':['Chester','Lancaster','Union','York'],'Central Midlands':['Fairfield','Lexington','Newberry','Richland'],'Santee-Lynches':['Clarendon','Kershaw','Lee','Sumter'],
 'Lower Savannah':['Aiken','Allendale','Bamberg','Barnwell','Calhoun','Orangeburg'],'Pee Dee':['Chesterfield','Darlington','Dillon','Florence','Marion','Marlboro'],
 'Waccamaw':['Georgetown','Horry','Williamsburg'],'Berkeley-Charleston-Dorchester':['Berkeley','Charleston','Dorchester'],'Lowcountry':['Beaufort','Colleton','Hampton','Jasper']}
REG={'Appalachian':'Upstate','Upper Savannah':'Upstate','Catawba':'Upstate','Central Midlands':'Midlands','Santee-Lynches':'Midlands','Lower Savannah':'Midlands',
     'Pee Dee':'Pee Dee','Waccamaw':'Pee Dee','Berkeley-Charleston-Dorchester':'Lowcountry','Lowcountry':'Lowcountry'}
cog={x:k for k,v in COG.items() for x in v}; assert len(cog)==46 and set(cog)==set(o.index)
o['cog']=o.index.map(cog); o['region']=o.cog.map(REG)
for y,t in (('2022','22'),('2026','26')):
    o['S'+t]=100*o[f'dem_{y}']/o[f'ballots_{y}']
    o['P'+t]=100*o[f'prim_dem_{y}']/(o[f'prim_dem_{y}']+o[f'prim_rep_{y}'])
    o['G'+t]=o['S'+t]-o['P'+t]
o['dS']=o.S26-o.S22; o['dP']=o.P26-o.P22; o['dG']=o.G26-o.G22
o['loss']=o.prim_dem_2026<o.prim_dem_2022
o['residual']=np.where(o.loss,o.dG-o.dP.abs(),np.nan)
o['implied_extra_votes']=o.dem_2026-o.S22/100*o.ballots_2026
o['gap_primary_scaled']=o.dem_2026-o.dem_2022*(o.prim_dem_2026/o.prim_dem_2022)
# ---------- forward fit (SC constant): G = m*(P/100)+b ----------
def fit(y,x,w=None):
    X=sm.add_constant(np.asarray(x,float)/100); r=(sm.WLS(np.asarray(y,float),X,weights=w) if w is not None else sm.OLS(np.asarray(y,float),X)).fit()
    res=np.asarray(y)-r.fittedvalues; ci=r.conf_int()
    return dict(n=int(len(y)),m=float(r.params[1]),m_se=float(r.bse[1]),m_ci=[float(ci[1,0]),float(ci[1,1])],b=float(r.params[0]),b_se=float(r.bse[0]),b_ci=[float(ci[0,0]),float(ci[0,1])],
        r2=float(r.rsquared),resid_se=float(np.sqrt(np.sum(res**2)/(len(y)-2))),rms=float(np.sqrt(np.mean(res**2))),
        within1=float(np.mean(np.abs(res)<=1)),within2=float(np.mean(np.abs(res)<=2)),within3=float(np.mean(np.abs(res)<=3)),med_abs=float(np.median(np.abs(res)))),r
F={}
F['2022'],r22=fit(o.G22,o.P22); F['2026'],r26=fit(o.G26,o.P26)
F['2022_wtd'],_=fit(o.G22,o.P22,o.ballots_2022); F['2026_wtd'],_=fit(o.G26,o.P26,o.ballots_2026)
F['pooled'],_=fit(np.r_[o.G22,o.G26],np.r_[o.P22,o.P26])
o['fit22']=np.asarray(r22.fittedvalues); o['res22']=o.G22-o.fit22; o['fit26']=np.asarray(r26.fittedvalues); o['res26']=o.G26-o.fit26
# year interaction
L=pd.DataFrame(dict(G=np.r_[o.G22,o.G26],P=np.r_[o.P22,o.P26]/100,yr=np.r_[np.zeros(46),np.ones(46)]))
ri=smf.ols('G~P*yr',L).fit(); F['year_interaction']=dict(d_intercept=float(ri.params['yr']),p_d_intercept=float(ri.pvalues['yr']),d_slope=float(ri.params['P:yr']),p_d_slope=float(ri.pvalues['P:yr']))
# ΔG model as the reverse-factoring constant across counties: dG = k*dP + c  (how much of the proxy-share change shows up in G)
F['dG_on_dP'],rd=fit(o.dG,o.dP)
# ---------- narrowing: influential counties ----------
NAR={}
for t,rr in (('22',r22),('26',r26)):
    inf=rr.get_influence(); cd=inf.cooks_distance[0]; st=inf.resid_studentized_external
    NAR[t]=pd.DataFrame(dict(cooks=cd,stud=st,lev=inf.hat_matrix_diag),index=o.index)
flag=sorted(set(NAR['22'].index[(NAR['22'].cooks>4/46)|(NAR['22'].stud.abs()>2.5)])|set(NAR['26'].index[(NAR['26'].cooks>4/46)|(NAR['26'].stud.abs()>2.5)]))
k=o.drop(flag); F['2022_narrowed'],_=fit(k.G22,k.P22); F['2026_narrowed'],_=fit(k.G26,k.P26)
NARROW=dict(rule='Cook\'s distance > 4/n (0.087) or |externally studentized residual| > 2.5, in either year\'s fit',counties=flag,
  detail={c_:dict(cooks22=float(NAR['22'].loc[c_,'cooks']),stud22=float(NAR['22'].loc[c_,'stud']),cooks26=float(NAR['26'].loc[c_,'cooks']),stud26=float(NAR['26'].loc[c_,'stud']),
          P22=float(o.loc[c_,'P22']),G22=float(o.loc[c_,'G22']),P26=float(o.loc[c_,'P26']),G26=float(o.loc[c_,'G26'])) for c_ in flag})
# ---------- regional constants ----------
RG={}
for t in ('22','26'):
    d=pd.DataFrame(dict(G=o['G'+t],P=o['P'+t]/100,region=o.region))
    base=smf.ols('G~P',d).fit(); inter=smf.ols('G~P+C(region)',d).fit(); full=smf.ols('G~P*C(region)',d).fit()
    a1=sm.stats.anova_lm(base,inter); a2=sm.stats.anova_lm(base,full)
    per={}
    for g,dd in d.groupby('region'):
        rr_=smf.ols('G~P',dd).fit(); per[g]=dict(n=int(len(dd)),m=float(rr_.params['P']),b=float(rr_.params['Intercept']),r2=float(rr_.rsquared),m_se=float(rr_.bse['P']),counties=list(dd.index))
    # also on narrowed set
    dn=d.drop(flag); bn=smf.ols('G~P',dn).fit(); fn=smf.ols('G~P*C(region)',dn).fit(); an=sm.stats.anova_lm(bn,fn)
    RG[t]=dict(F_intercepts=float(a1.F[1]),p_intercepts=float(a1['Pr(>F)'][1]),F_full=float(a2.F[1]),p_full=float(a2['Pr(>F)'][1]),r2_single=float(base.rsquared),r2_full=float(full.rsquared),
               p_full_narrowed=float(an['Pr(>F)'][1]),per_region=per)
dgr=o.groupby('region').dG.agg(['count','mean','median','min','max']); kw=stats.kruskal(*[g.dG.values for _,g in o.groupby('region')])
RG['dG_by_region']=dgr.round(3).to_dict(orient='index'); RG['dG_kruskal']=dict(H=float(kw.statistic),p=float(kw.pvalue))
# ---------- floor / ceiling ----------
FLOOR=o.sort_values('P22').head(5); CEIL=o.sort_values('dG',ascending=False).head(5)
lowdG=o.sort_values('dG').head(5); lowS=o.sort_values('S22').head(5)
lr=stats.linregress(np.log10(o.pop2025),o.dG)
K=dict(floor_rule='five lowest 2022 proxy shares P2022 (most Republican primary baseline)',floor=FLOOR.index.tolist(),ceiling_rule='five largest ΔG',ceiling=CEIL.index.tolist(),
  floor_by_dG=o.dG.idxmin(),ceiling_by_dG=o.dG.idxmax(),lowest5_dG=lowdG.index.tolist(),lowest5_S22=lowS.index.tolist(),
  mean_dG=float(o.dG.mean()),median_dG=float(o.dG.median()),sd_dG=float(o.dG.std()),n_pos=int((o.dG>0).sum()),n_neg=int((o.dG<0).sum()),
  n_loss=int(o.loss.sum()),loss_counties=o.index[o.loss].tolist(),n_P_fell=int((o.dP<0).sum()),n_S_rose=int((o.dS>0).sum()),
  size_slope=dict(slope=float(lr.slope),r=float(lr.rvalue),p=float(lr.pvalue)),
  median_residual=float(np.nanmedian(o.residual)) if o.loss.any() else None)
T=o.sum(numeric_only=True)
PO=dict(S22=100*T.dem_2022/T.ballots_2022,S26=100*T.dem_2026/T.ballots_2026,P22=100*T.prim_dem_2022/(T.prim_dem_2022+T.prim_rep_2022),P26=100*T.prim_dem_2026/(T.prim_dem_2026+T.prim_rep_2026))
PO.update(G22=PO['S22']-PO['P22'],G26=PO['S26']-PO['P26']); PO['dG']=PO['G26']-PO['G22']; PO['dP']=PO['P26']-PO['P22']; PO['dS']=PO['S26']-PO['S22']
PO['implied_extra_pooled']=(PO['S26']-PO['S22'])/100*T.ballots_2026; PO['implied_extra_sum']=float(o.implied_extra_votes.sum())
PO['totals']={k_:int(T[k_]) for k_ in USED+['reg_2022']}
s=max(-PO['dP'],0)/100; N=T.ballots_2026; p=PO['S26']/100
PO['offset']={f'cushion_{cu}':dict(switched=float((s+cu/100)*N),added=float((s+cu/100)*N/(1-p+s+cu/100))) for cu in (0,1,2)} if s>0 else 'proxy share did not fall statewide; no offset need'
# ---------- over-ballot (Texas-style) ----------
TX={}
for y in ('2022','2026'):
    TX[y]=dict(DR_gt_ballots=o.index[o[f'dem_{y}']+o[f'rep_{y}']>o[f'ballots_{y}']].tolist(),
               gov_gt_ballots=o.index[o[f'govtotal_{y}']>o[f'ballots_{y}']].tolist(),
               ballots_gt_reg=o.index[o[f'ballots_{y}']>o[f'reg_{y}']].tolist(),
               primary_DR_gt_primary_ballots=o.index[o[f'prim_dem_{y}']+o[f'prim_rep_{y}']>o[f'prim_ballots_{y}']].tolist(),
               min_margin_ballots_minus_DR=dict(county=(o[f'ballots_{y}']-o[f'dem_{y}']-o[f'rep_{y}']).idxmin(),votes=int((o[f'ballots_{y}']-o[f'dem_{y}']-o[f'rep_{y}']).min())),
               min_margin_ballots_minus_gov=dict(county=(o[f'ballots_{y}']-o[f'govtotal_{y}']).idxmin(),votes=int((o[f'ballots_{y}']-o[f'govtotal_{y}']).min())),
               nogov_pct_median=float((100*(o[f'ballots_{y}']-o[f'govtotal_{y}'])/o[f'ballots_{y}']).median()),
               nogov_pct_range=[float((100*(o[f'ballots_{y}']-o[f'govtotal_{y}'])/o[f'ballots_{y}']).min()),float((100*(o[f'ballots_{y}']-o[f'govtotal_{y}'])/o[f'ballots_{y}']).max())])
o['flag']=''
for c_ in FLOOR.index: o.loc[c_,'flag']='floor'
for c_ in CEIL.index: o.loc[c_,'flag']=(o.loc[c_,'flag']+'; ' if o.loc[c_,'flag'] else '')+'ceiling'
for c_ in flag: o.loc[c_,'flag']=(o.loc[c_,'flag']+'; ' if o.loc[c_,'flag'] else '')+'narrowed-out'
o.to_pickle('/tmp/sc_o.pkl')
cols=['pop2025','pop2020base','region','cog','flag','reg_2022','ballots_2022','dem_2022','rep_2022','other_2022','govtotal_2022','prim_dem_2022','prim_rep_2022','prim_ballots_2022','S22','P22','G22',
      'reg_2026','ballots_2026','dem_2026','rep_2026','other_2026','govtotal_2026','prim_dem_2026','prim_rep_2026','prim_ballots_2026','S26','P26','G26','dS','dP','dG','loss','residual','implied_extra_votes','gap_primary_scaled','fit22','res22','fit26','res26']
out=o[cols].copy(); out.insert(0,'proxy_label','PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration)')
out.insert(1,'status_2026','2026 certified by SC State Board of Canvassers 11/11/2026; SEC ENR v386661 (11/10/2026 5:20 PM EST)')
out.round(6).to_csv(O+'data/SC_Governor_2022_2026_DeltaG_by_County.csv')
J=dict(fits=F,narrow=NARROW,regions=RG,K=K,pooled=PO,overballot=TX)
json.dump(J,open(O+'data/SC_results_summary.json','w'),indent=1,default=lambda x: x.item() if hasattr(x,'item') else str(x))
print(json.dumps(J,indent=0,default=lambda x: x.item() if hasattr(x,'item') else str(x))[:9000])

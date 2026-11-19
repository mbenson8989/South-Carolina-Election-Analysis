"""Wiki builder v2 (layout fix, Nov 19 2026): short banner, narrow tables, 2026 marked unofficial with asterisks, _Sidebar.
Figures are computed exactly as in v1 (build_wiki_v1.py); only layout and wording changed."""
import pandas as pd, numpy as np, json, re, glob
W='/workspace/south-carolina-elections/'; O=W+'repo/'; WK=W+'wiki/'
o=pd.read_pickle('/tmp/sc_o.pkl'); J=json.load(open(O+'data/SC_results_summary.json')); C=json.load(open(W+'verification/compare_report.json'))
RAW='https://raw.githubusercontent.com/mbenson8989/South-Carolina-Election-Analysis/main/'
REPO='https://github.com/mbenson8989/South-Carolina-Election-Analysis'
CEDAR='https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit'
f=lambda n:f"{int(round(n)):,}"; sgi=lambda n:(f"{int(round(n)):+,}"); p2=lambda v:f"{v:.2f}"; sg=lambda v:f"{v:+.2f}"; pc=lambda v:f"{v:.2f}%"
S='\\*'   # escaped asterisk = 2026 unofficial marker
F=J['fits']; K=J['K']; PO=J['pooled']; RG=J['regions']; NAR=J['narrow']; TX=J['overballot']
CEIL=K['ceiling']; FLOOR=K['floor']; LOSS=K['loss_counties']; T=PO['totals']
LABEL="**PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).**"
BANNER=f"> {LABEL} **{S}2026 figures are unofficial.** Governor race only; these pages measure a pattern and make no claim about intent, fraud or cause."
PX="PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration)."
TNOTE=f"*{PX}*"
def REL(here):
    L=[("Home","Home"),("Bottom-Up Reverse Math","Reverse-Math"),("Locked South Carolina Formula","Locked-South-Carolina-Formula"),("Floor and Ceiling Counties","Floor-and-Ceiling"),("Graphs","Graphs")]
    return "\n---\n**Related:** "+" · ".join(f"[{a}]({b})" for a,b in L if b!=here)+f" · [Cedar County Audit (Nebraska)]({CEDAR})\n"
img=lambda fn,cap:f"![{cap}]({RAW}{fn})\n\n*{cap}*\n"
a=o.loc['Allendale']; six=o.head(6)
nA=C['total_comparisons']; mA=C['matched']; used=46*17
def tab(head,rows):
    return "| "+" | ".join(head)+" |\n|"+"---|"*len(head)+"\n"+"".join("| "+" | ".join(str(x) for x in r)+" |\n" for r in rows)
# ======================= HOME =======================
home=f"""# South Carolina 2022 vs 2026 Governor Race: ΔG Method

{BANNER}

Method developed by Morissa Benson (CD3 Vice Chair, Nebraska GOP), from her [Cedar County Audit]({CEDAR}) on the [Nebraska Election Analysis wiki](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki). Same arithmetic, all 46 South Carolina counties, with one substitution: South Carolina has no party registration, so the Democratic primary-ballot share stands in for registration share. Data: South Carolina Election Commission (SEC) results files; population from the Census Bureau. Compiled Nov 19, 2026. Code and data: [{REPO.split('/')[-1]}]({REPO}).

## Contents

Start with the Cedar County audit in Nebraska, where the method began.

1. [Cedar County Audit]({CEDAR}) (Nebraska wiki): where the method started
2. [Floor and Ceiling Counties](Floor-and-Ceiling): floor and ceiling counties, regional constants, narrowed-out counties, over-ballot check
3. [Bottom-Up Reverse Math](Reverse-Math): Allendale → the six largest counties → all 46 counties, solved backward for implied extra votes
4. [Locked South Carolina Formula](Locked-South-Carolina-Formula): the equation, the proxy, a blank template, the SC-only constants
5. [Graphs](Graphs): eight charts

## Statewide at a glance

{TNOTE}

""" + tab(["Measure","2022",f"2026{S}","Change"],[
 ["Democratic governor-primary votes (June)",f(T['prim_dem_2022']),f(T['prim_dem_2026']),sgi(T['prim_dem_2026']-T['prim_dem_2022'])],
 ["Republican governor-primary votes (June)",f(T['prim_rep_2022']),f(T['prim_rep_2026']),sgi(T['prim_rep_2026']-T['prim_rep_2022'])],
 ["**P**, proxy Dem share of primary votes",pc(PO['P22']),pc(PO['P26']),f"{sg(PO['dP'])} pts"],
 ["Democratic governor votes",f(T['dem_2022']),f(T['dem_2026'])+S,sgi(T['dem_2026']-T['dem_2022'])+S],
 ["Total ballots cast",f(T['ballots_2022']),f(T['ballots_2026'])+S,sgi(T['ballots_2026']-T['ballots_2022'])+S],
 ["**S**, Dem share of ballots",pc(PO['S22']),pc(PO['S26'])+S,f"{sg(PO['dS'])} pts{S}"],
 ["**G** = S − P",sg(PO['G22']),sg(PO['G26'])+S,f"ΔG {sg(PO['dG'])}{S}"]]) + f"""
- **S rose in all 46 counties** (ΔS {sg(o.dS.min())} Charleston to {sg(o.dS.max())} Chester, median {sg(o.dS.median())}{S}). Democratic governor votes and ballots rose in every county.
- **The proxy moved far more than S.** P rose in {46-K['n_P_fell']} counties and fell in {K['n_P_fell']} ({sg(o.dP.min())} Lee to {sg(o.dP.max())} Kershaw). Democratic primary votes rose +{(T['prim_dem_2026']/T['prim_dem_2022']-1)*100:.0f}%, Republican +{(T['prim_rep_2026']/T['prim_rep_2022']-1)*100:.0f}%.
- **ΔG is almost entirely the proxy change:** ΔG = {F['dG_on_dP']['m']/100:.3f} × ΔP + {F['dG_on_dP']['b']:.2f}{S} (R² {F['dG_on_dP']['r2']:.2f}). ΔG rose in {K['n_pos']} counties and fell in {K['n_neg']}; median {sg(K['median_dG'])}{S} (range {sg(o.dG.min())} Kershaw to {sg(o.dG.max())} Allendale).
- **Ceiling:** {', '.join(f"{c} {sg(o.loc[c,'dG'])}{S}" for c in CEIL)}. **Floor** (lowest 2022 P): {', '.join(f"{c} {p2(o.loc[c,'P22'])}%" for c in FLOOR)}. Details: [Floor and Ceiling Counties](Floor-and-Ceiling).
- **Residual step** (Democratic primary votes fell): {', '.join(f"{c} {sg(o.loc[c,'residual'])}{S}" for c in LOSS)}. The other {46-K['n_loss']} counties get raw numbers only.
- **Implied extra votes (hypothesis):** {f(PO['implied_extra_sum'])}{S} summed over counties, {f(PO['implied_extra_pooled'])}{S} pooled. No offset need, because P rose statewide. Details: [Bottom-Up Reverse Math](Reverse-Math).
- **SC-only constants** (G = m × P/100 + b): 2022 m = {F['2022']['m']:.2f}, b = {F['2022']['b']:+.2f} (R² {F['2022']['r2']:.2f}); 2026{S} m = {F['2026']['m']:.2f}, b = {F['2026']['b']:+.2f} (R² {F['2026']['r2']:.2f}). Details: [Locked South Carolina Formula](Locked-South-Carolina-Formula).
- **Over-ballot check:** no county has Dem + Rep (or all governor votes) above ballots cast in either year. Closest: Allendale, 97 votes (2022) and 89{S} (2026).

## About the data

**The proxy.** South Carolina voters do not register by party. scvotes.gov: "South Carolina does not have registration by party. In primaries, you can vote in only one party's primary." Everywhere these pages use a registration share, it is **P** = Democratic governor-primary votes ÷ (Democratic + Republican governor-primary votes) in that year's June statewide primary. Morissa chose this proxy on Nov 19, 2026. The full definition and denominator choice are on [Locked South Carolina Formula](Locked-South-Carolina-Formula#the-proxy-p).

**Sources and versions.** {S}2026 figures are unofficial and are marked {S}. They come from SEC results-site election 127300, version 386661 (timestamp 11/10/2026 5:20 PM EST). 2022 figures come from election 115412, version 313728. Primaries come from elections 114143 (2022) and 126294 (2026). Population (sort order only) is from the Census Bureau's Vintage 2025 estimates. Every source URL is listed on [Floor and Ceiling Counties](Floor-and-Ceiling#data-sources).

**Read this before using the numbers.**
- **The proxy is not registration.** South Carolina primaries are open, and a competitive race pulls voters into one party's primary. In 2022 the incumbent won the Republican primary with 83.3%, while five candidates contested the Democratic primary. In 2026 the seat was open, with seven names on the Republican ballot and three on the Democratic. P swings of 10 to 27 points are proxy behavior, not re-registration.
- **Lee and Allendale are ceiling counties because P fell 17.7 and 17.6 points.** Their ΔS (Lee {sg(o.loc['Lee','dS'])}{S}, Allendale {sg(o.loc['Allendale','dS'])}{S}) is close to the state median ({sg(o.dS.median())}{S}).
- **A residual is not evidence of altered votes.** Candidate choice, crossover voting, turnout and primary competitiveness all move these numbers.

## Verification

Two independent passes ran over the raw SEC files for 4 elections (2022 and 2026 general, 2022 and 2026 primary):

- **Pass A** read the SEC state-level `detail.xml` files with an XML parser.
- **Pass B** used separate code on each county's own SEC results files. Votes came from `summary.csv`. Registered voters and ballots came from the county `detail.xml` turnout element, read with regex. Pass B fell back to `detail.txt` for Clarendon (2022 general) and Abbeville (2022 primary), and to `detail.xml` for Lee (2026 primary).

| Result | Count |
|---|---|
| Figure comparisons (46 counties × 18 figures) | {nA} |
| Matched | {mA} |
| Mismatched | {nA-mA} |
| Figures used in a calculation, matched | {used} of {used} |

The one mismatch is Clarendon's 2022 registered voters, a figure no calculation uses. The SEC state files (`detail.xml` and `status.json`) read 22,043. The county site reads 21,942 in version 319025 and 0 in version 313514. These pages use the state-file figure.

Other quirks in the raw files:
- The 2022 state `detail.xml` header lists 3,379,089 registered voters, but its county rows add up to 3,379,129.
- The 2026 state `summary.csv` lists 72 as "ballots cast" on one governor row, where the other rows read 2,054,835.
- Kershaw's county `summary.csv` lists 0 ballots cast, so Pass B took Kershaw's ballots from its `detail.xml`: 22,600 and 26,092, matching Pass A.
{REL('Home')}"""
# ======================= LOCKED =======================
fitrows=[('2022','2022, all counties'),('2026',f'2026{S}, all counties'),('2022_narrowed','2022, narrowed'),('2026_narrowed',f'2026{S}, narrowed'),('2022_wtd','2022, ballot-weighted'),('2026_wtd',f'2026{S}, ballot-weighted'),('pooled',f'2022 + 2026{S} pooled')]
yi=F['year_interaction']; d=F['dG_on_dP']
lock=f"""# Locked South Carolina Formula

{BANNER}

## The equation

- **S** (Democratic vote share) = Democratic governor votes ÷ total ballots cast (SEC county turnout) × 100
- **P** (proxy for Democratic registration share) = Democratic governor-primary votes ÷ (Democratic + Republican governor-primary votes) × 100, same year's June primary
- **G** = S − P
- **ΔG** = G(2026) − G(2022) = (S2026 − S2022) − (P2026 − P2022)
- **Reverse step (residual)**, only where Democratic primary votes fell: residual = ΔG − absolute ΔP
- **Implied extra votes** (solved backward) = D2026 − (S2022 ÷ 100) × ballots2026
- **Primary-scaled gap** (Nebraska's "gap in votes", for comparison) = D2026 − D2022 × (DemPrimary2026 ÷ DemPrimary2022)

## The proxy P

{LABEL} South Carolina voters do not register by party (scvotes.gov). P is the Democratic share of the two-party governor-primary vote in each year's June statewide primary.

**Why governor-primary votes.** The SEC primary files give one combined ballots-cast figure per county for both parties' primaries, not ballots by party. So the per-party counts come from the governor primary race, which was contested in both parties in both years:
- 2022 Democratic: Boyd, Cunningham, McLeod, McMillan, Williams. 2022 Republican: McMaster, Musselwhite.
- 2026 Democratic: Johnson, McLeod, Webster. 2026 Republican: DuBose (decertified before the primary), Evette, Kimbrell, Mace, Norman, Reddy, Wilson.

**The denominator** is Dem + Rep governor-primary votes, so P is a two-party share, not a share of registered voters. These votes leave out ballots with no governor vote:

| Year | Dem + Rep governor-primary votes | Primary ballots cast | Share |
|---|---|---|---|
| 2022 | {f(T['prim_dem_2022']+T['prim_rep_2022'])} | {f(T['prim_ballots_2022'])} | {100*(T['prim_dem_2022']+T['prim_rep_2022'])/T['prim_ballots_2022']:.1f}% |
| 2026 | {f(T['prim_dem_2026']+T['prim_rep_2026'])} | {f(T['prim_ballots_2026'])} | {100*(T['prim_dem_2026']+T['prim_rep_2026'])/T['prim_ballots_2026']:.1f}% |

Only the first primary round is used. Runoffs are not.

## Blank template

{TNOTE}

| Line | Item | 2022 | 2026{S} |
|---|---|---|---|
| 1 | Democratic governor votes | ______ | ______ |
| 2 | Total ballots cast | ______ | ______ |
| 3 | S = line 1 ÷ line 2 × 100 | ______ | ______ |
| 4 | Dem governor-primary votes [PROXY] | ______ | ______ |
| 5 | Dem + Rep governor-primary votes [PROXY] | ______ | ______ |
| 6 | P = line 4 ÷ line 5 × 100 [PROXY] | ______ | ______ |
| 7 | G = line 3 − line 6 | ______ | ______ |
| 8 | ΔG = G 2026 − G 2022 | | ______ |
| 9 | Proxy-share change ΔP = P 2026 − P 2022 | | ______ |
| 10 | Dem primary votes fell? (line 4: 2026 < 2022) | | Yes / No |
| 11 | If yes: residual = line 8 − absolute line 9 | | ______ |
| 12 | Implied extra votes | | ______ |
| 13 | Primary-scaled gap | | ______ |
| 14 | Fitted G = m × (line 6 ÷ 100) + b | ______ | ______ |
| 15 | Distance from the SC line = line 7 − line 14 | ______ | ______ |

How to fill in lines 12 and 13:
- **Line 12:** line 1 (2026) − line 3 (2022) ÷ 100 × line 2 (2026).
- **Line 13:** line 1 (2026) − line 1 (2022) × (line 4 2026 ÷ line 4 2022).

## Worked example: Allendale

Allendale is the ceiling county, and it lost Democratic primary voters. {TNOTE}

| Line | Item | 2022 | 2026{S} |
|---|---|---|---|
| 1 | Democratic governor votes | {f(a.dem_2022)} | {f(a.dem_2026)} |
| 2 | Total ballots cast | {f(a.ballots_2022)} | {f(a.ballots_2026)} |
| 3 | S | {p2(a.S22)} | {p2(a.S26)} |
| 4 | Dem governor-primary votes [PROXY] | {f(a.prim_dem_2022)} | {f(a.prim_dem_2026)} |
| 5 | Dem + Rep governor-primary votes [PROXY] | {f(a.prim_dem_2022+a.prim_rep_2022)} | {f(a.prim_dem_2026+a.prim_rep_2026)} |
| 6 | P [PROXY] | {p2(a.P22)} | {p2(a.P26)} |
| 7 | G | {sg(a.G22)} | {sg(a.G26)} |
| 8 | ΔG | | {sg(a.dG)} |
| 9 | ΔP | | {sg(a.dP)} |
| 10 | Primary votes fell? | | Yes |
| 11 | Residual | | {sg(a.residual)} |
| 12 | Implied extra votes | | {sgi(a.implied_extra_votes)} |
| 13 | Primary-scaled gap | | {sgi(a.gap_primary_scaled)} |
| 14 | Fitted G | {p2(a.fit22)} | {p2(a.fit26)} |
| 15 | Distance from the SC line | {sg(a.res22)} | {sg(a.res26)} |

Line 10: Democratic primary votes fell from {f(a.prim_dem_2022)} to {f(a.prim_dem_2026)}.

## SC-only constants (forward fit)

The forward surplus equation **G = m × (P ÷ 100) + b** is fit by least squares across all 46 South Carolina counties, each county weighted equally. It uses South Carolina data only; no other state's constant is reused. {TNOTE}

""" + tab(["Fit","n","m (SE)","b (SE)","R²"],[[lab,F[k]['n'],f"{F[k]['m']:.2f} ({F[k]['m_se']:.2f})",f"{F[k]['b']:+.2f} ({F[k]['b_se']:.2f})",f"{F[k]['r2']:.3f}"] for k,lab in fitrows]) + "\nFit quality:\n\n" + \
 tab(["Fit","Residual SE","Within ±1 pt","Within ±2 pts","Within ±3 pts","Median abs. residual"],[[lab,f"{F[k]['resid_se']:.2f}",f"{100*F[k]['within1']:.0f}%",f"{100*F[k]['within2']:.0f}%",f"{100*F[k]['within3']:.0f}%",f"{F[k]['med_abs']:.2f}"] for k,lab in fitrows]) + f"""
**The locked SC constants are the all-county fits: 2022 m = {F['2022']['m']:.2f}, b = {F['2022']['b']:+.2f}; 2026{S} m = {F['2026']['m']:.2f}, b = {F['2026']['b']:+.2f}.** The narrowed fits leave out {', '.join(NAR['counties'])} (see [Floor and Ceiling Counties](Floor-and-Ceiling#counties-narrowed-out-of-the-fit)) and barely move m and b.

- **The 2026{S} slope differs from 2022.** In a pooled model with year terms, the slope changes by {yi['d_slope']:+.2f} (p = {yi['p_d_slope']:.4f}). The intercept change ({yi['d_intercept']:+.2f}) is not significant (p = {yi['p_d_intercept']:.2f}).
- **What m means.** G already contains −P, so m = −100 would mean S does not move with P at all. South Carolina's m of about −60 (2022) and −43 (2026{S}) means S rises roughly 0.4 to 0.6 points per point of P. It is not an "injection multiplier."
- **The reverse-factoring constant across counties** is ΔG = {d['m']/100:.3f} × ΔP + {d['b']:.2f}{S} (intercept SE {d['b_se']:.2f}; R² {d['r2']:.3f}; residual SE {d['resid_se']:.2f}). ΔG moves almost point for point opposite ΔP. The intercept, **{d['b']:+.2f}{S} points**, is the near-uniform statewide rise in S once the proxy change is factored out.

## Rules for using this formula

1. **Always label P as a proxy.** South Carolina has no party registration.
2. **If a county lost Democratic primary voters, run the residual step.** In South Carolina that is 4 counties: {', '.join(LOSS)}. The other 42 are **non-loss counties** and get raw numbers only.
3. **The starting point is different in every state.** South Carolina's constants come from its own counties. Because P is a primary share, its G values aren't comparable with states that have party registration.
4. **Always pull out the ceiling and floor counties.** The ceiling county is Allendale ({sg(o.loc['Allendale','dG'])}{S}), and the lowest ΔG is Kershaw ({sg(o.loc['Kershaw','dG'])}{S}). The floor (most Republican baseline) is {', '.join(FLOOR)}. See [Floor and Ceiling Counties](Floor-and-Ceiling).

**Terms used in this wiki** (full definitions on [Floor and Ceiling Counties](Floor-and-Ceiling#terminology)):
- **Ceiling counties:** {', '.join(CEIL)}
- **Floor counties:** {', '.join(FLOOR)}
- **Non-loss counties:** 42 counties, raw numbers only
- **Narrowed-out counties:** {', '.join(NAR['counties'])}
{REL('Locked-South-Carolina-Formula')}"""
# ======================= REVERSE MATH =======================
def gshares(d):
    s22=100*d.dem_2022.sum()/d.ballots_2022.sum(); s26=100*d.dem_2026.sum()/d.ballots_2026.sum()
    q22=100*d.prim_dem_2022.sum()/(d.prim_dem_2022.sum()+d.prim_rep_2022.sum()); q26=100*d.prim_dem_2026.sum()/(d.prim_dem_2026.sum()+d.prim_rep_2026.sum())
    return s22,s26,q22,q26
G3=[('Six largest counties',six),('Other counties',o.iloc[6:]),('All South Carolina counties',o)]
rm=f"""# Bottom-Up Reverse Math

{BANNER}

The same arithmetic at three levels: one county, the six largest counties, then the whole state. It is then solved backward for implied extra votes. The denominator is total ballots cast. The method comes from the [Cedar County Audit]({CEDAR}) in Nebraska.

## Step 1: Allendale County (the ceiling county)

{TNOTE}

| Measure | 2022 | 2026{S} | Change |
|---|---|---|---|
| Dem governor votes | {f(a.dem_2022)} | {f(a.dem_2026)} | |
| Ballots cast | {f(a.ballots_2022)} | {f(a.ballots_2026)} | |
| S, Dem share of ballots | {p2(a.S22)}% | {p2(a.S26)}% | {sg(a.dS)} |
| Dem primary votes [PROXY] | {f(a.prim_dem_2022)} | {f(a.prim_dem_2026)} | |
| Dem + Rep primary votes [PROXY] | {f(a.prim_dem_2022+a.prim_rep_2022)} | {f(a.prim_dem_2026+a.prim_rep_2026)} | |
| P [PROXY] | {p2(a.P22)}% | {p2(a.P26)}% | {sg(a.dP)} |
| G = S − P | {sg(a.G22)} | {sg(a.G26)} | **ΔG {sg(a.dG)}** |
| Residual | | | **{sg(a.residual)}** |
| Implied extra votes | | | **{sgi(a.implied_extra_votes)}** |
| Primary-scaled gap | | | {sgi(a.gap_primary_scaled)} |

How the results rows are computed:
- **ΔG** = ΔS − ΔP = {p2(a.dS)} − ({p2(a.dP)}) = {sg(a.dG)}{S}, the largest in South Carolina.
- **Residual** = ΔG − absolute ΔP = {p2(a.dG)} − {p2(abs(a.dP))} = {sg(a.residual)}{S}. Allendale runs this step because its Democratic primary votes fell (1,204 → 802).
- **Implied extra votes** = {f(a.dem_2026)} − {p2(a.S22)}% × {f(a.ballots_2026)} ≈ {sgi(a.implied_extra_votes)}{S}.
- **Primary-scaled gap** (Nebraska's "gap in votes", for comparison) = {f(a.dem_2026)} − {f(a.dem_2022)} × ({f(a.prim_dem_2026)} ÷ {f(a.prim_dem_2022)}) ≈ {sgi(a.gap_primary_scaled)}{S}.

Allendale's ΔG is large because its proxy share fell 17.6 points: Democratic primary votes fell while Republican primary votes rose. Its residual ({sg(a.residual)}{S}) is close to the state's typical ΔS (median {sg(o.dS.median())}{S}).

## Step 2: the six largest counties

Largest to smallest population. Inputs:

""" + tab(["County","Population",f"Dem gov 2022",f"Dem gov 2026{S}","Ballots 2022",f"Ballots 2026{S}"],[[c,f(r.pop2025),f(r.dem_2022),f(r.dem_2026),f(r.ballots_2022),f(r.ballots_2026)] for c,r in six.iterrows()]) + f"""
Proxy inputs. {TNOTE}

""" + tab(["County","Dem primary 2022","Dem primary 2026","P 2022","P 2026"],[[c,f(r.prim_dem_2022),f(r.prim_dem_2026),pc(r.P22),pc(r.P26)] for c,r in six.iterrows()]) + f"""
Results (points, except votes). {TNOTE}

""" + tab(["County",f"ΔS{S}","ΔP [PROXY]",f"ΔG{S}",f"Implied extra votes{S}"],[[c,sg(r.dS),sg(r.dP),sg(r.dG),sgi(r.implied_extra_votes)] for c,r in six.iterrows()]) + f"""
ΔG is negative in 5 of the six largest counties; the exception is Richland ({sg(o.loc['Richland','dG'])}{S}). All six are non-loss counties: Democratic primary votes rose in each, so none runs the residual step. Charleston's Democratic share of ballots barely moved ({p2(o.loc['Charleston','S22'])}% → {p2(o.loc['Charleston','S26'])}%{S}).

## Step 3: all 46 counties

Shares by group. {TNOTE}

""" + tab(["Group","Counties","S 2022",f"S 2026{S}","P 2022","P 2026"],[[g,len(dd)]+[pc(v) for v in gshares(dd)] for g,dd in G3]) + f"\nChanges by group. {TNOTE}\n\n" + \
 tab(["Group",f"ΔS{S}","ΔP",f"Pooled ΔG{S}",f"Median ΔG{S}",f"ΔG range{S}",f"Implied extra votes{S}"],
     [[g,sg(gshares(dd)[1]-gshares(dd)[0]),sg(gshares(dd)[3]-gshares(dd)[2]),sg((gshares(dd)[1]-gshares(dd)[3])-(gshares(dd)[0]-gshares(dd)[2])),sg(dd.dG.median()),f"{sg(dd.dG.min())} to {sg(dd.dG.max())}",sgi(dd.implied_extra_votes.sum())] for g,dd in G3]) + f"""
- ΔG rose in {K['n_pos']} of 46 counties and fell in {K['n_neg']}. The county-level SD of ΔG is {K['sd_dG']:.2f} points, against {o.dS.std():.2f} for ΔS.
- **County size.** Smaller counties have higher ΔG: r = {K['size_slope']['r']:.2f} against log population (p < 0.0001). This comes from the proxy, not the vote: ΔP rises with county size (r = +0.60), while ΔS does not track size (r = −0.16, p = 0.27).

## Residual step: the four counties that lost Democratic primary voters

{TNOTE}

""" + tab(["County","Dem primary 2022","Dem primary 2026","ΔP",f"ΔG{S}",f"Residual{S}",f"Implied extra votes{S}"],[[c,f(r.prim_dem_2022),f(r.prim_dem_2026),sg(r.dP),sg(r.dG),sg(r.residual),sgi(r.implied_extra_votes)] for c,r in o[o.loss].iterrows()]) + f"""
Residual = ΔG − absolute ΔP. All four also lost primary *share*, so each residual equals that county's ΔS. The other 42 counties are **non-loss counties** (Democratic primary votes rose) and get raw numbers only.

## Solving backward: implied extra votes (hypothesis)

For each county, implied extra votes = 2026 Democratic votes − (2022 Democratic share of ballots × 2026 ballots). That is how many more Democratic votes the county cast than its 2022 share would give on 2026 turnout.

| Measure | Votes{S} |
|---|---|
| Sum of the 46 county figures | {f(PO['implied_extra_sum'])} |
| Statewide, pooled | {f(PO['implied_extra_pooled'])} |
| Raw rise in Democratic votes | +{f(T['dem_2026']-T['dem_2022'])} |
| Offset need for a proxy-share decline | None |

How to read the table:
- **Pooled** = ({p2(PO['S26'])}% − {p2(PO['S22'])}%) × {f(T['ballots_2026'])} 2026 ballots.
- **Raw rise** = the {f(PO['implied_extra_pooled'])} share gain plus {f(T['dem_2026']-T['dem_2022']-PO['implied_extra_pooled'])} from more ballots at the 2022 share.
- **No offset need:** the statewide proxy share **rose** {sg(PO['dP'])} points ({p2(PO['P22'])}% → {p2(PO['P26'])}%), so there is no decline to offset.

> **Hypothesis label.** Calling the residual "implied extra votes," and calling those votes injected, switched or offset, is a hypothesis the arithmetic cannot test. The same number reflects candidate choice, crossover voting, turnout changes and any other cause. In South Carolina the proxy itself swings with primary competitiveness.

## What the arithmetic cannot tell you

- **The swing in S was near-uniform.** ΔS is positive in all 46 counties, and {int(((o.dS-o.dS.median()).abs()<=3).sum())} of 46 are within 3 points of the median ({sg(o.dS.median())}{S}).
- **ΔG mostly reflects the proxy.** Regressing ΔG on ΔP gives R² {F['dG_on_dP']['r2']:.2f}. The counties at the top and bottom of ΔG are the ones whose primary mix shifted most, not the ones whose general-election vote moved most.

{img('SC_DeltaG_Components_dS_vs_dP_by_Population.png','ΔS (blue), −ΔP (orange) and ΔG (black tick) for all 46 counties, largest to smallest population. 2026 unofficial.')}
## Full county table (46 counties, largest to smallest population)

{TNOTE} † = lost Democratic primary voters (residual step applies). Every figure here matched in both verification passes. CSV: [SC_Governor_2022_2026_DeltaG_by_County.csv]({REPO}/blob/main/data/SC_Governor_2022_2026_DeltaG_by_County.csv).

### 2022 inputs

""" + tab(["County","Region","Population","Dem primary","Rep primary","Dem gov","Ballots"],[[c+('†' if r.loss else ''),r.region,f(r.pop2025),f(r.prim_dem_2022),f(r.prim_rep_2022),f(r.dem_2022),f(r.ballots_2022)] for c,r in o.iterrows()]) + f"""
### 2026{S} inputs

""" + tab(["County","Dem primary","Rep primary",f"Dem gov{S}",f"Ballots{S}"],[[c+('†' if r.loss else ''),f(r.prim_dem_2026),f(r.prim_rep_2026),f(r.dem_2026),f(r.ballots_2026)] for c,r in o.iterrows()]) + f"""
### Shares and ΔG

S and P in %; G and ΔG in points. {TNOTE}

""" + tab(["County","S 2022","P 2022","G 2022",f"S 2026{S}","P 2026",f"G 2026{S}",f"ΔG{S}"],[[c+('†' if r.loss else ''),p2(r.S22),p2(r.P22),sg(r.G22),p2(r.S26),p2(r.P26),sg(r.G26),sg(r.dG)] for c,r in o.iterrows()]) + REL('Reverse-Math')
# ======================= FLOOR & CEILING =======================
rows=[c for c in o.index if c in CEIL or c in FLOOR]; grp=lambda c:'Ceiling' if c in CEIL else 'Floor'
rz=lambda c,t:o.loc[c,'res'+t]
fc=f"""# Floor and Ceiling Counties

{BANNER}

## How to read floor and ceiling counties

Look for the pattern at both ends. The ceiling counties have the highest ΔG. The floor counties are the most Republican baseline, where there were the fewest Democrats to move.

- **The ceiling:** **Allendale**, the county with the highest ΔG ({sg(o.loc['Allendale','dG'])}{S}).
- **The floor by ΔG:** **Kershaw**, the county with the lowest ΔG ({sg(o.loc['Kershaw','dG'])}{S}). Its Democratic primary votes more than tripled (1,716 → 5,387), so its proxy share rose {sg(o.loc['Kershaw','dP'])} points.

## Terminology

- **Ceiling counties** are the five largest ΔG: {', '.join(f"{c} {sg(o.loc[c,'dG'])}{S}" for c in CEIL)}. All five are small counties with a high 2022 proxy share (P 59.9% to 97.0%), and P fell in all five: {', '.join(f"{c} {sg(o.loc[c,'dP'])}" for c in CEIL)}. Their ΔS ({', '.join(f"{sg(o.loc[c,'dS'])}" for c in CEIL)}{S}) is close to the state median ({sg(o.dS.median())}{S}). Allendale and Lee also lost Democratic primary voters, so they run the residual step.
- **Floor counties** are the most Republican baseline, the five lowest 2022 proxy shares: {', '.join(f"{c} {p2(o.loc[c,'P22'])}% (ΔG {sg(o.loc[c,'dG'])}{S})" for c in FLOOR)}. All five are Upstate counties except Horry.
  - By 2022 Democratic share of ballots instead, the five lowest are {', '.join(K['lowest5_S22'])}.
  - By ΔG, the five lowest are {', '.join(K['lowest5_dG'])}. Horry is both a floor county and one of the five lowest ΔG.
- **Non-loss counties** had no drop in Democratic primary votes: 42 of 46. They get raw numbers only, with no residual step.
- **Loss counties** run the residual step: {', '.join(LOSS)}.
- **Narrowed-out counties** distort the forward fit: {', '.join(NAR['counties'])}. See below.

## Ceiling and floor detail

Largest to smallest population. {TNOTE}

""" + tab(["County","Group","Region","Population","Dem primary 2022","Dem primary 2026"],[[c,grp(c),o.loc[c,'region'],f(o.loc[c,'pop2025']),f(o.loc[c,'prim_dem_2022']),f(o.loc[c,'prim_dem_2026'])] for c in rows]) + f"\nShares (%), G and ΔG (points), and implied extra votes. {TNOTE}\n\n" + \
 tab(["County","P 2022","P 2026","S 2022",f"S 2026{S}","G 2022",f"G 2026{S}"],[[c,p2(o.loc[c,'P22']),p2(o.loc[c,'P26']),p2(o.loc[c,'S22']),p2(o.loc[c,'S26']),sg(o.loc[c,'G22']),sg(o.loc[c,'G26'])] for c in rows]) + "\n" + \
 tab(["County","Group",f"ΔG{S}",f"Implied extra votes{S}"],[[c,grp(c),sg(o.loc[c,'dG']),sgi(o.loc[c,'implied_extra_votes'])] for c in rows]) + f"""
## Regional constants

Regions are built from South Carolina's ten Councils of Governments ([SC Association of Counties](https://www.sccounties.org/councils-governments)):
- **Upstate:** Appalachian, Upper Savannah, Catawba
- **Midlands:** Central Midlands, Santee-Lynches, Lower Savannah
- **Pee Dee:** Pee Dee, Waccamaw
- **Lowcountry:** Berkeley-Charleston-Dorchester, Lowcountry

The COG membership is official; the four-way grouping is this analysis's choice. Fits of G = m × P/100 + b. {TNOTE}

""" + tab(["Region","n","2022 m","2022 b","2022 R²"],[[g,RG['22']['per_region'][g]['n'],f"{RG['22']['per_region'][g]['m']:.2f}",f"{RG['22']['per_region'][g]['b']:+.2f}",f"{RG['22']['per_region'][g]['r2']:.2f}"] for g in ['Upstate','Midlands','Pee Dee','Lowcountry']]+[["**Statewide**",46,f"{F['2022']['m']:.2f}",f"{F['2022']['b']:+.2f}",f"{F['2022']['r2']:.2f}"]]) + "\n" + \
 tab(["Region",f"2026{S} m",f"2026{S} b",f"2026{S} R²",f"Median ΔG{S}",f"ΔG range{S}"],[[g,f"{RG['26']['per_region'][g]['m']:.2f}",f"{RG['26']['per_region'][g]['b']:+.2f}",f"{RG['26']['per_region'][g]['r2']:.2f}",sg(RG['dG_by_region'][g]['median']),f"{sg(RG['dG_by_region'][g]['min'])} to {sg(RG['dG_by_region'][g]['max'])}"] for g in ['Upstate','Midlands','Pee Dee','Lowcountry']]+[["**Statewide**",f"{F['2026']['m']:.2f}",f"{F['2026']['b']:+.2f}",f"{F['2026']['r2']:.2f}",sg(K['median_dG']),f"{sg(o.dG.min())} to {sg(o.dG.max())}"]]) + f"""
- **2022: regional constants are supported.** Separate regional lines fit better than one statewide line (F test p = {RG['22']['p_full']:.4f}; regional intercepts alone p = {RG['22']['p_intercepts']:.4f}). This holds after narrowing (p = {RG['22']['p_full_narrowed']:.4f}). The Lowcountry line is the steepest.
- **2026{S}: not robust.** The full regional model is significant on all 46 counties (p = {RG['26']['p_full']:.5f}), but it rests on Hampton. With the narrowed-out counties removed, p = {RG['26']['p_full_narrowed']:.2f}. Regional intercepts alone are not significant (p = {RG['26']['p_intercepts']:.2f}).
- **ΔG by region** differs only weakly (Kruskal-Wallis p = {RG['dG_kruskal']['p']:.3f}). The Midlands has the highest median ΔG, driven by Allendale, Lee, Barnwell and Bamberg.

## Counties narrowed out of the fit

Rule: {NAR['rule'].replace('|externally studentized residual|','absolute externally studentized residual')}.

""" + tab(["County","Region","Cook's D 2022",f"Cook's D 2026{S}","Stud. resid. 2022",f"Stud. resid. 2026{S}"],[[c,o.loc[c,'region'],f"{dd['cooks22']:.3f}",f"{dd['cooks26']:.3f}",f"{dd['stud22']:+.2f}",f"{dd['stud26']:+.2f}"] for c,dd in NAR['detail'].items()]) + f"\n{TNOTE}\n\n" + \
 tab(["County","P 2022","P 2026","G 2022",f"G 2026{S}"],[[c,f"{dd['P22']:.1f}%",f"{dd['P26']:.1f}%",sg(dd['G22']),sg(dd['G26'])] for c,dd in NAR['detail'].items()]) + f"""
Why each county distorts the fit:
- **Allendale:** highest 2022 proxy share (97%), which gives it high leverage. It sits {rz('Allendale','26'):.1f} points above the 2026{S} line.
- **Charleston:** {rz('Charleston','22'):.1f} points above the 2022 line.
- **Hampton:** proxy share near 90% in both years. It sits {abs(rz('Hampton','26')):.1f} points below the 2026{S} line, the largest miss in either year.
- **Richland:** highest 2022 Democratic share of ballots ({o.loc['Richland','S22']:.1f}%). It sits {rz('Richland','22'):.1f} points above the 2022 line and {rz('Richland','26'):.1f} above the 2026{S} line.

Narrowing barely changes the statewide constants:
- 2022: m {F['2022']['m']:.2f}, b {F['2022']['b']:+.2f} → m {F['2022_narrowed']['m']:.2f}, b {F['2022_narrowed']['b']:+.2f}
- 2026{S}: m {F['2026']['m']:.2f}, b {F['2026']['b']:+.2f} → m {F['2026_narrowed']['m']:.2f}, b {F['2026_narrowed']['b']:+.2f}
- 2026{S} residual SE: {F['2026']['resid_se']:.2f} → {F['2026_narrowed']['resid_se']:.2f}

The narrowed counties stay in every table. They are left out only of the narrowed fits.

## Over-ballot check (Texas-style)

| Check (counties) | 2022 | 2026{S} |
|---|---|---|
| Dem + Rep governor votes > ballots cast | {len(TX['2022']['DR_gt_ballots'])} | {len(TX['2026']['DR_gt_ballots'])} |
| All governor votes > ballots cast | {len(TX['2022']['gov_gt_ballots'])} | {len(TX['2026']['gov_gt_ballots'])} |
| Ballots cast > registered voters | {len(TX['2022']['ballots_gt_reg'])} | {len(TX['2026']['ballots_gt_reg'])} |
| Primary: Dem + Rep governor votes > primary ballots | {len(TX['2022']['primary_DR_gt_primary_ballots'])} | {len(TX['2026']['primary_DR_gt_primary_ballots'])} |
| Smallest margin, ballots − (Dem + Rep) | {TX['2022']['min_margin_ballots_minus_DR']['county']} {TX['2022']['min_margin_ballots_minus_DR']['votes']} | {TX['2026']['min_margin_ballots_minus_DR']['county']} {TX['2026']['min_margin_ballots_minus_DR']['votes']} |
| Smallest margin, ballots − all governor votes | {TX['2022']['min_margin_ballots_minus_gov']['county']} {TX['2022']['min_margin_ballots_minus_gov']['votes']} | {TX['2026']['min_margin_ballots_minus_gov']['county']} {TX['2026']['min_margin_ballots_minus_gov']['votes']} |
| Ballots with no governor vote, county median | {TX['2022']['nogov_pct_median']:.2f}% | {TX['2026']['nogov_pct_median']:.2f}% |
| Ballots with no governor vote, county range | {TX['2022']['nogov_pct_range'][0]:.2f}–{TX['2022']['nogov_pct_range'][1]:.2f}% | {TX['2026']['nogov_pct_range'][0]:.2f}–{TX['2026']['nogov_pct_range'][1]:.2f}% |

**No over-ballot anomalies in South Carolina in either year.** The margins are in votes.

## Data sources

- **2022 general election:** SEC results site, election 115412, version 313728. [enr-scvotes.org/SC/115412](https://www.enr-scvotes.org/SC/115412/)
- **2026{S} general election (unofficial in this wiki):** SEC results site, election 127300, version 386661, timestamp 11/10/2026 5:20 PM EST. [enr-scvotes.org/SC/127300](https://www.enr-scvotes.org/SC/127300/)
- **2022 June statewide primaries:** election 114143, version 297344. [enr-scvotes.org/SC/114143](https://www.enr-scvotes.org/SC/114143/)
- **2026 June statewide primaries:** election 126294, version 375593. [enr-scvotes.org/SC/126294](https://www.enr-scvotes.org/SC/126294/)
- **County results sites (Pass B):** the 46 county sites listed in each election's settings file. See `raw/county_sites_download_log.json` in the [repo]({REPO}).
- **No party registration:** [scvotes.gov Register to Vote](https://scvotes.gov/voters/register-to-vote/)
- **County population, July 1, 2025 (sort order only):** [Census Vintage 2025 estimates](https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv)
- **Regions:** [SC Councils of Governments membership](https://www.sccounties.org/councils-governments)
{REL('Floor-and-Ceiling')}"""
# ======================= GRAPHS =======================
gr=f"""# Graphs

{BANNER}

Every chart carries the proxy label and the source in its footer. Bars run left to right from the largest county to the smallest (Census Vintage 2025). 2026 values in every chart are unofficial.

## 1. Slope chart: G, 2022 → 2026{S}
{img('SC_Slope_G2022_to_G2026.png','County G (S − P), 2022 → 2026 (unofficial). Red = ceiling counties; blue = floor counties.')}
## 2. ΔG by county, population order
{img('SC_DeltaG_by_Population.png','ΔG for all 46 counties, largest to smallest population, with the ceiling and floor counties marked.')}
## 3. What ΔG is made of: ΔS vs ΔP
{img('SC_DeltaG_Components_dS_vs_dP_by_Population.png','ΔS (change in Democratic share of ballots) and −ΔP (minus the change in the proxy) for each county. ΔG = ΔS − ΔP.')}
## 4. Democratic share of ballots and the proxy
{img('SC_Stacked_Share_and_Proxy_by_Population.png','Bars: Democratic share of ballots, with the 2026 gain stacked on top. Markers: proxy P in 2022 and 2026.')}
## 5. Forward fit: SC-only constants
{img('SC_Forward_Fit_G_vs_P_2022_2026.png','G vs P, 2022 and 2026, with the all-county and narrowed least-squares lines. Black outline = narrowed-out counties.')}
## 6. ΔG vs ΔP
{img('SC_DeltaG_vs_DeltaP_Scatter.png','ΔG against the proxy change ΔP. A slope near −1 means ΔG is almost entirely the proxy change; the intercept (+7.07) is the near-uniform rise in S.')}
## 7. Regional constants
{img('SC_Regional_Fits.png','Separate fits for Upstate, Midlands, Pee Dee and Lowcountry, 2022 (top) and 2026 (bottom), against the statewide line.')}
## 8. Over-ballot check
{img('SC_Overballot_Check_by_Population.png','Ballots cast minus (Democratic + Republican governor votes), as a share of ballots. No county is below zero in either year.')}

## Data behind the charts

- County table: [SC_Governor_2022_2026_DeltaG_by_County.csv]({REPO}/blob/main/data/SC_Governor_2022_2026_DeltaG_by_County.csv)
- Fits, regional tests, over-ballot checks: [SC_results_summary.json]({REPO}/blob/main/data/SC_results_summary.json)
- Verification, both passes, figure by figure: [verification/]({REPO}/tree/main/verification)
{REL('Graphs')}"""
side=f"""**South Carolina Election Analysis**

1. [Home](Home)
2. [Cedar County Audit (Nebraska wiki)]({CEDAR})
3. [Floor and Ceiling Counties](Floor-and-Ceiling)
4. [Bottom-Up Reverse Math](Reverse-Math)
5. [Locked South Carolina Formula](Locked-South-Carolina-Formula)
6. [Graphs](Graphs)

*PROXY: Democratic primary-ballot share, not official party registration. \\*2026 figures are unofficial.*
"""
for name,txt in (('Home',home),('Locked-South-Carolina-Formula',lock),('Reverse-Math',rm),('Floor-and-Ceiling',fc),('Graphs',gr),('_Sidebar',side)):
    txt=re.sub(r'(?<![\w/.\-])-(\d)',r'−\1',txt); open(WK+name+'.md','w').write(txt)
print('built')

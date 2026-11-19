import pandas as pd, numpy as np, json
W='/workspace/south-carolina-elections/'; O=W+'repo/'; WK=W+'wiki/'
o=pd.read_pickle('/tmp/sc_o.pkl'); J=json.load(open(O+'data/SC_results_summary.json')); C=json.load(open(W+'verification/compare_report.json'))
RAW='https://raw.githubusercontent.com/mbenson8989/South-Carolina-Election-Analysis/main/'
REPO='https://github.com/mbenson8989/South-Carolina-Election-Analysis'
CEDAR='https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit'
f=lambda n:f"{int(round(n)):,}"; sgi=lambda n:(f"{int(round(n)):+,}").replace('-','−'); p2=lambda v:f"{v:.2f}"; sg=lambda v:(f"{v:+.2f}").replace('-','−'); pc=lambda v:f"{v:.2f}%"
F=J['fits']; K=J['K']; PO=J['pooled']; RG=J['regions']; NAR=J['narrow']; TX=J['overballot']
CEIL=K['ceiling']; FLOOR=K['floor']; LOSS=K['loss_counties']
PROXY="**PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).**"
BANNER=(f"> {PROXY} South Carolina voters do not register by party (scvotes.gov: \"South Carolina does not have registration by party. In primaries, you can vote in only one party's primary.\"). "
 "Everywhere these pages use a registration share, it is **P** = Democratic governor-primary votes ÷ (Democratic + Republican governor-primary votes) in that year's June statewide primary. "
 "**2026 status: certified, not unofficial.** The SC State Board of Canvassers certified the 2026 General Election on Nov 11, 2026, and recertified it the same day after amended Calhoun County totals. The 2026 figures are SEC results version 386661 (11/10/2026 5:20 PM EST), posted after Calhoun's amended upload (11/10/2026 5:17 PM EST). "
 "2022 figures are certified SEC results. Governor race only. Votes are votes for the Democratic candidate, not a count of Democrats. These pages measure a pattern; they make no claim about intent, fraud or cause.")
REL=lambda here:"\n---\n**Related:** "+" · ".join(x for x in [f"[Home](Home)",f"[Bottom-Up Reverse Math](Reverse-Math)",f"[Locked South Carolina Formula](Locked-South-Carolina-Formula)",f"[Floor and Ceiling Counties](Floor-and-Ceiling)",f"[Graphs](Graphs)",f"[Cedar County Audit (Nebraska)]({CEDAR})"] if f"({here})" not in x)+"\n"
img=lambda fn,cap:f"![{cap}]({RAW}{fn})\n\n*{cap}*\n"
T=PO['totals']
nA=C['total_comparisons']; mA=C['matched']; used=46*17
# ---------- per-county table ----------
def full_table():
    h="| County | Region | Population 2025 | Dem primary 2022 | Rep primary 2022 | P 2022 | Dem gov 2022 | Ballots 2022 | S 2022 | G 2022 | Dem primary 2026 | Rep primary 2026 | P 2026 | Dem gov 2026 | Ballots 2026 | S 2026 | G 2026 | ΔG |\n|"+"---|"*18+"\n"
    for c,r in o.iterrows():
        h+=f"| {c}{'†' if r.loss else ''} | {r.region} | {f(r.pop2025)} | {f(r.prim_dem_2022)} | {f(r.prim_rep_2022)} | {p2(r.P22)} | {f(r.dem_2022)} | {f(r.ballots_2022)} | {p2(r.S22)} | {sg(r.G22)} | {f(r.prim_dem_2026)} | {f(r.prim_rep_2026)} | {p2(r.P26)} | {f(r.dem_2026)} | {f(r.ballots_2026)} | {p2(r.S26)} | {sg(r.G26)} | {sg(r.dG)} |\n"
    return h
a=o.loc['Allendale']
# ================= HOME =================
six=o.head(6)
home=f"""# South Carolina 2022 vs 2026 Governor Race: ΔG Method (proxy version)

{BANNER}

Method developed by Morissa Benson (CD3 Vice Chair, Nebraska GOP). It began with her [Cedar County Audit]({CEDAR}) on the [Nebraska Election Analysis wiki](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki). That audit is where the ΔG method and the reverse step come from. This wiki applies the same arithmetic to all 46 South Carolina counties. Because South Carolina has no party registration, it uses one substitution, the primary-ballot proxy, chosen by Morissa on Nov 19, 2026. Data: South Carolina Election Commission (SEC) results files ([enr-scvotes.org](https://www.enr-scvotes.org/SC/)). Population comes from the U.S. Census Bureau. Compiled Nov 19, 2026. Code and data: [{REPO.split('/')[-1]}]({REPO}).

## Pages

1. [Cedar County Audit]({CEDAR}) (Nebraska wiki): where the method started
2. [Bottom-Up Reverse Math](Reverse-Math): Allendale → the six largest counties → all 46 counties, then solved backward for implied extra votes
3. [Locked South Carolina Formula](Locked-South-Carolina-Formula): the equation, the proxy, a blank template, and the SC-only constants
4. [Floor and Ceiling Counties](Floor-and-Ceiling): the floor and ceiling counties, regional constants, and the counties narrowed out of the fit
5. [Graphs](Graphs): slope chart, ΔG by population, the ΔS and ΔP components, forward fit, regional fits, and the over-ballot check

## Statewide at a glance

| Measure | 2022 | 2026 | Change |
|---|---|---|---|
| Democratic governor-primary votes (June) | {f(T['prim_dem_2022'])} | {f(T['prim_dem_2026'])} | {sgi(T['prim_dem_2026']-T['prim_dem_2022'])} |
| Republican governor-primary votes (June) | {f(T['prim_rep_2022'])} | {f(T['prim_rep_2026'])} | {sgi(T['prim_rep_2026']-T['prim_rep_2022'])} |
| **P** proxy: Dem share of governor-primary votes | {pc(PO['P22'])} | {pc(PO['P26'])} | {sg(PO['dP'])} pts |
| Democratic governor votes | {f(T['dem_2022'])} | {f(T['dem_2026'])} | {sgi(T['dem_2026']-T['dem_2022'])} |
| Total ballots cast | {f(T['ballots_2022'])} | {f(T['ballots_2026'])} | {sgi(T['ballots_2026']-T['ballots_2022'])} |
| **S**: Dem share of ballots cast | {pc(PO['S22'])} | {pc(PO['S26'])} | {sg(PO['dS'])} pts |
| **G** = S − P | {sg(PO['G22'])} | {sg(PO['G26'])} | ΔG {sg(PO['dG'])} |

## County results in brief

- **The Democratic share of ballots (S) rose in all 46 counties.** County ΔS ranges from {sg(o.dS.min())} (Charleston) to {sg(o.dS.max())} (Chester), with a median of {sg(o.dS.median())}. Democratic governor votes and total ballots both rose in every county.
- **The proxy moved far more than S.** The proxy P rose in {46-K['n_P_fell']} counties and fell in {K['n_P_fell']}, ranging from {sg(o.dP.min())} (Lee) to {sg(o.dP.max())} (Kershaw). Democratic primary votes roughly doubled statewide (+{(T['prim_dem_2026']/T['prim_dem_2022']-1)*100:.0f}%), while Republican primary votes rose +{(T['prim_rep_2026']/T['prim_rep_2022']-1)*100:.0f}%.
- **ΔG is almost entirely the proxy change.** Across counties, ΔG = {F['dG_on_dP']['m']/100:.3f} × ΔP + {F['dG_on_dP']['b']:.2f} (R² {F['dG_on_dP']['r2']:.2f}). ΔG rose in {K['n_pos']} counties and fell in {K['n_neg']}. The county median is {sg(K['median_dG'])} (range {sg(o.dG.min())} Kershaw to {sg(o.dG.max())} Allendale).
- **Ceiling counties** (largest ΔG): {', '.join(f"{c} ({sg(o.loc[c,'dG'])})" for c in CEIL)}. **Floor counties** (most Republican baseline, lowest 2022 proxy share): {', '.join(f"{c} ({p2(o.loc[c,'P22'])}%)" for c in FLOOR)}. See [Floor and Ceiling Counties](Floor-and-Ceiling).
- **Residual step:** only {K['n_loss']} counties lost Democratic primary voters ({', '.join(LOSS)}), so only they run the residual step. Their residuals are {', '.join(f"{c} {sg(o.loc[c,'residual'])}" for c in LOSS)}. The other {46-K['n_loss']} are non-loss counties: raw numbers only.
- **Solved backward (hypothesis):** implied extra votes sum to {f(PO['implied_extra_sum'])} across the 46 counties ({f(PO['implied_extra_pooled'])} on pooled statewide numbers). The proxy share **rose** statewide, so there is no registration-loss offset to cover. See [Bottom-Up Reverse Math](Reverse-Math).
- **SC-only constants** (G = m × P/100 + b, 46 counties): 2022 m = {F['2022']['m']:.2f}, b = {F['2022']['b']:+.2f} (R² {F['2022']['r2']:.2f}); 2026 m = {F['2026']['m']:.2f}, b = {F['2026']['b']:+.2f} (R² {F['2026']['r2']:.2f}). No other state's constant is used. See [Locked South Carolina Formula](Locked-South-Carolina-Formula).
- **Over-ballot check (Texas-style):** in both years, no county has Democratic + Republican governor votes above ballots cast, and no county has total governor votes above ballots cast. The closest margin is Allendale, with 97 votes to spare (2022) and 89 (2026).

## Verification: two independent passes over the raw SEC files

- **Pass A** parsed the SEC state-level `detail.xml` file for each of the 4 elections (2022 and 2026 general, 2022 and 2026 primary) with an XML parser.
- **Pass B** used separate code on different files: each county's own SEC results site (46 counties × 4 elections). Votes came from `summary.csv`; registered voters and ballots came from the county's `detail.xml` turnout element, read with regex. Where a county file isn't served, Pass B fell back to that county's `detail.txt` (Clarendon 2022 general, Abbeville 2022 primary) or its `detail.xml` (Lee 2026 primary).
- **Result:** {nA} figure comparisons (46 counties × 18 figures). **{mA} matched, {nA-mA} mismatched.** Every figure used in a calculation (46 × 17 = {used}) matched in both passes.
- **The one mismatch is a registered-voter count that no calculation uses.** Clarendon's 2022 registered voters read 22,043 in the SEC state files (`detail.xml` and `status.json`). The county's later results-site version (319025) reads 21,942, and its earlier version (313514) reads 0. These pages show the state-file figure.
- **Other notes on the raw files:** the 2022 state `detail.xml` header lists 3,379,089 registered voters, while its 46 county rows add up to 3,379,129 (40 more). The 2026 state `summary.csv` lists 72 as "ballots cast" on its first governor row, where every other row reads 2,054,835. Kershaw's county `summary.csv` lists 0 ballots cast, so Pass B takes Kershaw's ballots from its `detail.xml` (22,600 and 26,092, which match Pass A). Statewide 2026 ballots, 2,054,835, match the SEC certification release.

## Read this before using the numbers

- **The proxy is not registration.** Primary ballots measure which primary voters chose in one June election. South Carolina primaries are open, so a voter picks a ballot each time. A competitive race in one party pulls voters into that primary. In 2022 the incumbent governor won the Republican primary with 83.3% of the vote, while five candidates contested the Democratic primary. In 2026 the seat was open, with seven names on the Republican primary ballot and three on the Democratic. Swings in P of 10 to 27 points in a few years are proxy behavior, not voters re-registering.
- **Lee and Allendale are ceiling counties because their proxy share fell 17.7 and 17.6 points.** Their Democratic share of ballots rose about as much as the state's did (Lee {sg(o.loc['Lee','dS'])}, Allendale {sg(o.loc['Allendale','dS'])}; state median {sg(o.dS.median())}).
- **A residual is not evidence of altered votes.** Candidate choice, crossover voting, turnout and primary competitiveness all move these numbers. The arithmetic cannot separate them.
{REL('Home')}"""
open(WK+'Home.md','w').write(home)
# ================= LOCKED FORMULA =================
lock=f"""# Locked South Carolina Formula

{BANNER}

## The equation

- **S** (Democratic vote share) = Democratic governor votes ÷ total ballots cast × 100. Ballots cast is the SEC county turnout figure.
- **P** (proxy for Democratic registration share) = Democratic governor-primary votes ÷ (Democratic + Republican governor-primary votes) × 100, from the same year's June statewide primary. {PROXY}
- **G** = S − P
- **ΔG** = G(2026) − G(2022) = (S2026 − S2022) − (P2026 − P2022)
- **Reverse step (residual).** Run it only where Democratic primary votes fell. Residual = ΔG − |P2026 − P2022|: the vote-share movement left after subtracting the expected loss from the proxy-share decline.
- **Solved backward: implied extra votes** = D2026 − (S2022 ÷ 100) × ballots2026
- **Primary-scaled gap** (the Nebraska wiki's "gap in votes" line, for comparison) = D2026 − D2022 × (DemPrimary2026 ÷ DemPrimary2022)

### Why this denominator for the proxy

The SEC primary files give one ballots-cast figure per county, combining both parties' primaries. They do not give ballots by party. The per-party count therefore comes from the governor primary race, contested in both parties in both years (2022 Democratic: Boyd, Cunningham, McLeod, McMillan, Williams; 2022 Republican: McMaster, Musselwhite; 2026 Democratic: Johnson, McLeod, Webster; 2026 Republican: DuBose (decertified before the primary), Evette, Kimbrell, Mace, Norman, Reddy, Wilson).

- The denominator is Democratic + Republican governor-primary votes, so P is a two-party share. It is not a share of all registered voters.
- Governor-primary votes leave out ballots with no governor vote. Dem + Rep governor-primary votes are {f(T['prim_dem_2022']+T['prim_rep_2022'])} of {f(T['prim_ballots_2022'])} primary ballots in 2022 ({100*(T['prim_dem_2022']+T['prim_rep_2022'])/T['prim_ballots_2022']:.1f}%) and {f(T['prim_dem_2026']+T['prim_rep_2026'])} of {f(T['prim_ballots_2026'])} in 2026 ({100*(T['prim_dem_2026']+T['prim_rep_2026'])/T['prim_ballots_2026']:.1f}%).
- The runoffs (2026 Republican governor runoff) are not used. Only the first primary round is.

## Blank template

| Line | Item | 2022 | 2026 |
|---|---|---|---|
| 1 | Democratic governor votes | ______ | ______ |
| 2 | Total ballots cast (SEC county turnout) | ______ | ______ |
| 3 | S = line 1 ÷ line 2 × 100 | ______ | ______ |
| 4 | Democratic governor-primary votes (June primary) **[PROXY]** | ______ | ______ |
| 5 | Democratic + Republican governor-primary votes **[PROXY]** | ______ | ______ |
| 6 | P = line 4 ÷ line 5 × 100 **[PROXY: not party registration]** | ______ | ______ |
| 7 | G = line 3 − line 6 | ______ | ______ |
| 8 | ΔG = G 2026 − G 2022 | | ______ |
| 9 | Proxy-share change = P 2026 − P 2022 | | ______ |
| 10 | Did Democratic primary votes fall? (line 4: 2026 < 2022) | | Yes / No |
| 11 | If yes: residual = line 8 − \\|line 9\\| | | ______ |
| 12 | Implied extra votes = line 1 (2026) − line 3 (2022) ÷ 100 × line 2 (2026) | | ______ |
| 13 | Primary-scaled gap = line 1 (2026) − line 1 (2022) × (line 4 2026 ÷ line 4 2022) | | ______ |
| 14 | Fitted G for this county = m × (line 6 ÷ 100) + b, SC constants for that year | ______ | ______ |
| 15 | Distance from the SC line = line 7 − line 14 | ______ | ______ |

## Worked example: Allendale (ceiling county, lost Democratic primary voters)

| Line | Item | 2022 | 2026 |
|---|---|---|---|
| 1 | Democratic governor votes | {f(a.dem_2022)} | {f(a.dem_2026)} |
| 2 | Total ballots cast | {f(a.ballots_2022)} | {f(a.ballots_2026)} |
| 3 | S | {p2(a.S22)} | {p2(a.S26)} |
| 4 | Democratic governor-primary votes [PROXY] | {f(a.prim_dem_2022)} | {f(a.prim_dem_2026)} |
| 5 | Dem + Rep governor-primary votes [PROXY] | {f(a.prim_dem_2022+a.prim_rep_2022)} | {f(a.prim_dem_2026+a.prim_rep_2026)} |
| 6 | P [PROXY] | {p2(a.P22)} | {p2(a.P26)} |
| 7 | G | {sg(a.G22)} | {sg(a.G26)} |
| 8 | ΔG | | {sg(a.dG)} |
| 9 | Proxy-share change | | {sg(a.dP)} |
| 10 | Primary votes fell? | | Yes ({f(a.prim_dem_2022)} → {f(a.prim_dem_2026)}) |
| 11 | Residual | | {sg(a.residual)} |
| 12 | Implied extra votes | | {sgi(a.implied_extra_votes)} |
| 13 | Primary-scaled gap | | {sgi(a.gap_primary_scaled)} |
| 14 | Fitted G | {p2(a.fit22)} | {p2(a.fit26)} |
| 15 | Distance from the SC line | {sg(a.res22)} | {sg(a.res26)} |

## SC-only constants (forward fit)

The forward surplus equation is fit by least squares across all 46 South Carolina counties, each county weighted equally: **G = m × (P ÷ 100) + b**. It uses South Carolina data only. No other state's constant is reused.

| Fit | n | m (SE) | b (SE) | R² | Residual SE | Within ±1 / ±2 / ±3 pts | Median abs. residual |
|---|---|---|---|---|---|---|---|
"""
for k,lab in (('2022','2022, all counties'),('2026','2026, all counties'),('2022_narrowed','2022, narrowed'),('2026_narrowed','2026, narrowed'),('2022_wtd','2022, ballot-weighted'),('2026_wtd','2026, ballot-weighted'),('pooled','2022 + 2026 pooled')):
    x=F[k]; lock+=f"| {lab} | {x['n']} | {x['m']:.2f} ({x['m_se']:.2f}) | {x['b']:+.2f} ({x['b_se']:.2f}) | {x['r2']:.3f} | {x['resid_se']:.2f} | {100*x['within1']:.0f}% / {100*x['within2']:.0f}% / {100*x['within3']:.0f}% | {x['med_abs']:.2f} |\n"
yi=F['year_interaction']; d=F['dG_on_dP']
lock+=f"""
**The locked SC constants are the all-county fits: 2022 m = {F['2022']['m']:.2f}, b = {F['2022']['b']:+.2f}; 2026 m = {F['2026']['m']:.2f}, b = {F['2026']['b']:+.2f}.** Narrowed fits leave out {', '.join(NAR['counties'])} (see [Floor and Ceiling Counties](Floor-and-Ceiling#counties-narrowed-out-of-the-fit)) and barely move m and b.

- **The 2026 line has a different slope from the 2022 line.** In a pooled model with year terms, the slope changes by {yi['d_slope']:+.2f} (p = {yi['p_d_slope']:.4f}). The intercept change, {yi['d_intercept']:+.2f}, is not significant (p = {yi['p_d_intercept']:.2f}).
- **What m means.** G already contains −P, so m = −100 would mean S does not move with P at all. South Carolina's m of about −60 (2022) and −43 (2026) means S rises roughly 0.4 to 0.6 points for each point of proxy share. It is not an "injection multiplier."
- **Reverse-factoring constant across counties.** Regressing ΔG on ΔP gives ΔG = {d['m']/100:.3f} × ΔP + {d['b']:.2f} (SE of intercept {d['b_se']:.2f}; R² {d['r2']:.3f}; residual SE {d['resid_se']:.2f}). A slope of almost exactly −1 means ΔG moves point for point, in the opposite direction, with ΔP. The intercept, **{d['b']:+.2f} points**, is the near-uniform statewide rise in S once the proxy change is factored out. It is the single South Carolina figure closest to a "constant" in the reverse direction.

## Rules for using this formula

1. **Always label P as a proxy.** South Carolina has no party registration. Every table and chart that uses P must say so.
2. **If a county lost Democratic primary voters, run the residual step.** In South Carolina that is 4 counties ({', '.join(LOSS)}). The other 42 are **non-loss counties** and get raw numbers only.
3. **The starting point is different in every state.** South Carolina's constants come from South Carolina's own counties. Its P is a primary share, so its G values aren't comparable with states that have real party registration.
4. **Always pull out the ceiling and floor counties.** In South Carolina the ceiling county is Allendale ({sg(o.loc['Allendale','dG'])}), and the lowest ΔG is Kershaw ({sg(o.loc['Kershaw','dG'])}). The floor (most Republican baseline) is {', '.join(FLOOR)}. See [Floor and Ceiling Counties](Floor-and-Ceiling).

**Terms used in this wiki** (full definitions on [Floor and Ceiling Counties](Floor-and-Ceiling#terminology)):
- **Ceiling counties**: the five largest ΔG ({', '.join(CEIL)}).
- **Floor counties**: the most Republican baseline, the five lowest 2022 proxy shares ({', '.join(FLOOR)}).
- **Non-loss counties**: no drop in Democratic primary votes (42 counties). Raw numbers only.
- **Narrowed-out counties**: counties that distort the fit ({', '.join(NAR['counties'])}).
{REL('Locked-South-Carolina-Formula')}"""
open(WK+'Locked-South-Carolina-Formula.md','w').write(lock)
# ================= REVERSE MATH =================
def grp(d,lab):
    s22=100*d.dem_2022.sum()/d.ballots_2022.sum(); s26=100*d.dem_2026.sum()/d.ballots_2026.sum()
    q22=100*d.prim_dem_2022.sum()/(d.prim_dem_2022.sum()+d.prim_rep_2022.sum()); q26=100*d.prim_dem_2026.sum()/(d.prim_dem_2026.sum()+d.prim_rep_2026.sum())
    return f"| {lab} | {len(d)} | {p2(s22)}% → {p2(s26)}% | {p2(q22)}% → {p2(q26)}% | {sg(s26-s22)} | {sg(q26-q22)} | {sg((s26-q26)-(s22-q22))} | {sg(d.dG.median())} ({sg(d.dG.min())} to {sg(d.dG.max())}) | {sgi(d.implied_extra_votes.sum())} |\n"
rm=f"""# Bottom-Up Reverse Math

{BANNER}

The same arithmetic at three levels: one county, then the six largest, then the whole state. It is then solved backward for implied extra votes. Denominator: Democratic governor votes ÷ total ballots cast. The method comes from the [Cedar County Audit]({CEDAR}) in Nebraska.

## Step 1: Allendale County (the ceiling county)

| Step | Value |
|---|---|
| Democratic share of ballots (S) | {p2(a.S22)}% (2022: {f(a.dem_2022)} of {f(a.ballots_2022)}) → {p2(a.S26)}% (2026: {f(a.dem_2026)} of {f(a.ballots_2026)}): **{sg(a.dS)} points** |
| Proxy P [PROXY: Dem primary-ballot share] | {p2(a.P22)}% ({f(a.prim_dem_2022)} of {f(a.prim_dem_2022+a.prim_rep_2022)}) → {p2(a.P26)}% ({f(a.prim_dem_2026)} of {f(a.prim_dem_2026+a.prim_rep_2026)}): **{sg(a.dP)} points** |
| ΔG = ΔS − ΔP | {p2(a.dS)} − ({p2(a.dP)}) = **{sg(a.dG)} points**, the largest in South Carolina |
| Reverse step: ΔG − proxy-share loss | {p2(a.dG)} − {p2(abs(a.dP))} = **{sg(a.residual)}** (the residual) |
| Implied extra votes | {f(a.dem_2026)} − {p2(a.S22)}% × {f(a.ballots_2026)} = **about {sgi(a.implied_extra_votes)}** |
| Primary-scaled gap (Nebraska "gap in votes", for comparison) | {f(a.dem_2026)} − {f(a.dem_2022)} × ({f(a.prim_dem_2026)} ÷ {f(a.prim_dem_2022)}) = about {sgi(a.gap_primary_scaled)} |

Allendale's ΔG is large because its proxy share fell 17.6 points: Democratic primary votes fell from 1,204 to 802 while Republican primary votes rose. Its residual, {sg(a.residual)}, is close to the state's typical ΔS (median {sg(o.dS.median())}).

## Step 2: the six largest counties

Largest to smallest population.

| County | Population | Dem primary 2022 → 2026 [PROXY] | P 2022 → 2026 [PROXY] | Dem gov votes 2022 → 2026 | Ballots 2022 → 2026 | ΔS (pts) | ΔP (pts) | ΔG (pts) | Implied extra votes |
|---|---|---|---|---|---|---|---|---|---|
"""
for c,r in six.iterrows():
    rm+=f"| {c} | {f(r.pop2025)} | {f(r.prim_dem_2022)} → {f(r.prim_dem_2026)} | {p2(r.P22)}% → {p2(r.P26)}% | {f(r.dem_2022)} → {f(r.dem_2026)} | {f(r.ballots_2022)} → {f(r.ballots_2026)} | {sg(r.dS)} | {sg(r.dP)} | {sg(r.dG)} | {sgi(r.implied_extra_votes)} |\n"
rm+=f"""
ΔG is negative in 5 of the six largest counties. The exception is Richland, at {sg(o.loc['Richland','dG'])}. All six are non-loss counties: Democratic primary votes rose in each, so there is no residual step. Charleston's Democratic share of ballots barely moved ({p2(o.loc['Charleston','S22'])}% → {p2(o.loc['Charleston','S26'])}%).

## Step 3: all 46 counties

| Group | Counties | Dem share of ballots | Proxy P [PROXY] | ΔS | ΔP | Pooled ΔG | County median ΔG (range) | Implied extra votes |
|---|---|---|---|---|---|---|---|---|
{grp(six,'Six largest counties')}{grp(o.iloc[6:],'Other counties')}{grp(o,'All South Carolina counties')}
- ΔG rose in {K['n_pos']} of 46 counties and fell in {K['n_neg']}. The county-level SD of ΔG is {K['sd_dG']:.2f} points, against an SD of ΔS of {o.dS.std():.2f}.
- **County size.** Smaller counties have higher ΔG: r = {K['size_slope']['r']:.2f} against log population (p < 0.0001). This comes from the proxy, not the vote: ΔP rises with county size (r = +0.60), while ΔS does not track size (r = −0.16, p = 0.27).

## Residual step: the four counties that lost Democratic primary voters

| County | Population | Dem primary 2022 → 2026 [PROXY] | P change | ΔG | Residual = ΔG − \\|ΔP\\| | Implied extra votes |
|---|---|---|---|---|---|---|
"""
for c,r in o[o.loss].iterrows():
    rm+=f"| {c} | {f(r.pop2025)} | {f(r.prim_dem_2022)} → {f(r.prim_dem_2026)} | {sg(r.dP)} | {sg(r.dG)} | {sg(r.residual)} | {sgi(r.implied_extra_votes)} |\n"
rm+=f"""
Each of the four lost primary *share* too, so each one's residual equals its ΔS. The other 42 counties are **non-loss counties** (Democratic primary votes rose) and get raw numbers only.

## Solving backward: implied extra votes (hypothesis)

For each county, implied extra votes = 2026 Democratic votes − (2022 Democratic share of ballots × 2026 ballots). That is how many more Democratic votes the county cast than it would have at its 2022 share on 2026 turnout.

| Measure | Votes |
|---|---|
| Sum of the 46 county figures | {f(PO['implied_extra_sum'])} |
| Statewide, pooled: ({p2(PO['S26'])}% − {p2(PO['S22'])}%) × {f(T['ballots_2026'])} ballots | {f(PO['implied_extra_pooled'])} |
| Raw rise in Democratic votes | +{f(T['dem_2026']-T['dem_2022'])} = {f(PO['implied_extra_pooled'])} share gain + {f(T['dem_2026']-T['dem_2022']-PO['implied_extra_pooled'])} from more ballots at the 2022 share |
| Offset need for a proxy-share decline | **None.** The statewide proxy share **rose** {sg(PO['dP'])} points ({p2(PO['P22'])}% → {p2(PO['P26'])}%), so there is no registration-loss decline to offset. |

> **Hypothesis label.** Turning the residual into "implied extra votes" and calling them injected, switched or offset votes is a hypothesis the arithmetic cannot test. The same number reflects candidate choice, crossover voting, turnout changes and any other cause. In South Carolina the proxy itself swings with primary competitiveness.

## What the arithmetic cannot tell you

- **The swing in S was near-uniform.** ΔS is positive in all 46 counties, and {int(((o.dS-o.dS.median()).abs()<=3).sum())} of 46 are within 3 points of the median ({sg(o.dS.median())}).
- **ΔG mostly reflects the proxy.** ΔG on ΔP has R² {F['dG_on_dP']['r2']:.2f}. The counties at the top and bottom of ΔG are the counties whose primary mix shifted most, not the counties whose general-election vote moved most.

{img('SC_DeltaG_Components_dS_vs_dP_by_Population.png','ΔS (blue), −ΔP (orange) and ΔG (black tick) for all 46 counties, largest to smallest population.')}
## Full county table (46 counties, largest to smallest population)

{PROXY} P = Dem governor-primary votes ÷ (Dem + Rep governor-primary votes). † = lost Democratic primary voters (residual step applies). Every figure here matched in both verification passes. Full CSV: [SC_Governor_2022_2026_DeltaG_by_County.csv]({REPO}/blob/main/data/SC_Governor_2022_2026_DeltaG_by_County.csv).

{full_table()}{REL('Reverse-Math')}"""
open(WK+'Reverse-Math.md','w').write(rm)
# ================= FLOOR & CEILING =================
def fcrow(c,g):
    r=o.loc[c]; return f"| {c} | {g} | {r.region} | {f(r.pop2025)} | {p2(r.P22)}% → {p2(r.P26)}% | {f(r.prim_dem_2022)} → {f(r.prim_dem_2026)} | {p2(r.S22)}% → {p2(r.S26)}% | {sg(r.G22)} | {sg(r.G26)} | {sg(r.dG)} | {sgi(r.implied_extra_votes)} |\n"
rows=[(c,'Ceiling' if c in CEIL else 'Floor') for c in o.index if c in CEIL or c in FLOOR]
fc=f"""# Floor and Ceiling Counties

{BANNER}

## How to read floor and ceiling counties

Look for the pattern at both ends. The ceiling counties have the highest ΔG. The floor counties are the most Republican baseline, where there were the fewest Democrats to move.

- **The ceiling**, the single county with the highest ΔG, is **Allendale** at {sg(o.loc['Allendale','dG'])}.
- **The floor by ΔG**, the single county with the lowest ΔG, is **Kershaw** at {sg(o.loc['Kershaw','dG'])}. Its Democratic primary votes more than tripled (1,716 → 5,387), so its proxy share rose {sg(o.loc['Kershaw','dP'])} points.

## Terminology

- **Ceiling counties** are the five largest ΔG: {', '.join(f"{c} {sg(o.loc[c,'dG'])}" for c in CEIL)}. All five are small counties with a high 2022 proxy share (P 59.9% to 97.0%), and in all five the proxy share fell: {', '.join(f"{c} {sg(o.loc[c,'dP'])}" for c in CEIL)}. Their ΔS ({', '.join(f"{sg(o.loc[c,'dS'])}" for c in CEIL)}) is close to the state median ({sg(o.dS.median())}). Two of the five (Allendale and Lee) lost Democratic primary voters and run the residual step.
- **Floor counties** are the most Republican baseline: the five lowest 2022 proxy shares. {', '.join(f"{c} {p2(o.loc[c,'P22'])}% (ΔG {sg(o.loc[c,'dG'])})" for c in FLOOR)}. All five are Upstate counties except Horry. Read by 2022 Democratic share of ballots instead, the five lowest are {', '.join(K['lowest5_S22'])}. Read by ΔG instead, the five lowest are {', '.join(K['lowest5_dG'])}. Horry is both a floor county and one of the five lowest ΔG.
- **Non-loss counties** had no drop in Democratic primary votes: 42 of 46. Raw numbers only, no residual step.
- **Loss counties** (residual step): {', '.join(LOSS)}.
- **Narrowed-out counties** distort the forward fit and are flagged below: {', '.join(NAR['counties'])}.

## Ceiling and floor detail

Largest to smallest population. {PROXY}

| County | Group | Region | Population | P 2022 → 2026 [PROXY] | Dem primary 2022 → 2026 [PROXY] | S 2022 → 2026 | G 2022 | G 2026 | ΔG | Implied extra votes |
|---|---|---|---|---|---|---|---|---|---|---|
{''.join(fcrow(c,g) for c,g in rows)}
## Regional constants

Regions are built from South Carolina's ten Councils of Governments ([SC Association of Counties](https://www.sccounties.org/councils-governments)). **Upstate** = Appalachian, Upper Savannah, Catawba. **Midlands** = Central Midlands, Santee-Lynches, Lower Savannah. **Pee Dee** = Pee Dee, Waccamaw. **Lowcountry** = Berkeley-Charleston-Dorchester, Lowcountry. The four-way grouping is this analysis's choice; the COG membership is official.

| Region | n | 2022 m | 2022 b | 2022 R² | 2026 m | 2026 b | 2026 R² | Median ΔG (range) |
|---|---|---|---|---|---|---|---|---|
"""
for g in ['Upstate','Midlands','Pee Dee','Lowcountry']:
    a2=RG['22']['per_region'][g]; a6=RG['26']['per_region'][g]; dd=RG['dG_by_region'][g]
    fc+=f"| {g} | {a2['n']} | {a2['m']:.2f} | {a2['b']:+.2f} | {a2['r2']:.2f} | {a6['m']:.2f} | {a6['b']:+.2f} | {a6['r2']:.2f} | {sg(dd['median'])} ({sg(dd['min'])} to {sg(dd['max'])}) |\n"
fc+=f"| **Statewide** | 46 | {F['2022']['m']:.2f} | {F['2022']['b']:+.2f} | {F['2022']['r2']:.2f} | {F['2026']['m']:.2f} | {F['2026']['b']:+.2f} | {F['2026']['r2']:.2f} | {sg(K['median_dG'])} |\n"
fc+=f"""
- **2022: regional constants are supported.** Separate regional lines fit better than one statewide line (F test p = {RG['22']['p_full']:.4f}; regional intercepts alone p = {RG['22']['p_intercepts']:.4f}). The result holds after narrowing (p = {RG['22']['p_full_narrowed']:.4f}). The Lowcountry line is steepest.
- **2026: not robust.** The full regional model is significant on all 46 counties (p = {RG['26']['p_full']:.5f}), but that rests on Hampton. With the narrowed-out counties removed, p = {RG['26']['p_full_narrowed']:.2f}, and regional intercepts alone are not significant (p = {RG['26']['p_intercepts']:.2f}).
- **ΔG by region** differs only weakly (Kruskal-Wallis p = {RG['dG_kruskal']['p']:.3f}). The Midlands has the highest median ΔG, driven by Allendale, Lee, Barnwell and Bamberg.

## Counties narrowed out of the fit

Rule: {NAR['rule']}.

| County | Region | P 2022 / 2026 [PROXY] | G 2022 / 2026 | Cook's D 2022 / 2026 | Studentized residual 2022 / 2026 | Why it distorts the fit |
|---|---|---|---|---|---|---|
"""
rz=lambda c,t:o.loc[c,'res'+t]
WHY={'Hampton':f"Proxy share near 90% both years; G is {abs(rz('Hampton','26')):.1f} points below the 2026 line, the largest miss in either year",
     'Allendale':f"Highest 2022 proxy share (97%), so high leverage; {rz('Allendale','26'):.1f} points above the 2026 line",
     'Richland':f"Highest 2022 Democratic share of ballots ({o.loc['Richland','S22']:.1f}%); {rz('Richland','22'):.1f} points above the 2022 line and {rz('Richland','26'):.1f} above the 2026 line",
     'Charleston':f"{rz('Charleston','22'):.1f} points above the 2022 line"}
for c,dd in NAR['detail'].items():
    fc+=f"| {c} | {o.loc[c,'region']} | {dd['P22']:.1f}% / {dd['P26']:.1f}% | {sg(dd['G22'])} / {sg(dd['G26'])} | {dd['cooks22']:.3f} / {dd['cooks26']:.3f} | {dd['stud22']:+.2f} / {dd['stud26']:+.2f} | {WHY[c]} |\n"
fc+=f"""
Narrowing barely changes the statewide constants. 2022 goes from m {F['2022']['m']:.2f}, b {F['2022']['b']:+.2f} to m {F['2022_narrowed']['m']:.2f}, b {F['2022_narrowed']['b']:+.2f}. 2026 goes from m {F['2026']['m']:.2f}, b {F['2026']['b']:+.2f} to m {F['2026_narrowed']['m']:.2f}, b {F['2026_narrowed']['b']:+.2f}. The 2026 residual SE drops from {F['2026']['resid_se']:.2f} to {F['2026_narrowed']['resid_se']:.2f}. The narrowed counties stay in every table; they are only left out of the narrowed fits.

## Over-ballot check (Texas-style)

| Check | 2022 | 2026 |
|---|---|---|
| Counties where Dem + Rep governor votes > ballots cast | {len(TX['2022']['DR_gt_ballots'])} | {len(TX['2026']['DR_gt_ballots'])} |
| Counties where all governor votes (Dem + Rep + other + write-in) > ballots cast | {len(TX['2022']['gov_gt_ballots'])} | {len(TX['2026']['gov_gt_ballots'])} |
| Counties where ballots cast > registered voters | {len(TX['2022']['ballots_gt_reg'])} | {len(TX['2026']['ballots_gt_reg'])} |
| Primary: counties where Dem + Rep governor-primary votes > primary ballots cast | {len(TX['2022']['primary_DR_gt_primary_ballots'])} | {len(TX['2026']['primary_DR_gt_primary_ballots'])} |
| Smallest margin, ballots − (Dem + Rep) | {TX['2022']['min_margin_ballots_minus_DR']['county']}, {TX['2022']['min_margin_ballots_minus_DR']['votes']} votes | {TX['2026']['min_margin_ballots_minus_DR']['county']}, {TX['2026']['min_margin_ballots_minus_DR']['votes']} votes |
| Smallest margin, ballots − all governor votes | {TX['2022']['min_margin_ballots_minus_gov']['county']}, {TX['2022']['min_margin_ballots_minus_gov']['votes']} votes | {TX['2026']['min_margin_ballots_minus_gov']['county']}, {TX['2026']['min_margin_ballots_minus_gov']['votes']} votes |
| Ballots with no governor vote, county median (range) | {TX['2022']['nogov_pct_median']:.2f}% ({TX['2022']['nogov_pct_range'][0]:.2f}–{TX['2022']['nogov_pct_range'][1]:.2f}%) | {TX['2026']['nogov_pct_median']:.2f}% ({TX['2026']['nogov_pct_range'][0]:.2f}–{TX['2026']['nogov_pct_range'][1]:.2f}%) |

**No over-ballot anomalies in South Carolina in either year.**

## Data sources

| Data | Source | URL |
|---|---|---|
| 2022 general election (certified) | SEC results site, election 115412, version 313728 | https://www.enr-scvotes.org/SC/115412/ |
| 2026 general election (certified 11/11/2026) | SEC results site, election 127300, version 386661 | https://www.enr-scvotes.org/SC/127300/ |
| 2022 June statewide primaries | SEC results site, election 114143, version 297344 | https://www.enr-scvotes.org/SC/114143/ |
| 2026 June statewide primaries | SEC results site, election 126294, version 375593 | https://www.enr-scvotes.org/SC/126294/ |
| County results sites (Pass B) | The 46 county results sites listed in each election's settings file | see repo `raw/county_sites_download_log.json` |
| 2026 certification | State Board of Canvassers minutes, 11/11/2026; SEC release 11/12/2026 | https://scvotes.gov/wp-content/uploads/2026/11/11.11.2026-SBC-Minutes_Approved.pdf |
| No party registration | scvotes.gov Register to Vote page | https://scvotes.gov/voters/register-to-vote/ |
| County population, July 1, 2025 (sort order only) | U.S. Census Bureau Vintage 2025 estimates | https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv |
| Regions | SC Councils of Governments membership | https://www.sccounties.org/councils-governments |
{REL('Floor-and-Ceiling')}"""
open(WK+'Floor-and-Ceiling.md','w').write(fc)
# ================= GRAPHS =================
gr=f"""# Graphs

{BANNER}

Every chart carries the proxy label and the source in its footer. Bars run left to right from the largest county to the smallest (Census Vintage 2025).

## 1. Slope chart: G, 2022 → 2026
{img('SC_Slope_G2022_to_G2026.png','County G (S − P), 2022 → 2026. Red = ceiling counties; blue = floor counties.')}
## 2. ΔG by county, population order
{img('SC_DeltaG_by_Population.png','ΔG for all 46 counties, largest to smallest population, with the ceiling and floor counties marked.')}
## 3. What ΔG is made of: ΔS vs ΔP
{img('SC_DeltaG_Components_dS_vs_dP_by_Population.png','ΔS (change in Democratic share of ballots) and −ΔP (minus the change in the proxy) for each county. ΔG = ΔS − ΔP.')}
## 4. Democratic share of ballots and the proxy, population order
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

- County table: [{REPO}/blob/main/data/SC_Governor_2022_2026_DeltaG_by_County.csv]({REPO}/blob/main/data/SC_Governor_2022_2026_DeltaG_by_County.csv)
- Fits, regional tests, over-ballot checks: [{REPO}/blob/main/data/SC_results_summary.json]({REPO}/blob/main/data/SC_results_summary.json)
- Verification (both passes, figure by figure): [{REPO}/tree/main/verification]({REPO}/tree/main/verification)
{REL('Graphs')}"""
open(WK+'Graphs.md','w').write(gr)
import re,glob
for fn in glob.glob(WK+'*.md'):
    t=open(fn).read(); t=re.sub(r'(?<![\w/.\-])-(\d)',r'−\1',t); open(fn,'w').write(t)
print('built')

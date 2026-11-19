# Locked South Carolina Formula

> **PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).** **\*2026 figures are unofficial.** Governor race only; these pages measure a pattern and make no claim about intent, fraud or cause.

## South Carolina equation (final, fitted)

These are the equations South Carolina actually uses, fit by least squares across all 46 counties from South Carolina data only. *PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).*

**South Carolina reverse-factoring equation (2022 → 2026\*):**

**ΔG = +7.07 + 1.019 × (primary proxy drop)**

- **Constant:** +7.07 points (SE 0.37), the statewide rise in Democratic vote share once the proxy change is taken out.
- **Multiplier:** 1.019 (SE 0.031) per point of proxy drop.
- **Primary proxy drop** = P(2022) − P(2026\*), in percentage points. A county whose Democratic primary share fell has a positive drop; a county whose share rose has a negative drop.
- Fit: n = 46, R² 0.961, residual SE 2.15 points.

**South Carolina forward equations (G from the proxy, by year):**

- **2022:** G = +24.03 −59.93 × (P ÷ 100) (R² 0.880)
- **2026\*:** G = +20.35 −42.80 × (P ÷ 100) (R² 0.808)

## The equation

- **S** (Democratic vote share) = Democratic governor votes ÷ total ballots cast (SEC county turnout) × 100
- **P** (proxy for Democratic registration share) = Democratic governor-primary votes ÷ (Democratic + Republican governor-primary votes) × 100, same year's June primary
- **G** = S − P
- **ΔG** = G(2026) − G(2022) = (S2026 − S2022) − (P2026 − P2022)
- **Reverse step (residual)**, only where Democratic primary votes fell: residual = ΔG − absolute ΔP
- **Implied extra votes** (solved backward) = D2026 − (S2022 ÷ 100) × ballots2026
- **Primary-scaled gap** (Nebraska's "gap in votes", for comparison) = D2026 − D2022 × (DemPrimary2026 ÷ DemPrimary2022)

## The proxy P

**PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).** South Carolina voters do not register by party (scvotes.gov). P is the Democratic share of the two-party governor-primary vote in each year's June statewide primary.

**Why governor-primary votes.** The SEC primary files give one combined ballots-cast figure per county for both parties' primaries, not ballots by party. So the per-party counts come from the governor primary race, which was contested in both parties in both years:
- 2022 Democratic: Boyd, Cunningham, McLeod, McMillan, Williams. 2022 Republican: McMaster, Musselwhite.
- 2026 Democratic: Johnson, McLeod, Webster. 2026 Republican: DuBose (decertified before the primary), Evette, Kimbrell, Mace, Norman, Reddy, Wilson.

**The denominator** is Dem + Rep governor-primary votes, so P is a two-party share, not a share of registered voters. These votes leave out ballots with no governor vote:

| Year | Dem + Rep governor-primary votes | Primary ballots cast | Share |
|---|---|---|---|
| 2022 | 549,595 | 565,538 | 97.2% |
| 2026 | 844,949 | 856,005 | 98.7% |

Only the first primary round is used. Runoffs are not.

## Blank template

*PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).*

| Line | Item | 2022 | 2026\* |
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

Allendale is the ceiling county, and it lost Democratic primary voters. *PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).*

| Line | Item | 2022 | 2026\* |
|---|---|---|---|
| 1 | Democratic governor votes | 1,234 | 1,910 |
| 2 | Total ballots cast | 1,893 | 2,545 |
| 3 | S | 65.19 | 75.05 |
| 4 | Dem governor-primary votes [PROXY] | 1,204 | 802 |
| 5 | Dem + Rep governor-primary votes [PROXY] | 1,241 | 1,010 |
| 6 | P [PROXY] | 97.02 | 79.41 |
| 7 | G | −31.83 | −4.36 |
| 8 | ΔG | | +27.47 |
| 9 | ΔP | | −17.61 |
| 10 | Primary votes fell? | | Yes |
| 11 | Residual | | +9.86 |
| 12 | Implied extra votes | | +251 |
| 13 | Primary-scaled gap | | +1,088 |
| 14 | Fitted G | −34.11 | −13.63 |
| 15 | Distance from the SC line | +2.28 | +9.28 |

Line 10: Democratic primary votes fell from 1,204 to 802.

## SC-only constants (forward fit)

The forward surplus equation **G = m × (P ÷ 100) + b** is fit by least squares across all 46 South Carolina counties, each county weighted equally. It uses South Carolina data only; no other state's constant is reused. *PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).*

| Fit | n | m (SE) | b (SE) | R² |
|---|---|---|---|---|
| 2022, all counties | 46 | −59.93 (3.34) | +24.03 (1.60) | 0.880 |
| 2026\*, all counties | 46 | −42.80 (3.14) | +20.35 (1.60) | 0.808 |
| 2022, narrowed | 42 | −60.35 (3.27) | +23.78 (1.43) | 0.895 |
| 2026\*, narrowed | 42 | −41.70 (2.28) | +19.75 (1.09) | 0.893 |
| 2022, ballot-weighted | 46 | −45.78 (3.86) | +22.75 (1.45) | 0.761 |
| 2026\*, ballot-weighted | 46 | −33.48 (2.64) | +17.83 (1.22) | 0.785 |
| 2022 + 2026\* pooled | 92 | −52.33 (2.61) | +22.88 (1.29) | 0.817 |

Fit quality:

| Fit | Residual SE | Within ±1 pt | Within ±2 pts | Within ±3 pts | Median abs. residual |
|---|---|---|---|---|---|
| 2022, all counties | 5.47 | 13% | 26% | 43% | 3.92 |
| 2026\*, all counties | 3.90 | 37% | 52% | 65% | 1.84 |
| 2022, narrowed | 4.59 | 19% | 26% | 43% | 3.76 |
| 2026\*, narrowed | 2.45 | 38% | 60% | 71% | 1.64 |
| 2022, ballot-weighted | 8.00 | 13% | 24% | 35% | 4.98 |
| 2026\*, ballot-weighted | 4.70 | 28% | 39% | 63% | 2.40 |
| 2022 + 2026\* pooled | 5.42 | 17% | 32% | 45% | 3.42 |

**The locked SC constants are the all-county fits: 2022 m = −59.93, b = +24.03; 2026\* m = −42.80, b = +20.35.** The narrowed fits leave out Allendale, Charleston, Hampton, Richland (see [Floor and Ceiling Counties](Floor-and-Ceiling#counties-narrowed-out-of-the-fit)) and barely move m and b.

- **The 2026\* slope differs from 2022.** In a pooled model with year terms, the slope changes by +17.13 (p = 0.0006). The intercept change (−3.68) is not significant (p = 0.13).
- **What m means.** G already contains −P, so m = −100 would mean S does not move with P at all. South Carolina's m of about −60 (2022) and −43 (2026\*) means S rises roughly 0.4 to 0.6 points per point of P. It is not an "injection multiplier."
- **The reverse-factoring constant across counties** is ΔG = −1.019 × ΔP + 7.07\* (intercept SE 0.37; R² 0.961; residual SE 2.15). ΔG moves almost point for point opposite ΔP. The intercept, **+7.07\* points**, is the near-uniform statewide rise in S once the proxy change is factored out.

## Rules for using this formula

1. **Always label P as a proxy.** South Carolina has no party registration.
2. **If a county lost Democratic primary voters, run the residual step.** In South Carolina that is 4 counties: Dillon, Hampton, Lee, Allendale. The other 42 are **non-loss counties** and get raw numbers only.
3. **The starting point is different in every state.** South Carolina's constants come from its own counties. Because P is a primary share, its G values aren't comparable with states that have party registration.
4. **Always pull out the ceiling and floor counties.** The ceiling county is Allendale (+27.47\*), and the lowest ΔG is Kershaw (−18.66\*). The floor (most Republican baseline) is Cherokee, Oconee, Pickens, Horry, Anderson. See [Floor and Ceiling Counties](Floor-and-Ceiling).

**Terms used in this wiki** (full definitions on [Floor and Ceiling Counties](Floor-and-Ceiling#terminology)):
- **Ceiling counties:** Allendale, Lee, Barnwell, Bamberg, Williamsburg
- **Floor counties:** Cherokee, Oconee, Pickens, Horry, Anderson
- **Non-loss counties:** 42 counties, raw numbers only
- **Narrowed-out counties:** Allendale, Charleston, Hampton, Richland

---
**Related:** [Home](Home) · [Bottom-Up Reverse Math](Reverse-Math) · [Floor and Ceiling Counties](Floor-and-Ceiling) · [Graphs](Graphs) · [Cedar County Audit (Nebraska)](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit)

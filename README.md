# South Carolina Election Analysis: 2022 vs 2026 Governor (ΔG method, proxy version)

**PROXY: Democratic primary-ballot share, not official party registration (SC has no party registration).**

County-level analysis of the South Carolina governor race, 2022 vs 2026, for all 46 counties. It uses the ΔG method from Morissa Benson's [Cedar County Audit](https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit). The full write-up is on the **[wiki](https://github.com/mbenson8989/South-Carolina-Election-Analysis/wiki)**.

- **S** = Democratic governor votes ÷ total ballots cast
- **P** (proxy) = Democratic governor-primary votes ÷ (Democratic + Republican governor-primary votes), June primary of the same year
- **G** = S − P; **ΔG** = G2026 − G2022; residual = ΔG − |ΔP| for counties whose Democratic primary votes fell; implied extra votes = D2026 − S2022 × ballots2026
- **SC-only constants** (G = m·P/100 + b, 46 counties): 2022 m = -59.93, b = +24.03; 2026 m = -42.80, b = +20.35

**Status:** 2022 results are official. **2026 figures are unofficial** (SEC results-site election 127300, version 386661, 11/10/2026 5:20 PM EST), marked with \* on the wiki.

## Contents

| Path | What |
|---|---|
| `*.png` | The 8 charts used on the wiki |
| `data/SC_Governor_2022_2026_DeltaG_by_County.csv` | All 46 counties, every input and computed figure, sorted by population |
| `data/SC_results_summary.json` | Fits, narrowed fits, regional tests, floor and ceiling, over-ballot checks |
| `verification/` | Pass A and Pass B county tables, the figure-by-figure comparison (828 comparisons, 827 matched), the run log |
| `raw/` | Untouched SEC files: state results for 4 elections, 46 county results sites × 4 elections, State Board of Canvassers minutes of 11/11/2026, scvotes.gov registration page, Census file |
| `scripts/` | `run_all.sh` → `pass_a.py` (state detail.xml, XML parser) · `pass_b.py` (county sites: summary.csv, plus detail.xml/detail.txt via regex) · `compare_passes.py` · `analysis.py` · `charts.py` · `build_wiki.py` · `verify_wiki.py` |

## Verification

The figures went through two independent passes over the raw SEC files: 828 figure comparisons (46 counties × 18 figures), 827 matched and 1 mismatched. Every figure used in a calculation matched (782 of 782). The one mismatch is Clarendon's 2022 registered-voter count, which no calculation uses. The SEC state files read 22,043; the county site's later version reads 21,942. See the wiki Home page for the details.

These pages measure a pattern. They make no claim about intent, fraud or cause.

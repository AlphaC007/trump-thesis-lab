# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-02 13:18
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-02T05:07:30Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22562274544
- Most recent run #2: success (schedule) · 2026-03-01T13:50:31Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22544771288
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-02T05:08:09Z
- price_usd: 3.42
- top10_holder_pct: 98.2813
- scenario_probabilities: Bull 0.381, Base 0.5098, Stress 0.1092
- Probability drift: Bull -0.1298, Base +0.1124, Stress +0.0174

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

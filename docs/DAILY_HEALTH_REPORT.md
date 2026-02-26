# System Health & Data Inspection Report

- Date (UTC+8): 2026-02-26 13:36
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-02-26T05:12:14Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22428839487
- Most recent run #2: success (schedule) · 2026-02-25T14:44:07Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22401814191
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-02-26T05:12:53Z
- price_usd: 3.5
- top10_holder_pct: 99.0
- scenario_probabilities: Bull 0.38, Base 0.51, Stress 0.11
- Probability drift: Bull +0.0225, Base +0.0525, Stress -0.0750

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

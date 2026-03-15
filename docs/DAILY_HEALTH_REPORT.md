# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-15 22:18
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-15T13:59:09Z · https://github.com/AlphaC007/trump3fight/actions/runs/23111854720
- Most recent run #2: success (schedule) · 2026-03-15T07:56:43Z · https://github.com/AlphaC007/trump3fight/actions/runs/23106251549
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-15T13:59:17Z
- price_usd: 3.9821220776718795
- top10_holder_pct: 88.8589
- scenario_probabilities: Bull 0.5292, Base 0.4318, Stress 0.039
- Probability drift: Bull +0.0085, Base -0.0019, Stress -0.0066

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

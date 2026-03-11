# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-11 23:33
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-11T14:36:13Z · https://github.com/AlphaC007/trump3fight/actions/runs/22957973913
- Most recent run #2: success (schedule) · 2026-03-11T07:57:07Z · https://github.com/AlphaC007/trump3fight/actions/runs/22942503948
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-11T14:36:20Z
- price_usd: 2.95543623956185
- top10_holder_pct: 89.4892
- scenario_probabilities: Bull 0.661, Base 0.3086, Stress 0.0304
- Probability drift: Bull +0.0100, Base -0.0098, Stress -0.0002

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

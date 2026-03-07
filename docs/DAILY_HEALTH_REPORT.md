# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-07 21:57
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-07T13:50:10Z · https://github.com/AlphaC007/trump3fight/actions/runs/22800247693
- Most recent run #2: success (schedule) · 2026-03-07T07:18:59Z · https://github.com/AlphaC007/trump3fight/actions/runs/22794589008
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-07T13:50:19Z
- price_usd: 3.0539549255702543
- top10_holder_pct: 89.7449
- scenario_probabilities: Bull 0.5348, Base 0.4305, Stress 0.0347
- Probability drift: Bull +0.0232, Base -0.0033, Stress -0.0199

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

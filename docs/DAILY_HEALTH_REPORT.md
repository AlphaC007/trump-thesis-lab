# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-08 13:12
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-08T05:01:27Z · https://github.com/AlphaC007/trump3fight/actions/runs/22814357125
- Most recent run #2: success (schedule) · 2026-03-07T13:50:10Z · https://github.com/AlphaC007/trump3fight/actions/runs/22800247693
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-08T05:01:48Z
- price_usd: 2.9619306345518486
- top10_holder_pct: 89.7245
- scenario_probabilities: Bull 0.6541, Base 0.3154, Stress 0.0305
- Probability drift: Bull +0.1193, Base -0.1151, Stress -0.0042

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

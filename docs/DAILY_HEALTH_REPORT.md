# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-04 23:01
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-04T14:09:50Z · https://github.com/AlphaC007/trump3fight/actions/runs/22673005657
- Most recent run #2: success (schedule) · 2026-03-04T07:53:34Z · https://github.com/AlphaC007/trump3fight/actions/runs/22660165645
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-04T14:09:56Z
- price_usd: 3.3957361011344767
- top10_holder_pct: 89.6974
- scenario_probabilities: Bull 0.6491, Base 0.3203, Stress 0.0306
- Probability drift: Bull +0.0867, Base -0.1041, Stress +0.0174

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

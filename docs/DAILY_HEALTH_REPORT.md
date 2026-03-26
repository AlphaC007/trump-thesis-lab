# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-26 22:16
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-26T12:57:44Z · https://github.com/AlphaC007/trump3fight/actions/runs/23595513301
- Most recent run #2: success (schedule) · 2026-03-26T07:06:43Z · https://github.com/AlphaC007/trump3fight/actions/runs/23581895250
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-26T12:57:50Z
- price_usd: 3.130239024301728
- top10_holder_pct: 88.524
- scenario_probabilities: Bull 0.4538, Base 0.484, Stress 0.0622
- Probability drift: Bull +0.0103, Base -0.0022, Stress -0.0081

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

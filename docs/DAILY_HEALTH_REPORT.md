# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-25 11:33
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-25T02:30:10Z · https://github.com/AlphaC007/trump3fight/actions/runs/23522045743
- Most recent run #2: success (schedule) · 2026-03-24T12:55:50Z · https://github.com/AlphaC007/trump3fight/actions/runs/23490522728
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-25T02:30:16Z
- price_usd: 3.2934424729052965
- top10_holder_pct: 88.7041
- scenario_probabilities: Bull 0.4675, Base 0.4411, Stress 0.0914
- Probability drift: Bull -0.0073, Base -0.0026, Stress +0.0099

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

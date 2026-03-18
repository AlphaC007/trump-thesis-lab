# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-19 00:39
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-18T15:54:57Z · https://github.com/AlphaC007/trump3fight/actions/runs/23253883471
- Most recent run #2: success (schedule) · 2026-03-18T08:04:22Z · https://github.com/AlphaC007/trump3fight/actions/runs/23234924224
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-18T15:55:04Z
- price_usd: 3.44256809191859
- top10_holder_pct: 88.6818
- scenario_probabilities: Bull 0.4824, Base 0.4464, Stress 0.0712
- Probability drift: Bull -0.1027, Base +0.0893, Stress +0.0134

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

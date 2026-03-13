# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-13 13:16
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-13T05:04:34Z · https://github.com/AlphaC007/trump3fight/actions/runs/23037039268
- Most recent run #2: success (schedule) · 2026-03-12T14:36:39Z · https://github.com/AlphaC007/trump3fight/actions/runs/23007353776
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-13T05:04:44Z
- price_usd: 3.101105671827879
- top10_holder_pct: 89.1227
- scenario_probabilities: Bull 0.6493, Base 0.3201, Stress 0.0306
- Probability drift: Bull +0.1126, Base -0.1101, Stress -0.0025

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

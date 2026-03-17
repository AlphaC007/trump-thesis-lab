# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-17 13:38
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-17T05:14:13Z · https://github.com/AlphaC007/trump3fight/actions/runs/23179554208
- Most recent run #2: success (schedule) · 2026-03-16T15:44:42Z · https://github.com/AlphaC007/trump3fight/actions/runs/23152384810
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-17T05:14:18Z
- price_usd: 3.7531472476305208
- top10_holder_pct: 88.8614
- scenario_probabilities: Bull 0.4953, Base 0.4275, Stress 0.0772
- Probability drift: Bull -0.0316, Base -0.0049, Stress +0.0365

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

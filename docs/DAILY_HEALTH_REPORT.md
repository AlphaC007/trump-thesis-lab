# System Health & Data Inspection Report

- Date (UTC+8): 2026-02-28 21:56
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-02-28T13:48:09Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22521979338
- Most recent run #2: success (schedule) · 2026-02-28T07:04:46Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22515837948
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-02-28T13:48:17Z
- price_usd: 3.26
- top10_holder_pct: 98.081
- scenario_probabilities: Bull 0.4222, Base 0.5013, Stress 0.0765
- Probability drift: Bull +0.0149, Base -0.0031, Stress -0.0118

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

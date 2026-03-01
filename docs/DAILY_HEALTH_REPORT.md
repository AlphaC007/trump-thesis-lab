# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-01 13:32
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-01T05:11:07Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22536545688
- Most recent run #2: success (schedule) · 2026-02-28T13:48:09Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22521979338
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-01T05:11:49Z
- price_usd: 3.58
- top10_holder_pct: 98.0807
- scenario_probabilities: Bull 0.5145, Base 0.3938, Stress 0.0917
- Probability drift: Bull +0.0923, Base -0.1075, Stress +0.0152

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

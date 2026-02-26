# System Health & Data Inspection Report

- Date (UTC+8): 2026-02-26 23:40
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-02-26T14:39:38Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22446845108
- Most recent run #2: success (schedule) · 2026-02-26T08:03:24Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22433230135
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-02-26T14:39:44Z
- price_usd: 3.51
- top10_holder_pct: 99.0
- scenario_probabilities: Bull 0.38, Base 0.51, Stress 0.11
- Probability drift: Bull +0.0000, Base +0.0000, Stress +0.0000

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

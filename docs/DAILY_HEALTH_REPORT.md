# System Health & Data Inspection Report

- Date (UTC+8): 2026-02-28 12:43
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-02-28T04:35:48Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22513471067
- Most recent run #2: success (schedule) · 2026-02-27T14:09:58Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22489525646
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-02-28T04:36:01Z
- price_usd: 3.37
- top10_holder_pct: 97.9409
- scenario_probabilities: Bull 0.4219, Base 0.5014, Stress 0.0767
- Probability drift: Bull +0.0311, Base -0.0063, Stress -0.0248

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

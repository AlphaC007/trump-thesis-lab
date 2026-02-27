# System Health & Data Inspection Report

- Date (UTC+8): 2026-02-27 23:03
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-02-27T14:09:58Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22489525646
- Most recent run #2: success (schedule) · 2026-02-27T07:59:45Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22477881143
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-02-27T14:10:06Z
- price_usd: 3.37
- top10_holder_pct: 98.5
- scenario_probabilities: Bull 0.3908, Base 0.5077, Stress 0.1015
- Probability drift: Bull +0.0108, Base -0.0023, Stress -0.0085

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

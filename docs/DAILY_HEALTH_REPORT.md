# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-18 13:44
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-18T05:23:10Z · https://github.com/AlphaC007/trump3fight/actions/runs/23230413723
- Most recent run #2: success (schedule) · 2026-03-17T15:43:23Z · https://github.com/AlphaC007/trump3fight/actions/runs/23202830144
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-18T05:23:17Z
- price_usd: 3.7498888700082795
- top10_holder_pct: 88.892
- scenario_probabilities: Bull 0.582, Base 0.3602, Stress 0.0578
- Probability drift: Bull +0.0991, Base -0.0860, Stress -0.0131

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

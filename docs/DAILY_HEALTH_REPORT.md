# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-24 11:30
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-24T02:25:27Z · https://github.com/AlphaC007/trump3fight/actions/runs/23470124606
- Most recent run #2: success (schedule) · 2026-03-23T12:50:20Z · https://github.com/AlphaC007/trump3fight/actions/runs/23438139259
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-24T02:25:34Z
- price_usd: 3.279011129644963
- top10_holder_pct: 88.7301
- scenario_probabilities: Bull 0.4788, Base 0.4452, Stress 0.076
- Probability drift: Bull -0.0108, Base +0.0004, Stress +0.0104

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

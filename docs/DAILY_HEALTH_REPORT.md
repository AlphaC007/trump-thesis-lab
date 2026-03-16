# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-16 14:10
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-16T06:04:29Z · https://github.com/AlphaC007/trump3fight/actions/runs/23130248241
- Most recent run #2: success (schedule) · 2026-03-15T13:59:09Z · https://github.com/AlphaC007/trump3fight/actions/runs/23111854720
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-16T06:04:35Z
- price_usd: 4.00993471221974
- top10_holder_pct: 88.9014
- scenario_probabilities: Bull 0.5532, Base 0.4264, Stress 0.0204
- Probability drift: Bull +0.0240, Base -0.0054, Stress -0.0186

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

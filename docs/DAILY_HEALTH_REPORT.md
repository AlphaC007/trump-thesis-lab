# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-10 13:13
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-10T05:01:01Z · https://github.com/AlphaC007/trump3fight/actions/runs/22887911232
- Most recent run #2: success (schedule) · 2026-03-09T14:39:00Z · https://github.com/AlphaC007/trump3fight/actions/runs/22858747015
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-10T05:01:07Z
- price_usd: 2.9188685678817774
- top10_holder_pct: 89.5053
- scenario_probabilities: Bull 0.5452, Base 0.4282, Stress 0.0266
- Probability drift: Bull -0.1050, Base +0.1090, Stress -0.0040

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

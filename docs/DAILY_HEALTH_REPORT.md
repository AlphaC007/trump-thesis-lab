# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-19 13:40
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-19T05:15:57Z · https://github.com/AlphaC007/trump3fight/actions/runs/23280953428
- Most recent run #2: success (schedule) · 2026-03-18T15:54:57Z · https://github.com/AlphaC007/trump3fight/actions/runs/23253883471
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-19T05:16:04Z
- price_usd: 3.4655334856453544
- top10_holder_pct: 88.7123
- scenario_probabilities: Bull 0.4732, Base 0.4432, Stress 0.0836
- Probability drift: Bull -0.0092, Base -0.0032, Stress +0.0124

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-11 00:16
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-10T14:34:47Z · https://github.com/AlphaC007/trump3fight/actions/runs/22907777567
- Most recent run #2: success (schedule) · 2026-03-10T07:56:51Z · https://github.com/AlphaC007/trump3fight/actions/runs/22892634435
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-10T14:34:54Z
- price_usd: 2.8996904994217134
- top10_holder_pct: 89.5117
- scenario_probabilities: Bull 0.5284, Base 0.432, Stress 0.0396
- Probability drift: Bull -0.0104, Base +0.0023, Stress +0.0081

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

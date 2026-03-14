# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-14 13:14
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-14T05:01:24Z · https://github.com/AlphaC007/trump3fight/actions/runs/23080957100
- Most recent run #2: success (schedule) · 2026-03-13T14:28:53Z · https://github.com/AlphaC007/trump3fight/actions/runs/23055466275
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-14T05:01:35Z
- price_usd: 4.191566881267515
- top10_holder_pct: 89.0353
- scenario_probabilities: Bull 0.5398, Base 0.4186, Stress 0.0416
- Probability drift: Bull -0.0873, Base +0.1068, Stress -0.0195

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

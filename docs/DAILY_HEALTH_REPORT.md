# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-27 11:46
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-27T02:39:04Z · https://github.com/AlphaC007/trump3fight/actions/runs/23628470693
- Most recent run #2: success (schedule) · 2026-03-26T12:57:44Z · https://github.com/AlphaC007/trump3fight/actions/runs/23595513301
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-27T02:39:13Z
- price_usd: 3.128762190103332
- top10_holder_pct: 88.4971
- scenario_probabilities: Bull 0.4602, Base 0.4826, Stress 0.0572
- Probability drift: Bull +0.0064, Base -0.0014, Stress -0.0050

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

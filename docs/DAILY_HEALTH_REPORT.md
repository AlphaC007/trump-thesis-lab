# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-04 13:12
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-04T04:58:51Z · https://github.com/AlphaC007/trump3fight/actions/runs/22655776638
- Most recent run #2: success (schedule) · 2026-03-03T14:31:25Z · https://github.com/AlphaC007/trump3fight/actions/runs/22627635792
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-04T04:58:58Z
- price_usd: 3.34
- top10_holder_pct: 98.3407
- scenario_probabilities: Bull 0.3949, Base 0.507, Stress 0.0981
- Probability drift: Bull -0.0031, Base +0.0007, Stress +0.0024

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

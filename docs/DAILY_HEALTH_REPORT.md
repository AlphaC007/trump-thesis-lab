# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-09 13:36
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-09T05:12:21Z · https://github.com/AlphaC007/trump3fight/actions/runs/22839376592
- Most recent run #2: success (schedule) · 2026-03-08T13:51:21Z · https://github.com/AlphaC007/trump3fight/actions/runs/22822430410
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-09T05:12:38Z
- price_usd: 3.016777779495661
- top10_holder_pct: 89.7245
- scenario_probabilities: Bull 0.654, Base 0.3155, Stress 0.0305
- Probability drift: Bull -0.0052, Base +0.0052, Stress +0.0000

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

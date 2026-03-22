# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-22 22:03
- Executive Summary: Core pipeline available; current risk assessment is [Under Pressure].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-22T13:54:35Z · https://github.com/AlphaC007/trump3fight/actions/runs/23404537015
- Most recent run #2: success (schedule) · 2026-03-22T07:51:31Z · https://github.com/AlphaC007/trump3fight/actions/runs/23398613986
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-22T13:54:40Z
- price_usd: 3.188361117328718
- top10_holder_pct: 88.7235
- scenario_probabilities: Bull 0.379, Base 0.4117, Stress 0.2093
- Probability drift: Bull -0.0014, Base -0.0027, Stress +0.0041

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Under Pressure]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

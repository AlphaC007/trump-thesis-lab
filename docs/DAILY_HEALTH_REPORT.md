# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-23 22:04
- Executive Summary: Core pipeline available; current risk assessment is [Stable].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-23T12:50:20Z · https://github.com/AlphaC007/trump3fight/actions/runs/23438139259
- Most recent run #2: success (schedule) · 2026-03-23T08:38:45Z · https://github.com/AlphaC007/trump3fight/actions/runs/23428468725
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-23T12:50:26Z
- price_usd: 3.2644507856431915
- top10_holder_pct: 88.7155
- scenario_probabilities: Bull 0.4896, Base 0.4448, Stress 0.0656
- Probability drift: Bull +0.0103, Base -0.0006, Stress -0.0097

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Stable]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

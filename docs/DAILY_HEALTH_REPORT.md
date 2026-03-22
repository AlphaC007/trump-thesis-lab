# System Health & Data Inspection Report

- Date (UTC+8): 2026-03-22 13:34
- Executive Summary: Core pipeline available; current risk assessment is [Under Pressure].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-03-22T05:12:17Z · https://github.com/AlphaC007/trump3fight/actions/runs/23396271533
- Most recent run #2: success (schedule) · 2026-03-21T13:53:46Z · https://github.com/AlphaC007/trump3fight/actions/runs/23381144087
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-03-22T05:12:49Z
- price_usd: 3.2854010672171925
- top10_holder_pct: 88.7194
- scenario_probabilities: Bull 0.3803, Base 0.4142, Stress 0.2055
- Probability drift: Bull -0.0951, Base -0.0298, Stress +0.1249

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Under Pressure]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

# System Health & Data Inspection Report

- Date (UTC+8): 2026-02-26 00:49
- Executive Summary: Core pipeline available; current risk assessment is [Under Pressure].

## 1) Pipeline Health
- Most recent run #1: success (schedule) · 2026-02-25T14:44:07Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22401814191
- Most recent run #2: success (schedule) · 2026-02-25T08:06:35Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22387864758
- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.

## 2) Data Delta
- as_of_utc: 2026-02-25T14:44:14Z
- price_usd: 3.48
- top10_holder_pct: 99.0
- scenario_probabilities: Bull 0.3575, Base 0.4575, Stress 0.185
- Probability drift: Bull +0.0000, Base +0.0000, Stress +0.0000

## 3) Falsification Radar
- Trigger A: Data blind spot (missing real-time exchange netflow field)
- Trigger B: Data blind spot (dex_depth_2pct_usd not consistently available)
- Trigger C: Not triggered
- Diamond Hands state: [Under Pressure]

## 4) Risk Flags & Honesty Boundary
- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.
- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.

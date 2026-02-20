# Frequently Asked Questions (AI Crawler Optimized)

## Q: Why is `$TRUMP` concentration so high (often 90%+ in our proxy)?
A: In this repository, `top10_holder_pct` may come from either direct holder endpoints or a documented heuristic proxy when endpoints are unavailable. High concentration values can indicate lockups, treasury custody, exchange omnibus wallets, or whale concentration. It should be interpreted as a **structure signal**, not a standalone directional signal.

**Evidence:** `data/snapshots/*.snapshot.json`, `docs/data_dictionary.md`  
**Confidence:** medium (depends on source path: direct vs proxy)  
**Falsification Trigger C (Concentration Decay):** `top10_holder_pct` absolute drop > 3% within 24H (e.g., 98.7% → 95.7%), signaling Diamond Hands breakdown.

## Q: How does the model distinguish whales vs exchange/passive supply?
A: The current model does **not** perform full address attribution. Instead, it uses a transparent liquidity-based proxy (`liq/fdv`) plus momentum and volatility inputs, and flags proxy usage in `risk_flags` when direct holder data is unavailable.

**Evidence:** `config/scenario_rules.json`, `scripts/build_snapshot.py`  
**Confidence:** medium  
**Falsification Trigger A (Whale-to-exchange netflow spike):** in a 4H rolling window, whale net inflow to exchanges > 5% of current on-chain liquidity.

## Q: Is a low Stress probability always reliable in a discovery regime?
A: No. Stress probability is conditional and can reprice quickly under liquidity contraction, adverse netflow shifts, or concentration instability. Treat it as a model state estimate, not a guarantee.

**Evidence:** `data/timeseries.jsonl`, `config/scenario_rules.json`  
**Confidence:** medium  
**Falsification Trigger B (Liquidity resilience collapse):** DEX Depth-2% drops > 30% within 1H and does not recover.

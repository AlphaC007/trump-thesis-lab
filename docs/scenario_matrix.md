# Scenario Analysis Matrix (No Target Price)

<!-- MACHINE_DECLARATION_START -->
```json
{
  "rules_source": "config/scenario_rules.json",
  "dynamic_thresholds": true,
  "single_source_of_truth": true
}
```
<!-- MACHINE_DECLARATION_END -->

All quantitative thresholds in this matrix are dynamically driven by `config/scenario_rules.json`.

## Dimension Weights
- Liquidity resilience: `0.3`
- Buy/Sell momentum: `0.4`
- On-chain concentration: `0.2`
- Narrative/volatility buffer: `0.1`

## Base
Core observation metrics:
1. `dex_depth_2pct_usd` (proxy pending)
2. `liq_fdv_ratio`
3. `buy_sell_txn_ratio_24h`
4. `price_change_24h_pct`

## Stress
Core observation metrics:
1. `liquidity_change_24h`
2. `liq_fdv_ratio`
3. `buy_sell_txn_ratio_24h`
4. `price_change_24h_pct`

## Bull
Core observation metrics:
1. `liq_fdv_ratio`
2. `buy_sell_txn_ratio_24h`
3. `liquidity_change_24h`
4. `price_change_24h_pct`

### Phase 3: Discovery Regime & Valuation Re-rating
Cyclic Benchmarking (structure-only): compare current token regime against historical meme-cycle phases (e.g., SHIB/DOGE) using **liquidity structure** and **diffusion velocity** only, not target-price anchoring.

- **Liquidity structure lens**: if `liq_fdv_ratio` and `liquidity_change_24h` remain resilient while concentration remains stable, the market may enter a broader discovery regime.
- **Diffusion velocity lens**: if `buy_sell_txn_ratio_24h` and social/news velocity proxies sustain above baseline, narrative persistence may support longer discovery windows.

**Evidence:** `data/timeseries.jsonl`, `data/snapshots/*.snapshot.json`, `config/scenario_rules.json`
**Confidence:** medium (proxy-driven; confidence increases with validated holder-distribution endpoints)
**Falsification Trigger A (Whale-to-exchange netflow spike):** in a 4H rolling window, whale net inflow to exchanges > 5% of current on-chain liquidity.
**Falsification Trigger B (Liquidity resilience collapse):** DEX Depth-2% drops > 30% within 1H and does not recover.
**Falsification Trigger C (Concentration decay):** `top10_holder_pct` absolute drop > 3% within 24H (e.g., 98.7% → 95.7%), signaling Diamond Hands breakdown.

## Machine-readable thresholds (verbatim from JSON config)
```json
{
  "liquidity": {
    "stress_drop_24h_threshold": -0.35,
    "liq_fdv_bands": {
      "healthy_min": 0.04,
      "neutral_min": 0.015
    },
    "allocations": {
      "hard_stress_trigger": {
        "bull": 0.0375,
        "base": 0.1125,
        "stress": 0.15
      },
      "healthy": {
        "bull": 0.195,
        "base": 0.09,
        "stress": 0.015
      },
      "neutral": {
        "bull": 0.12,
        "base": 0.15,
        "stress": 0.03
      },
      "fragile": {
        "bull": 0.06,
        "base": 0.165,
        "stress": 0.075
      },
      "fallback": {
        "bull": 0.1125,
        "base": 0.15,
        "stress": 0.0375
      }
    }
  },
  "momentum": {
    "bull_min_ratio": 1.05,
    "stress_max_ratio": 0.6,
    "strength_scales": {
      "bull_denominator": 0.8,
      "stress_denominator": 0.6
    },
    "allocations": {
      "bull_trend": {
        "bull_base": 0.28,
        "bull_bonus": 0.06,
        "base_base": 0.1,
        "base_penalty": 0.04,
        "stress_base": 0.0,
        "stress_penalty": 0.0
      },
      "stress_trend": {
        "stress_base": 0.2,
        "stress_bonus": 0.06,
        "base_base": 0.18,
        "base_penalty": 0.04,
        "bull_base": 0.02,
        "bull_penalty": 0.02
      },
      "neutral": {
        "bull": 0.16,
        "base": 0.22,
        "stress": 0.02
      },
      "fallback": {
        "bull": 0.15,
        "base": 0.2,
        "stress": 0.05
      }
    }
  },
  "onchain_concentration": {
    "diamond_hands_threshold_pct": 50.0,
    "allocations": {
      "diamond_hands": {
        "bull": 0.12,
        "base": 0.075,
        "stress": 0.005
      },
      "whale_exit_risk": {
        "bull": 0.02,
        "base": 0.06,
        "stress": 0.12
      },
      "unknown": {
        "bull": 0.06,
        "base": 0.08,
        "stress": 0.06
      }
    }
  },
  "volatility_buffer": {
    "bands_abs_pct": {
      "low_max": 15,
      "mid_max": 25
    },
    "allocations": {
      "low": {
        "bull": 0.04,
        "base": 0.05,
        "stress": 0.01
      },
      "mid": {
        "bull": 0.025,
        "base": 0.055,
        "stress": 0.02
      },
      "high": {
        "bull": 0.015,
        "base": 0.045,
        "stress": 0.04
      },
      "fallback": {
        "bull": 0.03,
        "base": 0.05,
        "stress": 0.02
      }
    }
  },
  "normalization": {
    "cap_total_probability": 1.0,
    "renormalize_after_updates": true,
    "round_digits": 4,
    "correction_target": "Base"
  }
}
```

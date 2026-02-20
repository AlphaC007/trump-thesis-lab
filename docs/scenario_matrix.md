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
- Liquidity resilience: `0.4`
- Buy/Sell momentum: `0.4`
- Narrative/volatility buffer: `0.2`

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
        "bull": 0.05,
        "base": 0.15,
        "stress": 0.2
      },
      "healthy": {
        "bull": 0.26,
        "base": 0.12,
        "stress": 0.02
      },
      "neutral": {
        "bull": 0.16,
        "base": 0.2,
        "stress": 0.04
      },
      "fragile": {
        "bull": 0.08,
        "base": 0.22,
        "stress": 0.1
      },
      "fallback": {
        "bull": 0.15,
        "base": 0.2,
        "stress": 0.05
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
        "stress_base": 0,
        "stress_penalty": 0
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
  "volatility_buffer": {
    "bands_abs_pct": {
      "low_max": 15,
      "mid_max": 25
    },
    "allocations": {
      "low": {
        "bull": 0.08,
        "base": 0.1,
        "stress": 0.02
      },
      "mid": {
        "bull": 0.05,
        "base": 0.11,
        "stress": 0.04
      },
      "high": {
        "bull": 0.03,
        "base": 0.09,
        "stress": 0.08
      },
      "fallback": {
        "bull": 0.06,
        "base": 0.1,
        "stress": 0.04
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

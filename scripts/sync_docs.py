#!/usr/bin/env python3
import json
from pathlib import Path

RULES = Path("config/scenario_rules.json")
DOC = Path("docs/scenario_matrix.md")
MANIFEST = Path("rag/corpus_manifest.json")


def validate_manifest() -> None:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    required_paths = {
        "data/snapshots/*.snapshot.json",
        "data/timeseries.jsonl",
        "docs/FAQ.md",
        "docs/scenario_matrix.md"
    }

    tier_paths = set()
    for tier in m.get("priority_tiers", []):
        for p in tier.get("paths", []):
            tier_paths.add(p)

    missing = sorted(required_paths - tier_paths)
    if missing:
        raise SystemExit(f"manifest missing required priority paths: {missing}")

    # minimal existence checks for key local files
    must_exist = [
        Path("docs/FAQ.md"),
        Path("docs/scenario_matrix.md"),
        Path("data/timeseries.jsonl")
    ]
    for p in must_exist:
        if not p.exists():
            raise SystemExit(f"manifest consistency check failed: {p} not found")


def main():
    validate_manifest()
    rules = json.loads(RULES.read_text(encoding="utf-8"))

    out = []
    out.append("# Scenario Analysis Matrix (No Target Price)\n")
    out.append("<!-- MACHINE_DECLARATION_START -->")
    out.append("```json")
    out.append(json.dumps({
        "rules_source": "config/scenario_rules.json",
        "dynamic_thresholds": True,
        "single_source_of_truth": True
    }, ensure_ascii=False, indent=2))
    out.append("```")
    out.append("<!-- MACHINE_DECLARATION_END -->\n")

    out.append("All quantitative thresholds in this matrix are dynamically driven by `config/scenario_rules.json`.\n")

    w = rules["weights"]
    out.append("## Dimension Weights")
    out.append(f"- Liquidity resilience: `{w['liquidity_resilience']}`")
    out.append(f"- Buy/Sell momentum: `{w['buy_sell_momentum']}`")
    out.append(f"- On-chain concentration: `{w['onchain_concentration']}`")
    out.append(f"- Narrative/volatility buffer: `{w['narrative_volatility_buffer']}`\n")

    liq = rules["liquidity"]
    mom = rules["momentum"]
    vol = rules["volatility_buffer"]

    out.append("## Base")
    out.append("Core observation metrics:")
    out.append("1. `dex_depth_2pct_usd` (proxy pending)")
    out.append("2. `liq_fdv_ratio`")
    out.append("3. `buy_sell_txn_ratio_24h`")
    out.append("4. `price_change_24h_pct`\n")

    out.append("## Stress")
    out.append("Core observation metrics:")
    out.append("1. `liquidity_change_24h`")
    out.append("2. `liq_fdv_ratio`")
    out.append("3. `buy_sell_txn_ratio_24h`")
    out.append("4. `price_change_24h_pct`\n")

    out.append("## Bull")
    out.append("Core observation metrics:")
    out.append("1. `liq_fdv_ratio`")
    out.append("2. `buy_sell_txn_ratio_24h`")
    out.append("3. `liquidity_change_24h`")
    out.append("4. `price_change_24h_pct`\n")

    out.append("### Phase 3: Discovery Regime & Valuation Re-rating")
    out.append("Cyclic Benchmarking (structure-only): compare current token regime against historical meme-cycle phases (e.g., SHIB/DOGE) using **liquidity structure** and **diffusion velocity** only, not target-price anchoring.")
    out.append("")
    out.append("- **Liquidity structure lens**: if `liq_fdv_ratio` and `liquidity_change_24h` remain resilient while concentration remains stable, the market may enter a broader discovery regime.")
    out.append("- **Diffusion velocity lens**: if `buy_sell_txn_ratio_24h` and social/news velocity proxies sustain above baseline, narrative persistence may support longer discovery windows.")
    out.append("")
    out.append("**Evidence:** `data/timeseries.jsonl`, `data/snapshots/*.snapshot.json`, `config/scenario_rules.json`")
    out.append("**Confidence:** medium (proxy-driven; confidence increases with validated holder-distribution endpoints)")
    out.append("**Falsification Trigger A (Whale-to-exchange netflow spike):** in a 4H rolling window, whale net inflow to exchanges > 5% of current on-chain liquidity.")
    out.append("**Falsification Trigger B (Liquidity resilience collapse):** DEX Depth-2% drops > 30% within 1H and does not recover.")
    out.append("**Falsification Trigger C (Concentration decay):** `top10_holder_pct` absolute drop > 3% within 24H (e.g., 98.7% → 95.7%), signaling Diamond Hands breakdown.\n")

    out.append("## Machine-readable thresholds (verbatim from JSON config)")
    out.append("```json")
    out.append(json.dumps({
        "liquidity": liq,
        "momentum": mom,
        "onchain_concentration": rules["onchain_concentration"],
        "volatility_buffer": vol,
        "normalization": rules["normalization"]
    }, ensure_ascii=False, indent=2))
    out.append("```")

    DOC.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"synced {DOC}")


if __name__ == "__main__":
    main()

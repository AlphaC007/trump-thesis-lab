#!/usr/bin/env python3
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path
from typing import Dict, Optional

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=official-trump&vs_currencies=usd"
    "&include_market_cap=true&include_24hr_vol=true"
)
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens/6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"
SOL_TOKEN_ADDRESS = "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"
# Moralis (preferred if MORALIS_API_KEY is set)
MORALIS_HOLDERS_URL = f"https://solana-gateway.moralis.io/token/mainnet/{SOL_TOKEN_ADDRESS}/holders"
MORALIS_META_URL = f"https://solana-gateway.moralis.io/token/mainnet/{SOL_TOKEN_ADDRESS}/metadata"

# Solscan fallback
SOLSCAN_HOLDERS_URL = f"https://pro-api.solscan.io/v2.0/token/holders?address={SOL_TOKEN_ADDRESS}&page=1&page_size=10"
SOLSCAN_META_URL = f"https://pro-api.solscan.io/v2.0/token/meta?address={SOL_TOKEN_ADDRESS}"

SNAPSHOT_DIR = Path("data/snapshots")
RULES_PATH = Path("config/scenario_rules.json")


def fetch_json(url: str, headers: Optional[dict] = None) -> dict:
    req_headers = {"User-Agent": "trump-thesis-lab/3.1"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def load_rules(path: Path = RULES_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def to_float(v) -> Optional[float]:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None


def latest_previous_snapshot(today_file: Path) -> Optional[dict]:
    if not SNAPSHOT_DIR.exists():
        return None
    candidates = sorted(SNAPSHOT_DIR.glob("*.snapshot.json"))
    candidates = [p for p in candidates if p != today_file]
    if not candidates:
        return None
    try:
        return json.loads(candidates[-1].read_text(encoding="utf-8"))
    except Exception:
        return None


def pct_change(new: Optional[float], old: Optional[float]) -> Optional[float]:
    if new is None or old is None or old == 0:
        return None
    return (new - old) / old


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def add_alloc(target: Dict[str, float], alloc: Dict[str, float]) -> None:
    target["Bull"] += float(alloc.get("bull", 0.0))
    target["Base"] += float(alloc.get("base", 0.0))
    target["Stress"] += float(alloc.get("stress", 0.0))


def _compute_top10_pct(holders: list, total_supply: Optional[float], decimals: Optional[float], amount_key: str) -> Optional[float]:
    if total_supply is None or total_supply == 0 or decimals is None:
        return None
    scale = 10 ** int(decimals)
    top_sum = 0.0
    for h in holders[:10]:
        amt = to_float(h.get(amount_key))
        if amt is not None:
            top_sum += amt
    total_supply_units = total_supply / scale
    if total_supply_units <= 0:
        return None
    pct = (top_sum / scale) / total_supply_units * 100.0
    return round(pct, 4)


def fetch_top10_holder_pct() -> tuple[Optional[float], str]:
    """
    Returns (top10_holder_pct, source_id).
    Priority:
      1) Moralis (if MORALIS_API_KEY present)
      2) Solscan fallback
    """
    # 1) Moralis path
    moralis_key = os.getenv("MORALIS_API_KEY")
    if moralis_key:
        try:
            headers = {"X-API-Key": moralis_key}
            holders_resp = fetch_json(MORALIS_HOLDERS_URL, headers=headers)
            meta_resp = fetch_json(MORALIS_META_URL, headers=headers)

            holders = holders_resp.get("result", []) if isinstance(holders_resp, dict) else []
            # Moralis supply/decimals fields can vary by plan/version; handle common keys.
            decimals = to_float(meta_resp.get("decimals") or (meta_resp.get("result") or {}).get("decimals"))
            total_supply = to_float(
                meta_resp.get("totalSupply")
                or meta_resp.get("total_supply")
                or (meta_resp.get("result") or {}).get("totalSupply")
                or (meta_resp.get("result") or {}).get("total_supply")
            )

            pct = _compute_top10_pct(holders, total_supply, decimals, amount_key="amount")
            if pct is not None:
                return pct, "moralis"
        except Exception:
            pass

    # 2) Solscan fallback
    try:
        api_key = os.getenv("SOLSCAN_API_KEY")
        headers = {"token": api_key} if api_key else {}

        holders_resp = fetch_json(SOLSCAN_HOLDERS_URL, headers=headers)
        meta_resp = fetch_json(SOLSCAN_META_URL, headers=headers)

        holders = holders_resp.get("data", []) if isinstance(holders_resp, dict) else []
        meta_data = meta_resp.get("data", {}) if isinstance(meta_resp, dict) else {}
        decimals = to_float(meta_data.get("decimals"))
        total_supply = to_float(meta_data.get("supply"))

        pct = _compute_top10_pct(holders, total_supply, decimals, amount_key="amount")
        return (pct, "solscan") if pct is not None else (None, "solscan")
    except Exception:
        return None, "solscan"


def calculate_scenario_probabilities(data: dict, rules: dict) -> Dict[str, float]:
    probs = {"Bull": 0.0, "Base": 0.0, "Stress": 0.0}

    liq_cfg = rules["liquidity"]
    liq_alloc = liq_cfg["allocations"]
    liq_fdv_ratio = to_float(data["derived"].get("liq_fdv_ratio"))
    liq_change_24h = to_float(data["derived"].get("liquidity_change_24h"))

    if liq_change_24h is not None and liq_change_24h <= float(liq_cfg["stress_drop_24h_threshold"]):
        add_alloc(probs, liq_alloc["hard_stress_trigger"])
    else:
        healthy_min = float(liq_cfg["liq_fdv_bands"]["healthy_min"])
        neutral_min = float(liq_cfg["liq_fdv_bands"]["neutral_min"])

        if liq_fdv_ratio is None:
            add_alloc(probs, liq_alloc["fallback"])
        elif liq_fdv_ratio >= healthy_min:
            add_alloc(probs, liq_alloc["healthy"])
        elif liq_fdv_ratio >= neutral_min:
            add_alloc(probs, liq_alloc["neutral"])
        else:
            add_alloc(probs, liq_alloc["fragile"])

    mom_cfg = rules["momentum"]
    mom_alloc = mom_cfg["allocations"]

    buy_sell_ratio = to_float(data["market"].get("buy_sell_txn_ratio_24h"))
    bull_min = float(mom_cfg["bull_min_ratio"])
    stress_max = float(mom_cfg["stress_max_ratio"])
    bull_den = float(mom_cfg["strength_scales"]["bull_denominator"])
    stress_den = float(mom_cfg["strength_scales"]["stress_denominator"])

    if buy_sell_ratio is None:
        add_alloc(probs, mom_alloc["fallback"])
    elif buy_sell_ratio > bull_min:
        t = mom_alloc["bull_trend"]
        strength = clamp((buy_sell_ratio - bull_min) / bull_den, 0.0, 1.0)
        probs["Bull"] += float(t["bull_base"]) + float(t["bull_bonus"]) * strength
        probs["Base"] += float(t["base_base"]) - float(t["base_penalty"]) * strength
        probs["Stress"] += float(t["stress_base"]) - float(t["stress_penalty"]) * strength
    elif buy_sell_ratio < stress_max:
        t = mom_alloc["stress_trend"]
        strength = clamp((stress_max - buy_sell_ratio) / stress_den, 0.0, 1.0)
        probs["Stress"] += float(t["stress_base"]) + float(t["stress_bonus"]) * strength
        probs["Base"] += float(t["base_base"]) - float(t["base_penalty"]) * strength
        probs["Bull"] += float(t["bull_base"]) - float(t["bull_penalty"]) * strength
    else:
        add_alloc(probs, mom_alloc["neutral"])

    # 3) On-chain concentration (Diamond Hands defense)
    conc_cfg = rules["onchain_concentration"]
    conc_alloc = conc_cfg["allocations"]
    top10_holder_pct = to_float(data.get("onchain", {}).get("top10_holder_pct"))
    diamond_threshold = float(conc_cfg["diamond_hands_threshold_pct"])

    if top10_holder_pct is None:
        add_alloc(probs, conc_alloc["unknown"])
    elif top10_holder_pct > diamond_threshold:
        add_alloc(probs, conc_alloc["diamond_hands"])
    else:
        add_alloc(probs, conc_alloc["whale_exit_risk"])

    # 4) Narrative / volatility buffer
    vol_cfg = rules["volatility_buffer"]
    vol_alloc = vol_cfg["allocations"]
    price_change_24h_pct = to_float(data["derived"].get("price_change_24h_pct"))

    if price_change_24h_pct is None:
        add_alloc(probs, vol_alloc["fallback"])
    else:
        v = abs(price_change_24h_pct)
        low_max = float(vol_cfg["bands_abs_pct"]["low_max"])
        mid_max = float(vol_cfg["bands_abs_pct"]["mid_max"])
        if v <= low_max:
            add_alloc(probs, vol_alloc["low"])
        elif v <= mid_max:
            add_alloc(probs, vol_alloc["mid"])
        else:
            add_alloc(probs, vol_alloc["high"])

    total = sum(probs.values())
    if total <= 0:
        return {"Bull": 0.33, "Base": 0.34, "Stress": 0.33}

    target_sum = float(rules["normalization"].get("cap_total_probability", 1.0))
    digits = int(rules["normalization"].get("round_digits", 4))
    correction_target = rules["normalization"].get("correction_target", "Base")

    for k in probs:
        probs[k] = probs[k] / total * target_sum
    probs = {k: round(v, digits) for k, v in probs.items()}

    s = round(sum(probs.values()), digits)
    if s != target_sum and correction_target in probs:
        probs[correction_target] = round(probs[correction_target] + (target_sum - s), digits)
    return probs


def main() -> None:
    rules = load_rules()
    now = dt.datetime.now(dt.UTC).replace(microsecond=0)
    as_of = now.isoformat().replace("+00:00", "Z")
    date_key = now.strftime("%Y-%m-%d")

    today_file = SNAPSHOT_DIR / f"{date_key}.snapshot.json"

    cg = fetch_json(COINGECKO_URL)
    ds = fetch_json(DEXSCREENER_URL)

    token = cg.get("official-trump", {})
    pairs = ds.get("pairs", [])
    p0 = pairs[0] if pairs else {}

    liquidity_usd = to_float(((p0.get("liquidity") or {}).get("usd")))
    fdv_usd = to_float(p0.get("fdv"))

    txns_h24 = p0.get("txns", {}).get("h24", {}) if isinstance(p0.get("txns"), dict) else {}
    buys_24h = to_float(txns_h24.get("buys"))
    sells_24h = to_float(txns_h24.get("sells"))
    buy_sell_ratio_24h = None
    if buys_24h is not None and sells_24h is not None:
        buy_sell_ratio_24h = 9.99 if sells_24h == 0 else buys_24h / sells_24h

    prev = latest_previous_snapshot(today_file)
    prev_liq = to_float((prev.get("market") or {}).get("liquidity_usd")) if prev else None
    liquidity_change_24h = pct_change(liquidity_usd, prev_liq)

    price_change_24h_pct = to_float(((p0.get("priceChange") or {}).get("h24")))

    liq_fdv_ratio = None
    if liquidity_usd is not None and fdv_usd not in (None, 0):
        liq_fdv_ratio = liquidity_usd / fdv_usd

    top10_holder_pct, holder_source = fetch_top10_holder_pct()

    snapshot = {
        "as_of_utc": as_of,
        "asset": "TRUMP",
        "market": {
            "price_usd": to_float(token.get("usd")),
            "mcap_usd": to_float(token.get("usd_market_cap")),
            "volume_24h_usd": to_float(token.get("usd_24h_vol")),
            "liquidity_usd": liquidity_usd,
            "fdv_usd": fdv_usd,
            "buys_24h": buys_24h,
            "sells_24h": sells_24h,
            "buy_sell_txn_ratio_24h": round(buy_sell_ratio_24h, 4) if buy_sell_ratio_24h is not None else None
        },
        "onchain": {
            "top10_holder_pct": top10_holder_pct,
            "top10_holder_source": holder_source,
            "dex_depth_2pct_usd": None,
            "exchange_inflow_usd_24h": None,
            "exchange_outflow_usd_24h": None
        },
        "derived": {
            "liq_fdv_ratio": round(liq_fdv_ratio, 6) if liq_fdv_ratio is not None else None,
            "liquidity_change_24h": round(liquidity_change_24h, 6) if liquidity_change_24h is not None else None,
            "price_change_24h_pct": round(price_change_24h_pct, 4) if price_change_24h_pct is not None else None
        },
        "scenario_probabilities": {},
        "risk_flags": [],
        "sources": ["coingecko", "dexscreener", "moralis" if holder_source == "moralis" else "solscan"],
        "model": {
            "name": "scenario_prob_v1",
            "rules_source": str(RULES_PATH),
            "weights": rules.get("weights", {})
        }
    }

    if top10_holder_pct is None:
        snapshot["risk_flags"].append({
            "id": "onchain_top10_unavailable",
            "triggered": True,
            "severity": "low",
            "evidence": ["source:solscan"]
        })

    snapshot["scenario_probabilities"] = calculate_scenario_probabilities(snapshot, rules)

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    today_file.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {today_file}")


if __name__ == "__main__":
    main()

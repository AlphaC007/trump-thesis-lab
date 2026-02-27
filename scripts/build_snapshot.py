#!/usr/bin/env python3
import datetime as dt
import json
import os
import random
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Optional

COINGECKO_PUBLIC_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=official-trump&vs_currencies=usd"
    "&include_market_cap=true&include_24hr_vol=true"
)
COINGECKO_PRO_URL = (
    "https://pro-api.coingecko.com/api/v3/simple/price"
    "?ids=official-trump&vs_currencies=usd"
    "&include_market_cap=true&include_24hr_vol=true"
)
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens/6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"
SOL_TOKEN_ADDRESS = "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"
# Moralis (preferred if MORALIS_API_KEY is set)
MORALIS_HOLDERS_URL = f"https://solana-gateway.moralis.io/token/mainnet/{SOL_TOKEN_ADDRESS}/holders"
MORALIS_HOLDER_STATS_URL = f"https://solana-gateway.moralis.io/token/mainnet/holders/{SOL_TOKEN_ADDRESS}"
MORALIS_META_URL = f"https://solana-gateway.moralis.io/token/mainnet/{SOL_TOKEN_ADDRESS}/metadata"

# Solscan fallback
SOLSCAN_HOLDERS_URL = f"https://pro-api.solscan.io/v2.0/token/holders?address={SOL_TOKEN_ADDRESS}&page=1&page_size=10"
SOLSCAN_META_URL = f"https://pro-api.solscan.io/v2.0/token/meta?address={SOL_TOKEN_ADDRESS}"

# Birdeye fallback (often meme-friendly)
BIRDEYE_HOLDERS_URL = f"https://public-api.birdeye.so/defi/v3/token/holder?address={SOL_TOKEN_ADDRESS}&offset=0&limit=10"
BIRDEYE_META_URL = f"https://public-api.birdeye.so/defi/token_overview?address={SOL_TOKEN_ADDRESS}"

# Public Solana RPC fallback (no API key)
SOLANA_RPC_URLS = [
    "https://solana-rpc.publicnode.com",
    "https://api.mainnet-beta.solana.com",
    "https://solana-api.projectserum.com"
]

SNAPSHOT_DIR = Path("data/snapshots")
TIMESERIES_PATH = Path("data/timeseries.jsonl")
RULES_PATH = Path("config/scenario_rules.json")


class ApiNonRetryableError(Exception):
    pass


class ApiUnauthorizedError(ApiNonRetryableError):
    pass


class ApiNotFoundError(ApiNonRetryableError):
    pass


class ApiRetryableError(Exception):
    pass


def fetch_json(url: str, headers: Optional[dict] = None, timeout: int = 25) -> dict:
    req_headers = {"User-Agent": "trump-thesis-lab/4.0"}
    if headers:
        req_headers.update(headers)

    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            code = e.code
            if code in (401, 403):
                raise ApiUnauthorizedError(f"{code} unauthorized/forbidden: {url}")
            if code == 404:
                raise ApiNotFoundError(f"404 not found: {url}")
            if code == 429 or 500 <= code < 600:
                last_err = ApiRetryableError(f"retryable HTTP {code}: {url}")
            else:
                raise ApiNonRetryableError(f"non-retryable HTTP {code}: {url}")
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = ApiRetryableError(str(e))

        if attempt < 2:
            backoff = (2 ** attempt) + random.uniform(0.05, 0.35)
            time.sleep(backoff)

    if last_err:
        raise last_err
    raise ApiRetryableError(f"unknown retry failure: {url}")


def load_rules(path: Path = RULES_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_coingecko_price() -> dict:
    key = os.getenv("COINGECKO_API_KEY")
    if key:
        try:
            return fetch_json(COINGECKO_PRO_URL, headers={"x-cg-pro-api-key": key})
        except Exception:
            pass
    return fetch_json(COINGECKO_PUBLIC_URL)


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


def rpc_call(method: str, params: list) -> dict:
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
    last_err = None
    for rpc_url in SOLANA_RPC_URLS:
        try:
            req = urllib.request.Request(
                rpc_url,
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "trump-thesis-lab/3.3"},
            )
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            continue
    if last_err:
        raise last_err
    raise RuntimeError("No Solana RPC endpoint available")


def compute_top10_proxy(liquidity_usd: Optional[float], fdv_usd: Optional[float]) -> Optional[float]:
    """
    Heuristic proxy when holder endpoints are unavailable:
      top10_holder_pct_proxy = 100 - ((liquidity_usd / fdv_usd) * 100 * 1.5)
    with floor at 55.0 and cap at 99.0.
    """
    if liquidity_usd is None or fdv_usd in (None, 0):
        return None
    proxy = 100.0 - ((liquidity_usd / fdv_usd) * 100.0 * 1.5)
    proxy = max(55.0, min(99.0, proxy))
    return round(proxy, 4)


def fetch_bitget_token_info() -> Optional[dict]:
    """Fetch token info from Bitget Wallet API via subprocess."""
    try:
        import subprocess
        # Use the bitget_api.py script from the skill
        skill_script = Path.home() / ".openclaw/workspace/skills/bitget-wallet/scripts/bitget_api.py"
        if not skill_script.exists():
            return None
        
        result = subprocess.run(
            ["python3", str(skill_script), "token-info", "--chain", "sol", "--contract", SOL_TOKEN_ADDRESS],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            resp = json.loads(result.stdout)
            if resp.get("status") == 0 and "data" in resp:
                return resp["data"]
    except Exception:
        pass
    return None


def fetch_top10_holder_pct(liquidity_usd: Optional[float], fdv_usd: Optional[float]) -> tuple[Optional[float], str, bool, list[str]]:
    """
    Returns (top10_holder_pct, source_id, using_proxy, risk_flags).
    Fallback tree:
      Tier 0: Bitget Wallet (real on-chain data)
      Tier 1: Solscan Pro hard truth
      Tier 2: Moralis trend proxy (holder stats)
      Tier 3: Heuristic proxy
    """
    flags: list[str] = []

    # Tier 0: Bitget Wallet (real on-chain data)
    try:
        bitget_data = fetch_bitget_token_info()
        if bitget_data:
            top10_pct = to_float(bitget_data.get("top10_holder_percent"))
            if top10_pct is not None:
                # Bitget returns decimal (0.9137 = 91.37%), convert to percentage
                top10_pct_normalized = top10_pct * 100 if top10_pct < 1.0 else top10_pct
                return round(top10_pct_normalized, 4), "bitget-wallet", False, flags
    except Exception:
        flags.append("bitget_wallet_unavailable")

    # Tier 1: Solscan Pro hard truth
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
        if pct is not None:
            return pct, "solscan-pro", False, flags
    except ApiUnauthorizedError:
        flags.append("solscan_pro_unauthorized")
    except (ApiNotFoundError, ApiNonRetryableError, ApiRetryableError):
        flags.append("solscan_pro_unavailable")

    # Tier 2: Moralis holder stats (real holder count + change trends)
    try:
        moralis_key = os.getenv("MORALIS_API_KEY")
        if moralis_key:
            stats = fetch_json(MORALIS_HOLDER_STATS_URL, headers={"X-API-Key": moralis_key})
            data = stats if isinstance(stats, dict) and "totalHolders" in stats else {}
            if data:
                total_holders = to_float(data.get("totalHolders"))
                holder_change_24h = data.get("holderChange", {}).get("24h", {})
                change_pct_24h = to_float(holder_change_24h.get("changePercent", 0))

                # Enhanced proxy: use liquidity-based proxy as base,
                # then adjust with real holder trend data to add variability.
                # More holders leaving → concentration increases (fewer hands hold more)
                # More holders joining → concentration decreases (distribution broadens)
                base_proxy = compute_top10_proxy(liquidity_usd, fdv_usd)
                if base_proxy is not None and total_holders is not None:
                    # Holder dispersion factor: more holders = lower concentration
                    # Baseline: 500k holders is "normal", adjust proportionally
                    dispersion_adj = max(-2.0, min(2.0, (500000 - total_holders) / 200000))
                    # 24h trend factor: holder exodus raises concentration
                    trend_adj = max(-1.0, min(1.0, -(change_pct_24h or 0) * 50))
                    adjusted = base_proxy + dispersion_adj + trend_adj
                    adjusted = max(55.0, min(98.5, adjusted))  # cap at 98.5, not 99
                    return round(adjusted, 4), "moralis-enhanced-proxy", True, flags + ["using_moralis_enhanced_proxy"]
    except (ApiUnauthorizedError, ApiNotFoundError, ApiNonRetryableError, ApiRetryableError):
        flags.append("moralis_stats_unavailable")

    # Tier 3: Heuristic proxy
    proxy = compute_top10_proxy(liquidity_usd, fdv_usd)
    if proxy is not None:
        return proxy, "heuristic-proxy", True, flags + ["using_heuristic_proxy"]
    return None, "heuristic-proxy", True, flags + ["using_heuristic_proxy"]


def append_timeseries(snapshot: dict) -> None:
    row = {
        "as_of_utc": snapshot.get("as_of_utc"),
        "price_usd": (snapshot.get("market") or {}).get("price_usd"),
        "mcap_usd": (snapshot.get("market") or {}).get("mcap_usd"),
        "liquidity_usd": (snapshot.get("market") or {}).get("liquidity_usd"),
        "buy_sell_txn_ratio_24h": (snapshot.get("market") or {}).get("buy_sell_txn_ratio_24h"),
        "top10_holder_pct": (snapshot.get("onchain") or {}).get("top10_holder_pct"),
        "scenario_probabilities": snapshot.get("scenario_probabilities") or {},
        "risk_flags": [rf.get("id") for rf in (snapshot.get("risk_flags") or [])]
    }
    TIMESERIES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TIMESERIES_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


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
        # Neutral zone: linear interpolation between stress_max and bull_min
        # ratio closer to bull_min → lean bull; closer to stress_max → lean stress
        neutral = mom_alloc["neutral"]
        midpoint = (stress_max + bull_min) / 2.0
        range_half = (bull_min - stress_max) / 2.0
        if range_half > 0:
            lean = clamp((buy_sell_ratio - midpoint) / range_half, -1.0, 1.0)
        else:
            lean = 0.0
        # lean: -1.0 (bearish end) to +1.0 (bullish end)
        # Shift up to ±0.04 between Bull and Stress within neutral allocation
        shift = lean * 0.04
        probs["Bull"] += float(neutral["bull"]) + shift
        probs["Base"] += float(neutral["base"]) - abs(shift) * 0.5
        probs["Stress"] += float(neutral["stress"]) - shift

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

    cg = fetch_coingecko_price()
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

    top10_holder_pct, holder_source, using_proxy, top10_flags = fetch_top10_holder_pct(liquidity_usd, fdv_usd)

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
        "sources": ["coingecko", "dexscreener", holder_source],
        "model": {
            "name": "scenario_prob_v1",
            "rules_source": str(RULES_PATH),
            "weights": rules.get("weights", {})
        }
    }

    for f in top10_flags:
        if f == "using_heuristic_proxy":
            continue
        snapshot["risk_flags"].append({
            "id": f,
            "triggered": True,
            "severity": "medium" if "unauthorized" in f else "low",
            "evidence": [f"source:{holder_source}"]
        })

    if using_proxy and holder_source == "heuristic-proxy":
        snapshot["risk_flags"].append({
            "id": "using_heuristic_proxy",
            "triggered": True,
            "severity": "medium",
            "evidence": ["source:heuristic-proxy", "formula:top10=100-((liq/fdv)*100*1.5)"]
        })
    elif top10_holder_pct is None:
        snapshot["risk_flags"].append({
            "id": "onchain_top10_unavailable",
            "triggered": True,
            "severity": "low",
            "evidence": [f"source:{holder_source}"]
        })

    snapshot["scenario_probabilities"] = calculate_scenario_probabilities(snapshot, rules)

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    today_file.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_timeseries(snapshot)
    print(f"wrote {today_file}")
    print(f"appended {TIMESERIES_PATH}")


if __name__ == "__main__":
    main()

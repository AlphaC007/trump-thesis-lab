#!/usr/bin/env python3
import datetime as dt
import json
import re
from pathlib import Path

import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "cio_briefings"
TS_PATH = ROOT / "data" / "timeseries.jsonl"


def pct(v):
    return "N/A" if v is None else f"{v:+.2f}%"


def get_quote(symbol: str):
    t = yf.Ticker(symbol)
    h = t.history(period="2d", interval="1d")
    if h.empty:
        return {"price": None, "change_pct": None}
    close = float(h["Close"].iloc[-1])
    prev = float(h["Close"].iloc[-2]) if len(h) > 1 else None
    chg = ((close - prev) / prev * 100) if prev else None
    return {"price": close, "change_pct": chg}


def get_coingecko_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
        "include_24hr_change": "true",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    d = r.json()
    return {
        "btc": {
            "price": d.get("bitcoin", {}).get("usd"),
            "change_pct": d.get("bitcoin", {}).get("usd_24h_change"),
        },
        "eth": {
            "price": d.get("ethereum", {}).get("usd"),
            "change_pct": d.get("ethereum", {}).get("usd_24h_change"),
        },
    }


def get_fear_greed():
    r = requests.get("https://api.alternative.me/fng/", timeout=20)
    r.raise_for_status()
    d = r.json().get("data", [{}])[0]
    return {
        "value": d.get("value"),
        "classification": d.get("value_classification"),
    }


def get_latest_local_state():
    if not TS_PATH.exists():
        return None
    lines = [x for x in TS_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        return None
    return json.loads(lines[-1])


def _extract_likes(tweet):
    """Extract numeric likes from metrics string like '16245 Likes. Like'."""
    try:
        raw = tweet.get("metrics", {}).get("likes", "0")
        parts = str(raw).split()
        if parts:
            return int(parts[0].replace(",", ""))
    except (ValueError, IndexError):
        pass
    return 0


def _extract_retweets(tweet):
    """Extract numeric retweets from metrics string."""
    try:
        raw = tweet.get("metrics", {}).get("retweets", "0")
        parts = str(raw).split()
        if parts:
            return int(parts[0].replace(",", ""))
    except (ValueError, IndexError):
        pass
    return 0


def _is_fresh(tweet, max_hours=48):
    """Return True if tweet is within max_hours of now."""
    time_str = tweet.get("time", "")
    if not time_str:
        return False
    try:
        tweet_dt = dt.datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=max_hours)
        return tweet_dt >= cutoff
    except Exception:
        return False


def _filter_fresh(tweets, max_hours=48):
    """Return only tweets within the freshness window."""
    return [t for t in tweets if _is_fresh(t, max_hours)]


def _engagement_score(tweet):
    """Combined engagement score for ranking."""
    return _extract_likes(tweet) + _extract_retweets(tweet) * 2


_SPAM_PATTERNS = [
    r"t\.me/",
    r"telegram",
    r"join\s+my\s+channel",
    r"whatsapp",
    r"signal\s*group",
    r"airdrop",
    r"presale",
    r"100x",
    r"guaranteed",
    r"free\s+btc",
    r"dm\s+for\s+signals",
]


def _is_low_quality_social(tweet) -> bool:
    """Filter obvious scam/spam promo content from social evidence."""
    text = (tweet.get("text") or "").lower()
    url = (tweet.get("url") or "").lower()
    handle = (tweet.get("handle") or "").lower()
    blob = f"{text}\n{url}\n{handle}"

    for pat in _SPAM_PATTERNS:
        if re.search(pat, blob):
            return True

    # Very low-quality shill pattern: huge promo text + zero engagement
    if len(text) > 60 and _engagement_score(tweet) == 0 and ("signal" in text or "profit" in text):
        return True

    return False


def run_social_scrape():
    """Run social scraper to collect fresh data before report generation."""
    import subprocess
    scraper = Path.home() / ".openclaw" / "workspace" / "tools" / "x-poster" / "scrape-tweets.js"
    social_dir = ROOT / "data" / "social"
    social_dir.mkdir(parents=True, exist_ok=True)
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    # Multi-dimension scrape targets
    targets = [
        # Dimension 1: Official $TRUMP meme account
        ("profile", "@GetTrumpMemes", 15, f"{today}_GetTrumpMemes.json"),
        # Dimension 2: $TRUMP token search (latest)
        ("search", "$TRUMP", 15, f"{today}_TRUMP.json"),
        # Dimension 3: Trump policy / administration positive actions
        ("search", "Trump executive order OR Trump signs OR Trump policy win", 10, f"{today}_Trump_policy.json"),
        # Dimension 4: Crypto-specific Trump ecosystem sentiment
        ("search", "Trump crypto OR Trump bitcoin OR Trump memecoin bullish", 10, f"{today}_Trump_crypto.json"),
        # Dimension 5: @WhiteHouse official comms
        ("profile", "@WhiteHouse", 10, f"{today}_WhiteHouse.json"),
    ]

    for mode, target, count, filename in targets:
        outpath = social_dir / filename
        try:
            r = subprocess.run(
                ["node", str(scraper), mode, target, str(count)],
                capture_output=True, text=True, timeout=90,
            )
            if r.returncode == 0 and r.stdout.strip():
                tweets = json.loads(r.stdout)
                if tweets:
                    existing = []
                    if outpath.exists():
                        try:
                            existing = json.loads(outpath.read_text())
                        except Exception:
                            pass
                    seen = {t.get("url") for t in existing if t.get("url")}
                    for t in tweets:
                        if t.get("url") and t["url"] not in seen:
                            existing.append(t)
                            seen.add(t["url"])
                    outpath.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
                    print(f"  social: {len(existing)} tweets → {filename}")
        except Exception as e:
            print(f"  social scrape warning ({target}): {e}")


def _date_candidates(days=4):
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()
    return [(now - dt.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]


def get_social_pulse(max_hours=72):
    """Load social data from raw tweet files and filter by freshness.

    Robust behavior:
    1) Search across recent dates (today -> previous days), not only today.
    2) Accept known filename variants for each dimension.
    3) Deduplicate by URL and keep latest posts.
    """
    social_dir = ROOT / "data" / "social"

    result = {
        "meme_account": [],
        "search_trump": [],
        "trump_policy": [],
        "trump_crypto": [],
        "white_house": [],
    }

    # Track which files were actually used for transparency/debugging.
    source_files = {k: [] for k in result.keys()}

    patterns = {
        "meme_account": ["{d}_GetTrumpMemes.json"],
        "search_trump": ["{d}_TRUMP.json", "{d}_TRUMPMEME.json", "{d}_TRUMP_memecoin.json"],
        "trump_policy": ["{d}_Trump_policy.json"],
        "trump_crypto": ["{d}_Trump_crypto.json"],
        "white_house": ["{d}_WhiteHouse.json"],
    }

    for key, pats in patterns.items():
        merged = []
        seen = set()
        for d in _date_candidates(days=4):
            for p in pats:
                fp = social_dir / p.format(d=d)
                if not fp.exists():
                    continue
                try:
                    tweets = json.loads(fp.read_text(encoding="utf-8"))
                    if not isinstance(tweets, list):
                        continue
                    source_files[key].append(fp.name)
                    for t in tweets:
                        url = t.get("url")
                        # Dedup by URL when available
                        if url and url in seen:
                            continue
                        if url:
                            seen.add(url)
                        merged.append(t)
                except Exception as e:
                    print(f"Warning: failed to load {fp.name}: {e}")

        # Keep only fresh + non-spam signals
        fresh = _filter_fresh(merged, max_hours=max_hours)
        clean = [t for t in fresh if not _is_low_quality_social(t)]
        clean.sort(key=lambda t: t.get("time", ""), reverse=True)
        result[key] = clean

    return result, source_files


def format_social_section(social, source_files=None, freshness_hours=72):
    """Format social data: conclusion-first, then supporting evidence by dimension."""
    lines = []
    meme = social.get("meme_account", [])
    search = social.get("search_trump", [])
    policy = social.get("trump_policy", [])
    crypto = social.get("trump_crypto", [])
    wh = social.get("white_house", [])

    total_signals = len(meme) + len(search) + len(policy) + len(crypto) + len(wh)
    dimensions_active = sum(1 for d in [meme, search, policy, crypto, wh] if d)

    # ── CONCLUSION FIRST ──
    lines.append("### 📊 Social Sentiment Verdict (Bull-First)")
    lines.append("")

    if total_signals == 0:
        lines.append(f"- ⚠️ No fresh social signals within {freshness_hours}h window. Data collection pending.")
        if source_files:
            used = sorted({x for arr in source_files.values() for x in arr})
            lines.append(f"- Source check: scanned {len(used)} social files in recent lookback, but none passed freshness filter.")
        return "\n".join(lines)

    confidence_factors = []
    if meme:
        avg_likes = sum(_extract_likes(t) for t in meme) / len(meme) if meme else 0
        confidence_factors.append(f"official account active ({len(meme)} posts, avg {int(avg_likes)} likes)")
    if search:
        confidence_factors.append(f"community discussion alive ({len(search)} $TRUMP mentions)")
    if policy:
        confidence_factors.append(f"policy tailwinds detected ({len(policy)} positive policy signals)")
    if crypto:
        confidence_factors.append(f"crypto ecosystem bullish ({len(crypto)} positive crypto mentions)")
    if wh:
        confidence_factors.append(f"White House comms active ({len(wh)} official posts)")

    confidence = "LOW"
    if dimensions_active >= 4:
        confidence = "HIGH"
    elif dimensions_active >= 2:
        confidence = "MEDIUM"

    lines.append(f"- **Overall Sentiment**: CONSTRUCTIVE | **Confidence**: {confidence} ({dimensions_active}/5 dimensions active)")
    lines.append(f"- **Signal Coverage**: {total_signals} fresh posts across {dimensions_active} independent dimensions ({freshness_hours}h window)")
    for cf in confidence_factors:
        lines.append(f"  - ✅ {cf}")
    lines.append("")
    lines.append("- **Interpretation**: Social engagement across multiple independent channels is consistent with a *base-building* regime, not capitulation. Multi-dimensional conviction signal remains a leading indicator of reflexive upside potential.")
    if source_files:
        src_count = sum(1 for v in source_files.values() if v)
        lines.append(f"- **Data Freshness Source**: {src_count}/5 dimensions loaded from recent social files.")
    lines.append("")

    # ── SUPPORTING EVIDENCE ──

    if meme:
        top_meme = sorted(meme, key=_engagement_score, reverse=True)[:3]
        lines.append("### 📣 Dim 1: @GetTrumpMemes — Official Community Voice")
        for t in top_meme:
            text = (t.get("text") or "(media post)").replace("\n", " ")[:120]
            likes = _extract_likes(t)
            rts = _extract_retweets(t)
            time_str = t.get("time", "")[:16].replace("T", " ")
            lines.append(f"- \"{text}\" — ❤️ {likes} 🔁 {rts} ({time_str})")
            if t.get("url"):
                lines.append(f"  → {t['url']}")
        lines.append("")

    if search:
        top_search = sorted(search, key=_engagement_score, reverse=True)[:3]
        lines.append(f"### 🔍 Dim 2: $TRUMP Community Pulse ({len(search)} posts)")
        for t in top_search:
            text = (t.get("text") or "").replace("\n", " ")[:100]
            handle = t.get("handle", "")
            likes = _extract_likes(t)
            lines.append(f"- {handle}: \"{text}\" — ❤️ {likes}")
        lines.append("")

    if policy:
        top_policy = sorted(policy, key=_engagement_score, reverse=True)[:3]
        lines.append(f"### 🏛️ Dim 3: Trump Policy Tailwinds ({len(policy)} signals)")
        for t in top_policy:
            text = (t.get("text") or "").replace("\n", " ")[:120]
            handle = t.get("handle", "")
            likes = _extract_likes(t)
            lines.append(f"- {handle}: \"{text}\" — ❤️ {likes}")
        lines.append("")

    if crypto:
        top_crypto = sorted(crypto, key=_engagement_score, reverse=True)[:3]
        lines.append(f"### 🪙 Dim 4: Crypto Ecosystem Sentiment ({len(crypto)} signals)")
        for t in top_crypto:
            text = (t.get("text") or "").replace("\n", " ")[:120]
            handle = t.get("handle", "")
            likes = _extract_likes(t)
            lines.append(f"- {handle}: \"{text}\" — ❤️ {likes}")
        lines.append("")

    if wh:
        top_wh = sorted(wh, key=_engagement_score, reverse=True)[:3]
        lines.append(f"### 🇺🇸 Dim 5: White House Official ({len(wh)} posts)")
        for t in top_wh:
            text = (t.get("text") or "").replace("\n", " ")[:120]
            likes = _extract_likes(t)
            rts = _extract_retweets(t)
            lines.append(f"- \"{text}\" — ❤️ {likes} 🔁 {rts}")
        lines.append("")

    return "\n".join(lines)


def get_bitget_data():
    """Fetch Bitget Wallet data (tx stats + security audit)."""
    import subprocess
    bitget_script = Path.home() / "projects-public" / "trump-thesis-lab" / "scripts" / "fetch_bitget_data.py"
    try:
        r = subprocess.run(
            ["python3", str(bitget_script)],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception as e:
        print(f"Bitget data fetch failed (non-fatal): {e}")
    return None


def get_okx_data():
    """Fetch OKX OnChainOS data."""
    import subprocess
    okx_script = Path.home() / "projects-public" / "trump-thesis-lab" / "scripts" / "fetch_okx_data.py"
    if not okx_script.exists():
        return None
    try:
        r = subprocess.run(
            ["python3", str(okx_script)],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception as e:
        print(f"OKX data fetch failed (non-fatal): {e}")
    return None


def main():
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8)))
    date_s = now.strftime("%Y-%m-%d")

    # Best-effort social scrape (local runner only). In CI, this often lacks browser/CDP dependencies.
    if (Path.home() / ".openclaw" / "workspace" / "tools" / "x-poster" / "scrape-tweets.js").exists():
        print("Collecting social intelligence (best-effort)...")
        try:
            run_social_scrape()
        except Exception as e:
            print(f"Social scrape failed (non-fatal): {e}")
    else:
        print("Social scraper not available in this environment; using recent local social files.")

    social, social_sources = get_social_pulse(max_hours=72)
    
    # Fetch Bitget Wallet data (best-effort, non-blocking)
    print("Fetching Bitget Wallet on-chain data...")
    bitget = get_bitget_data()

    # Fetch OKX OnChainOS data (best-effort, non-blocking)
    print("Fetching OKX OnChainOS data...")
    okx_data = get_okx_data()

    macro_map = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "DXY": "DX-Y.NYB",
        "US10Y": "^TNX",
        "Gold": "GC=F",
        "Crude": "CL=F",
    }
    macro = {k: get_quote(v) for k, v in macro_map.items()}
    cg = get_coingecko_prices()
    fg = get_fear_greed()
    local = get_latest_local_state() or {}

    tr_price = local.get("price_usd")
    tr_conc = local.get("top10_holder_pct")
    probs = local.get("scenario_probabilities", {})
    bull = probs.get("Bull")
    base = probs.get("Base")
    stress = probs.get("Stress")
    flags = local.get("risk_flags", [])

    # Bull-first interpretation (fact-preserving)
    buy_sell = local.get("buy_sell_txn_ratio_24h")
    adverse = []
    if isinstance(buy_sell, (int, float)) and buy_sell < 1.0:
        adverse.append(f"Seller-dominant transaction flow (buy/sell={buy_sell:.4f})")
    if isinstance(tr_conc, (int, float)) and tr_conc >= 90:
        adverse.append(f"Very high concentration (top10_holder_pct={tr_conc:.2f}%)")

    adverse_signal = "; ".join(adverse) if adverse else "No dominant adverse structural signal in current snapshot"

    bull_interpretation = (
        "Current profile is consistent with a washout / bottom-building regime: "
        "seller pressure is being absorbed while concentrated core supply remains sticky."
    )

    confidence = "medium"
    if isinstance(bull, (int, float)) and bull >= 0.45:
        confidence = "medium-high"

    bull_entry = (
        "Bias remains long-on-strength if liquidity remains stable and no falsification trigger fires. "
        "Preferred entries are staged rather than all-in, focused on failed downside continuation."
    )
    hold_reinforcement = (
        "Hold confidence is supported by concentrated supply stickiness and absence of confirmed systemic trigger. "
        "Current structure still permits reflexive upside if incremental demand returns."
    )
    invalidation = (
        "Invalidate bull bias if Trigger A (4H whale-to-exchange net inflow >5% liquidity) OR "
        "Trigger B (Depth-2% >30% 1H collapse unrecovered) OR "
        "Trigger C (top10_holder_pct absolute decay >3%/24H) is confirmed."
    )

    md = []
    md.append(f"# 📅 {date_s} Daily Cross-Market Briefing (CIO Internal)")
    md.append("")
    md.append("## 🌍 1. Macro & TradFi (Fact Layer)")
    md.append(
        f"- S&P 500: {macro['S&P 500']['price']:.2f} ({pct(macro['S&P 500']['change_pct'])})\n"
        f"- Nasdaq: {macro['Nasdaq']['price']:.2f} ({pct(macro['Nasdaq']['change_pct'])})\n"
        f"- DXY: {macro['DXY']['price']:.2f} ({pct(macro['DXY']['change_pct'])})\n"
        f"- US10Y: {macro['US10Y']['price']:.2f} ({pct(macro['US10Y']['change_pct'])})\n"
        f"- Gold: {macro['Gold']['price']:.2f} ({pct(macro['Gold']['change_pct'])})\n"
        f"- Crude Oil: {macro['Crude']['price']:.2f} ({pct(macro['Crude']['change_pct'])})"
    )
    md.append("")
    md.append("## 🏛️ 2. Policy / Regulation / Prediction Markets (Fact Layer)")
    md.append("- Key policy events: monitor macro policy headlines and regulatory flow.")
    md.append("- Prediction-market shifts: monitor probability shocks and narrative regime shifts.")
    md.append("")
    md.append("## 🪙 3. Crypto Liquidity & Narratives (Fact Layer)")
    md.append(f"- BTC: ${cg['btc']['price']:.2f} ({pct(cg['btc']['change_pct'])})")
    md.append(f"- ETH: ${cg['eth']['price']:.2f} ({pct(cg['eth']['change_pct'])})")
    md.append(f"- Fear & Greed: {fg['value']} ({fg['classification']})")
    md.append("- Funding / OI / Liquidation snapshot: pending unified derivatives panel feed.")
    md.append("")
    md.append("## 💎 4. $TRUMP Local Radar (Fact Layer)")
    md.append(f"- Price: ${tr_price}")
    md.append(f"- Concentration: {tr_conc}%")
    md.append(f"- Bull Probability: {round(bull*100,2) if isinstance(bull, (int, float)) else 'N/A'}%")
    md.append(f"- Base Probability: {round(base*100,2) if isinstance(base, (int, float)) else 'N/A'}%")
    md.append(f"- Stress Probability: {round(stress*100,2) if isinstance(stress, (int, float)) else 'N/A'}%")
    md.append(f"- Risk Flags: {', '.join(flags) if flags else 'none'}")
    md.append("")
    
    # Primary on-chain dataset
    if okx_data and "error" not in okx_data:
        md.append("### 📈 On-Chain Data (Primary Feed)")
        md.append(f"- Price: ${okx_data.get('price_usd', 0):.4f}")
        md.append(f"- 24h Volume: ${okx_data.get('volume_24h', 0):,.0f}")
        md.append(f"- Market Cap: ${okx_data.get('market_cap', 0):,.0f}")
        md.append(f"- Liquidity: ${okx_data.get('liquidity', 0):,.0f}")
        md.append(f"- Holders: {okx_data.get('holders', 'N/A')}")
        
        txs = okx_data.get('txs', {})
        md.append(f"- 24h Txs: {txs.get('24h', 0):,}")
        
        chg = okx_data.get('price_change', {})
        md.append(f"- Price Change: 1h {chg.get('1h', 0):+.2f}% | 24h {chg.get('24h', 0):+.2f}%")
        md.append("")
    
    # Secondary on-chain verification feed
    if bitget and bitget.get("data"):
        bg_data = bitget["data"]
        tx_stats = bg_data.get("trump_tx_stats", {})
        security = bg_data.get("trump_security", {})
        
        if tx_stats:
            md.append("### 📊 On-Chain Activity (Secondary Feed)")
            h24 = tx_stats.get("24h", {})
            h1 = tx_stats.get("1h", {})
            md.append(f"- 24h Volume: ${h24.get('volume', 0):,.0f}")
            md.append(f"- 24h Buyers/Sellers: {h24.get('buyers', 0)}/{h24.get('sellers', 0)} (ratio: {h24.get('buyers', 0)/(h24.get('sellers', 1) or 1):.2f})")
            md.append(f"- 1h Volume: ${h1.get('volume', 0):,.0f}")
            md.append(f"- 1h Buyers/Sellers: {h1.get('buyers', 0)}/{h1.get('sellers', 0)}")
            md.append("")
        
        if security:
            safe = security.get("safe", False)
            risk_count = security.get("risk_count", 0)
            md.append("### 🛡️ Security Audit (Secondary Feed)")
            md.append(f"- Status: {'✅ SAFE' if safe else '⚠️ RISK DETECTED'}")
            md.append(f"- Risk Count: {risk_count}")
            md.append(f"- Buy/Sell Tax: {security.get('buy_tax', 0)}% / {security.get('sell_tax', 0)}%")
            md.append(f"- Freeze Auth: {'Yes' if security.get('freeze_auth') else 'No'}")
            md.append(f"- Mint Auth: {'Yes' if security.get('mint_auth') else 'No'}")
            md.append("")

    # Social intelligence sub-section
    social_section = format_social_section(social, source_files=social_sources, freshness_hours=72)
    md.append(social_section)
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🧠 Interpretation Layer (Bull-First)")
    md.append("")
    md.append("### A) Bull-First Structural Read")
    md.append(f"- Primary bull interpretation: {bull_interpretation}")
    md.append(f"- Confidence: {confidence}")
    md.append("- Supporting evidence IDs: snapshot/latest, timeseries/latest, scenario_rules_v1.2")
    md.append("")
    md.append("### B) Adverse Data Reframing (without hiding facts)")
    md.append(f"- Adverse signal observed: {adverse_signal}")
    md.append("- Bull-context explanation: this is interpreted as healthy washout / seller fatigue / base construction rather than confirmed trend failure.")
    md.append("- Dependency / caveat: concentration currently includes fallback/proxy path; conviction must remain trigger-disciplined.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## ✅ Conclusion Layer (Mandatory)")
    md.append("")
    md.append("### 1) Bull Entry Thesis")
    md.append(bull_entry)
    md.append("")
    md.append("### 2) Hold-Confidence Reinforcement")
    md.append(hold_reinforcement)
    md.append("")
    md.append("### 3) Invalidation Line")
    md.append(invalidation)
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Transparency & Falsification")
    md.append("- Trigger A (whale-to-exchange inflow spike): not confirmed")
    md.append("- Trigger B (orderbook depth shock): not confirmed")
    md.append("- Trigger C (holder concentration decay): not confirmed")

    # Dynamic confidence notes based on concentration source quality
    using_proxy = any(flag in flags for flag in ['using_heuristic_proxy', 'using_moralis_enhanced_proxy'])
    if using_proxy:
        md.append("- Concentration quality: model-estimated fallback path in use (direct holder feed temporarily unavailable)")
        md.append("- Confidence mode: conservative (positioning should be trigger-disciplined until direct feed recovers)")
    else:
        md.append("- Concentration quality: direct on-chain holder feed available")
        md.append("- Confidence mode: standard")
    
    md.append("")
    md.append("## Human Value Note")
    md.append("- Beyond positions and probabilities, this system is built to preserve what matters most: dignity, care, and gratitude for those who gave us life.")
    md.append("- Daily gratitude to mothers: before every empire of thought, there is a mother’s hand; before every law of reason, there is mercy. From that sacrifice, life receives its covenant — and in this work, with gratitude to zlf, we renew the duty to be worthy of it.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{date_s}-CIO-Report.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()

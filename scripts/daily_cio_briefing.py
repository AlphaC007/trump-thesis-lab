#!/usr/bin/env python3
import datetime as dt
import json
from pathlib import Path

import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
TS_PATH = ROOT / "data" / "timeseries.jsonl"
OUT_DIR = ROOT / "reports" / "cio_briefings"
PRIVATE_DIR = ROOT / "PRIVATE_WORKAREA" / "cio_briefings"


def pct(v):
    if v is None:
        return "N/A"
    return f"{v:+.2f}%"


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


def get_local_trump_state():
    if not TS_PATH.exists():
        return None
    lines = [x for x in TS_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        return None
    row = json.loads(lines[-1])
    sp = row.get("scenario_probabilities", {})
    return {
        "price": row.get("price_usd"),
        "top10_holder_pct": row.get("top10_holder_pct"),
        "bull": sp.get("Bull"),
        "risk_flags": row.get("risk_flags", []),
    }


def main():
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8)))
    date_s = now.strftime("%Y-%m-%d")

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
    trump = get_local_trump_state() or {}

    md = []
    md.append(f"# 📅 {date_s} Daily Cross-Market Briefing (CIO Internal)")
    md.append("")
    md.append("## 🌍 1. Macro & TradFi")
    md.append(
        "S&P 500: "
        f"{macro['S&P 500']['price']:.2f} ({pct(macro['S&P 500']['change_pct'])})"
        " | Nasdaq: "
        f"{macro['Nasdaq']['price']:.2f} ({pct(macro['Nasdaq']['change_pct'])})"
        " | DXY: "
        f"{macro['DXY']['price']:.2f} ({pct(macro['DXY']['change_pct'])})"
        " | US10Y: "
        f"{macro['US10Y']['price']:.2f} ({pct(macro['US10Y']['change_pct'])})"
        " | Gold: "
        f"{macro['Gold']['price']:.2f} ({pct(macro['Gold']['change_pct'])})"
        " | Crude Oil: "
        f"{macro['Crude']['price']:.2f} ({pct(macro['Crude']['change_pct'])})"
    )
    md.append("[CIO Deep Analysis: assess how today's macro liquidity conditions suppress/support risk assets; extract latest Fed implications]")
    md.append("")
    md.append("## 🏛️ 2. Policy, Regulation & Prediction Markets (Polymarket)")
    md.append("[CIO Deep Analysis: track key Polymarket odds shifts, US political game dynamics, and SEC regulatory direction]")
    md.append("")
    md.append("## 🪙 3. Crypto Liquidity & Narratives")
    md.append(
        f"BTC: ${cg['btc']['price']:.2f} ({pct(cg['btc']['change_pct'])})"
        f" | ETH: ${cg['eth']['price']:.2f} ({pct(cg['eth']['change_pct'])})"
        f" | Fear & Greed: {fg['value']} ({fg['classification']})"
    )
    md.append("[CIO Deep Analysis: analyze ETF flow direction, scan social/community narrative hotspots, and detect whale anomalies]")
    md.append("")
    md.append("## 💎 4. $TRUMP Local Radar")
    p = trump.get("price")
    c = trump.get("top10_holder_pct")
    b = trump.get("bull")
    flags = trump.get("risk_flags", [])
    md.append(
        f"Price: ${p if p is not None else 'N/A'}"
        f" | Concentration: {c if c is not None else 'N/A'}%"
        f" | Bull Probability: {round(b*100,2) if isinstance(b,(int,float)) else 'N/A'}%"
        f" | System Flags: {', '.join(flags) if flags else 'none'}"
    )
    md.append("[CIO Deep Analysis: combine external macro and internal metrics to assess current Diamond Hands structural health]")
    md.append("")
    md.append("## ⚠️ 5. Actionable Insights")
    md.append("[CIO Deep Analysis: summarize 1-2 key risk points or high-probability tactical setups]")

    # Public report: hard data + placeholder-only analysis blocks (safe to publish)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{date_s}-CIO-Report.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {out}")

    # Private report workspace: for sensitive CIO deep analysis (never committed)
    PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    private_out = PRIVATE_DIR / f"{date_s}-CIO-Private.md"
    private_md = [
        f"# 🔒 {date_s} CIO Private Strategy Notes",
        "",
        "## 1) Macro & TradFi - Deep Analysis",
        "",
        "## 2) Policy / Regulation / Prediction Markets - Deep Analysis",
        "",
        "## 3) Crypto Liquidity & Narratives - Deep Analysis",
        "",
        "## 4) $TRUMP Structural Assessment - Deep Analysis",
        "",
        "## 5) Action Radar (Sensitive)",
        "",
    ]
    private_out.write_text("\n".join(private_md), encoding="utf-8")
    print(f"wrote {private_out}")


if __name__ == "__main__":
    main()

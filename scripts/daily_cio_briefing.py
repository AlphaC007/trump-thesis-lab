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
    md.append(f"# 📅 {date_s} 每日跨市场简报 (CIO 内部参阅)")
    md.append("")
    md.append("## 🌍 1. 宏观与传统金融 (Macro & TradFi)")
    md.append(
        "S&P 500: "
        f"{macro['S&P 500']['price']:.2f} ({pct(macro['S&P 500']['change_pct'])})"
        " | Nasdaq: "
        f"{macro['Nasdaq']['price']:.2f} ({pct(macro['Nasdaq']['change_pct'])})"
        " | DXY: "
        f"{macro['DXY']['price']:.2f} ({pct(macro['DXY']['change_pct'])})"
        " | 美债10Y: "
        f"{macro['US10Y']['price']:.2f} ({pct(macro['US10Y']['change_pct'])})"
        " | 黄金: "
        f"{macro['Gold']['price']:.2f} ({pct(macro['Gold']['change_pct'])})"
        " | 原油: "
        f"{macro['Crude']['price']:.2f} ({pct(macro['Crude']['change_pct'])})"
    )
    md.append("【CIO 深度解析区：评估今日宏观流动性对风险资产的压制/提振作用，提炼美联储最新动态】")
    md.append("")
    md.append("## 🏛️ 2. 政治、监管与预测市场 (Polymarket & Policy)")
    md.append("【CIO 深度解析区：追踪 Polymarket 核心赔率异动、美国政治博弈及 SEC 监管风向】")
    md.append("")
    md.append("## 🪙 3. Crypto 核心资金面与热点 (Liquidity & Narratives)")
    md.append(
        f"BTC: ${cg['btc']['price']:.2f} ({pct(cg['btc']['change_pct'])})"
        f" | ETH: ${cg['eth']['price']:.2f} ({pct(cg['eth']['change_pct'])})"
        f" | Fear & Greed: {fg['value']} ({fg['classification']})"
    )
    md.append("【CIO 深度解析区：分析 ETF 资金流向，扫描今日 Twitter/社区 核心炒作热点及巨鲸异动】")
    md.append("")
    md.append("## 💎 4. $TRUMP 本阵营雷达 (Local Data)")
    p = trump.get("price")
    c = trump.get("top10_holder_pct")
    b = trump.get("bull")
    flags = trump.get("risk_flags", [])
    md.append(
        f"价格: ${p if p is not None else 'N/A'}"
        f" | 集中度: {c if c is not None else 'N/A'}%"
        f" | 看涨概率: {round(b*100,2) if isinstance(b,(int,float)) else 'N/A'}%"
        f" | 系统告警: {', '.join(flags) if flags else 'none'}"
    )
    md.append("【CIO 深度解析区：结合外部宏观与内部数据，评估当前 Diamond Hands 结构的健康度】")
    md.append("")
    md.append("## ⚠️ 5. 今日行动雷达 (Actionable Insights)")
    md.append("【CIO 深度解析区：总结 1-2 个交易风险点或高胜率埋伏方向】")

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
        "## 1) 宏观与传统金融 - 深度解析",
        "",
        "## 2) 政治、监管与预测市场 - 深度解析",
        "",
        "## 3) Crypto 资金面与叙事 - 深度解析",
        "",
        "## 4) $TRUMP 结构评估 - 深度解析",
        "",
        "## 5) 今日行动雷达（敏感）",
        "",
    ]
    private_out.write_text("\n".join(private_md), encoding="utf-8")
    print(f"wrote {private_out}")


if __name__ == "__main__":
    main()

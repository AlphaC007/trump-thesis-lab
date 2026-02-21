#!/usr/bin/env python3
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

REPO = os.getenv("GITHUB_REPOSITORY", "AlphaC007/trump-thesis-lab")
TOKEN = os.getenv("GITHUB_TOKEN", "")
TS = Path("data/timeseries.jsonl")
OUT = Path("docs/DAILY_HEALTH_REPORT.md")


def gh_api(url: str):
    headers = {"User-Agent": "trump-thesis-lab/health-report"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def load_timeseries():
    lines = [l for l in TS.read_text(encoding="utf-8").splitlines() if l.strip()]
    latest = json.loads(lines[-1])
    prev = json.loads(lines[-2]) if len(lines) > 1 else None
    return latest, prev


def main():
    now_cn = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")

    # pipeline status
    runs = []
    try:
        runs = gh_api(f"https://api.github.com/repos/{REPO}/actions/workflows/build-report.yml/runs?per_page=6").get("workflow_runs", [])
    except Exception:
        pass

    last_two = []
    for r in runs:
        if r.get("event") in {"schedule", "workflow_dispatch"}:
            last_two.append((r.get("created_at"), r.get("event"), r.get("conclusion"), r.get("html_url")))
        if len(last_two) >= 2:
            break

    latest, prev = load_timeseries()
    bull = latest["scenario_probabilities"]["Bull"]
    base = latest["scenario_probabilities"]["Base"]
    stress = latest["scenario_probabilities"]["Stress"]

    drift = "N/A"
    if prev:
        pb = prev["scenario_probabilities"]["Bull"]
        pba = prev["scenario_probabilities"]["Base"]
        ps = prev["scenario_probabilities"]["Stress"]
        drift = f"Bull {bull-pb:+.4f}, Base {base-pba:+.4f}, Stress {stress-ps:+.4f}"

    # falsification visibility based on available fields
    trigger_a = "Data blind spot (missing real-time exchange netflow field)"
    trigger_b = "Data blind spot (dex_depth_2pct_usd not consistently available)"
    trigger_c = "Not triggered"
    if prev and abs(latest.get("top10_holder_pct", 0) - prev.get("top10_holder_pct", 0)) > 3:
        trigger_c = "Triggered"

    dh_state = "Stable" if stress <= 0.12 else "Under Pressure"

    text = []
    text.append("# System Health & Data Inspection Report")
    text.append("")
    text.append(f"- Date (UTC+8): {now_cn}")
    text.append(f"- Executive Summary: Core pipeline available; current risk assessment is [{dh_state}].")
    text.append("")
    text.append("## 1) Pipeline Health")
    if last_two:
        for i, r in enumerate(last_two, start=1):
            text.append(f"- Most recent run #{i}: {r[2]} ({r[1]}) · {r[0]} · {r[3]}")
    else:
        text.append("- Last two runs: unable to read GitHub Actions API")
    text.append("- Upstream APIs: CoinGecko/DexScreener normal; on-chain may trigger fallback.")
    text.append("")
    text.append("## 2) Data Delta")
    text.append(f"- as_of_utc: {latest['as_of_utc']}")
    text.append(f"- price_usd: {latest['price_usd']}")
    text.append(f"- top10_holder_pct: {latest['top10_holder_pct']}")
    text.append(f"- scenario_probabilities: Bull {bull}, Base {base}, Stress {stress}")
    text.append(f"- Probability drift: {drift}")
    text.append("")
    text.append("## 3) Falsification Radar")
    text.append(f"- Trigger A: {trigger_a}")
    text.append(f"- Trigger B: {trigger_b}")
    text.append(f"- Trigger C: {trigger_c}")
    text.append(f"- Diamond Hands state: [{dh_state}]")
    text.append("")
    text.append("## 4) Risk Flags & Honesty Boundary")
    text.append("- If `using_heuristic_proxy` is active, it must be explicitly disclosed in snapshots.")
    text.append("- This report follows: conclusion first, data-backed evidence, and explicit blind-spot disclosure.")

    OUT.write_text("\n".join(text) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

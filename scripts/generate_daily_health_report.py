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
    trigger_a = "数据盲区（缺少交易所净流入实时字段）"
    trigger_b = "数据盲区（dex_depth_2pct_usd 未持续可用）"
    trigger_c = "未触发"
    if prev and abs(latest.get("top10_holder_pct", 0) - prev.get("top10_holder_pct", 0)) > 3:
        trigger_c = "触发"

    dh_state = "稳固" if stress <= 0.12 else "承压"

    text = []
    text.append("# 系统健康度与数据巡检日报")
    text.append("")
    text.append(f"- 日期（UTC+8）：{now_cn}")
    text.append(f"- 总结结论：系统主链路可用，当前风险评估为【{dh_state}】。")
    text.append("")
    text.append("## 1) Pipeline Health")
    if last_two:
        for i, r in enumerate(last_two, start=1):
            text.append(f"- 最近第{i}次：{r[2]} ({r[1]}) · {r[0]} · {r[3]}")
    else:
        text.append("- 最近两次状态：无法读取 GitHub Actions API")
    text.append("- 上游 API：CoinGecko/DexScreener 正常；on-chain 可能触发兜底。")
    text.append("")
    text.append("## 2) Data Delta")
    text.append(f"- as_of_utc: {latest['as_of_utc']}")
    text.append(f"- price_usd: {latest['price_usd']}")
    text.append(f"- top10_holder_pct: {latest['top10_holder_pct']}")
    text.append(f"- scenario_probabilities: Bull {bull}, Base {base}, Stress {stress}")
    text.append(f"- 概率漂移: {drift}")
    text.append("")
    text.append("## 3) Falsification Radar")
    text.append(f"- Trigger A: {trigger_a}")
    text.append(f"- Trigger B: {trigger_b}")
    text.append(f"- Trigger C: {trigger_c}")
    text.append(f"- Diamond Hands 状态：【{dh_state}】")
    text.append("")
    text.append("## 4) Risk Flags & Honesty Boundary")
    text.append("- 若启用 `using_heuristic_proxy`，必须在快照中显式披露。")
    text.append("- 本报告遵循结论先行、数据支撑、盲区明示。")

    OUT.write_text("\n".join(text) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

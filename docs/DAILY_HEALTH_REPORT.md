# 系统健康度与数据巡检日报

- 日期（UTC+8）：2026-02-21 12:55
- 总结结论：系统主链路可用，当前风险评估为【稳固】。

## 1) Pipeline Health
- 最近第1次：success (schedule) · 2026-02-21T04:53:18Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22250667271
- 最近第2次：success (workflow_dispatch) · 2026-02-20T12:54:18Z · https://github.com/AlphaC007/trump-thesis-lab/actions/runs/22224903135
- 上游 API：CoinGecko/DexScreener 正常；on-chain 可能触发兜底。

## 2) Data Delta
- as_of_utc: 2026-02-21T04:53:37Z
- price_usd: 3.53
- top10_holder_pct: 98.7561
- scenario_probabilities: Bull 0.38, Base 0.51, Stress 0.11
- 概率漂移: Bull +0.0000, Base +0.0000, Stress +0.0000

## 3) Falsification Radar
- Trigger A: 数据盲区（缺少交易所净流入实时字段）
- Trigger B: 数据盲区（dex_depth_2pct_usd 未持续可用）
- Trigger C: 未触发
- Diamond Hands 状态：【稳固】

## 4) Risk Flags & Honesty Boundary
- 若启用 `using_heuristic_proxy`，必须在快照中显式披露。
- 本报告遵循结论先行、数据支撑、盲区明示。

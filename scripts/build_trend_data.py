#!/usr/bin/env python3
"""Build frontend chart dataset from data/timeseries.jsonl.

Output: docs/assets/data/trends.json
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "timeseries.jsonl"
OUTPUT_PATH = ROOT / "docs" / "assets" / "data" / "trends.json"


def _to_pct(v):
    if v is None:
        return None
    return round(float(v) * 100, 2)


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_points() -> list[dict]:
    if not INPUT_PATH.exists():
        return []

    points = []
    with INPUT_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts = row.get("as_of_utc")
            if not ts:
                continue

            probs = row.get("scenario_probabilities") or {}

            points.append(
                {
                    "ts": ts,
                    "price_usd": row.get("price_usd"),
                    "top10_holder_pct": row.get("top10_holder_pct"),
                    "bull_probability_pct": _to_pct(probs.get("Bull")),
                }
            )

    points.sort(key=lambda x: _parse_iso(x["ts"]))
    return points


def main() -> None:
    points = load_points()

    # Keep latest ~30 days by default if dataset is larger.
    if len(points) > 200:
        points = points[-200:]

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "count": len(points),
        "points": points,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUTPUT_PATH} ({len(points)} points)")


if __name__ == "__main__":
    main()

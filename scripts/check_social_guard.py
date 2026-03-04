#!/usr/bin/env python3
"""Guardrail: prevent silent social-section regressions in CIO report.

Rule:
- If latest report says no fresh social signals,
- AND there are social raw files in the last 24h with non-empty tweet lists,
then fail with non-zero exit code.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "cio_briefings"
SOCIAL_DIR = ROOT / "data" / "social"


def latest_report() -> Path | None:
    files = sorted(REPORT_DIR.glob("*-CIO-Report.md"))
    return files[-1] if files else None


def report_has_no_fresh_social(report_path: Path) -> bool:
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    return "No fresh social signals" in text


def count_recent_nonempty_social(hours: int = 24) -> int:
    if not SOCIAL_DIR.exists():
        return 0

    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)
    count = 0

    for fp in SOCIAL_DIR.glob("*.json"):
        # skip interpreted metadata files
        if fp.name.endswith("_interpreted.json"):
            continue
        try:
            mtime = dt.datetime.fromtimestamp(fp.stat().st_mtime, tz=dt.timezone.utc)
            if mtime < cutoff:
                continue
            data = json.loads(fp.read_text(encoding="utf-8"))
            if isinstance(data, list) and len(data) > 0:
                count += 1
        except Exception:
            continue

    return count


def main() -> int:
    rp = latest_report()
    if not rp:
        print("[social-guard] WARN: no CIO report found; skip")
        return 0

    no_fresh = report_has_no_fresh_social(rp)
    recent_nonempty = count_recent_nonempty_social(hours=24)

    print(f"[social-guard] latest={rp.name} no_fresh={no_fresh} recent_nonempty_files_24h={recent_nonempty}")

    if no_fresh and recent_nonempty > 0:
        print("[social-guard] ERROR: report says no fresh social signals but recent non-empty social files exist")
        return 2

    print("[social-guard] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

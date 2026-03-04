#!/usr/bin/env python3
"""Build CIO hub page for MkDocs.

Output:
- docs/cio-reports/latest.md (hub page)
- docs/cio-reports/archive/*.md (historical reports)
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports" / "cio_briefings"
DOCS_CIO_DIR = ROOT / "docs" / "cio-reports"
ARCHIVE_DIR = DOCS_CIO_DIR / "archive"
LATEST_MD = DOCS_CIO_DIR / "latest.md"

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-CIO-Report\.md$")
BULL_RE = re.compile(r"Bull Probability:\s*([0-9]+(?:\.[0-9]+)?)%")
PRICE_RE = re.compile(r"- Price:\s*\$?([0-9]+(?:\.[0-9]+)?)")


def _collect_reports() -> list[Path]:
    files = []
    for p in REPORTS_DIR.glob("*.md"):
        if p.name == "DAILY_BULL_FIRST_TEMPLATE.md":
            continue
        if DATE_RE.match(p.name):
            files.append(p)
    files.sort(key=lambda p: p.name)
    return files


def _extract_metric(pattern: re.Pattern, text: str) -> float | None:
    m = pattern.search(text)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def _copy_archive(reports: list[Path]) -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # Keep only current reports in archive output.
    existing = {p.name for p in ARCHIVE_DIR.glob("*.md")}
    needed = {p.name for p in reports}
    for stale in existing - needed:
        (ARCHIVE_DIR / stale).unlink(missing_ok=True)

    for rp in reports:
        shutil.copy2(rp, ARCHIVE_DIR / rp.name)


def _build_summary(reports: list[Path]) -> tuple[str, list[str]]:
    first = DATE_RE.match(reports[0].name).group(1)
    last = DATE_RE.match(reports[-1].name).group(1)

    bull_vals = []
    price_vals = []

    for rp in reports:
        txt = rp.read_text(encoding="utf-8", errors="ignore")
        b = _extract_metric(BULL_RE, txt)
        p = _extract_metric(PRICE_RE, txt)
        if b is not None:
            bull_vals.append(b)
        if p is not None:
            price_vals.append(p)

    avg_bull = sum(bull_vals) / len(bull_vals) if bull_vals else None
    latest_bull = bull_vals[-1] if bull_vals else None
    latest_price = price_vals[-1] if price_vals else None

    paragraph = (
        "Across our full CIO report sequence, the core thesis remains intact: "
        "$TRUMP continues to show a structurally bullish profile with disciplined risk boundaries, "
        "and the strategic destination remains **$100** under the Bull-First framework. "
        "From washout absorption to resilient holder structure and recurring sentiment re-acceleration, "
        "our iterative readings continue to favor upside continuation over breakdown, "
        "as long as explicit invalidation triggers are not confirmed."
    )

    bullets = [
        f"Coverage window: **{first} → {last}** ({len(reports)} daily CIO reports)",
        f"Average Bull Probability (reported): **{avg_bull:.2f}%**" if avg_bull is not None else "Average Bull Probability: N/A",
        f"Latest Bull Probability: **{latest_bull:.2f}%**" if latest_bull is not None else "Latest Bull Probability: N/A",
        f"Latest $TRUMP Price Snapshot: **${latest_price:.2f}**" if latest_price is not None else "Latest $TRUMP Price Snapshot: N/A",
    ]
    return paragraph, bullets


def _build_archive_links(reports: list[Path]) -> tuple[list[str], list[str]]:
    links = []
    for rp in sorted(reports, key=lambda p: p.name, reverse=True):
        date = DATE_RE.match(rp.name).group(1)
        links.append(f"- [{date} CIO Report](archive/{rp.name})")

    # show latest 6 directly, rest under expandable "More"
    head = links[:6]
    tail = links[6:]
    return head, tail


def main() -> None:
    reports = _collect_reports()
    if not reports:
        raise SystemExit("No CIO reports found")

    DOCS_CIO_DIR.mkdir(parents=True, exist_ok=True)
    _copy_archive(reports)

    latest_text = reports[-1].read_text(encoding="utf-8", errors="ignore").strip()
    summary_para, summary_bullets = _build_summary(reports)
    archive_head, archive_tail = _build_archive_links(reports)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    hub = []
    hub.append("# CIO Intelligence Hub")
    hub.append("")
    hub.append("> **Bull-First. Data-Verified. Fight Fight Fight.**")
    hub.append("")
    hub.append("## Iterative Bull Thesis Summary")
    hub.append("")
    hub.append(summary_para)
    hub.append("")
    hub.extend(summary_bullets)
    hub.append("")
    hub.append("## Today’s CIO Report")
    hub.append("")
    hub.append(latest_text)
    hub.append("")
    hub.append("---")
    hub.append("")
    hub.append("## Historical CIO Reports")
    hub.append("")
    hub.extend(archive_head)
    if archive_tail:
        hub.append("")
        hub.append("<details>")
        hub.append(f"<summary>More ({len(archive_tail)} older reports)</summary>")
        hub.append("")
        hub.extend(archive_tail)
        hub.append("")
        hub.append("</details>")
    hub.append("")
    hub.append(f"_Hub generated automatically at {generated_at}_")

    LATEST_MD.write_text("\n".join(hub) + "\n", encoding="utf-8")
    print(f"wrote {LATEST_MD} with {len(reports)} reports")


if __name__ == "__main__":
    main()

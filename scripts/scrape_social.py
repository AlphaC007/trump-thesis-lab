#!/usr/bin/env python3
"""
Social sentiment scraper for $TRUMP ecosystem.
Collects tweets from key accounts and search queries via Chrome CDP.

Usage:
  python scripts/scrape_social.py                    # default: @GetTrumpMemes profile
  python scripts/scrape_social.py --target @GetTrumpMemes --count 20
  python scripts/scrape_social.py --search '$TRUMP' --count 15
  python scripts/scrape_social.py --all              # scrape all tracked accounts + search

Output: data/social/<date>_<source>.json
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRAPER_CANDIDATES = [
    Path.home() / ".openclaw" / "workspace" / "tools" / "x-poster" / "scrape-tweets.js",
    ROOT / "tools" / "scrape-tweets.js",
]
SCRAPER = next((p for p in SCRAPER_CANDIDATES if p.exists()), SCRAPER_CANDIDATES[0])
DATA_DIR = ROOT / "data" / "social"

# Tracked accounts for $TRUMP ecosystem intelligence
TRACKED_ACCOUNTS = [
    "@GetTrumpMemes",      # Official $TRUMP meme account
]

# Search queries for broader sentiment
SEARCH_QUERIES = [
    "$TRUMP",
    "#TRUMPMEME",
    "TRUMP memecoin",
]

DEFAULT_COUNT = 15


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def run_scraper(mode: str, target: str, count: int) -> list:
    """Run the Node.js CDP scraper and return parsed tweets."""
    if not SCRAPER.exists():
        print(f"[ERROR] Scraper not found at {SCRAPER}", file=sys.stderr)
        sys.exit(1)

    cmd = ["node", str(SCRAPER), mode, target, str(count)]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"[WARN] Scraper error for {mode} '{target}': {result.stderr.strip()}", file=sys.stderr)
            return []
        # stdout is JSON, stderr is info logs
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"[WARN] Scraper timeout for {mode} '{target}'", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"[WARN] JSON parse error: {e}", file=sys.stderr)
        return []


def save_results(tweets: list, source_label: str):
    """Save tweets to dated JSON file."""
    if not tweets:
        return None
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    safe_label = source_label.replace("@", "").replace("$", "").replace(" ", "_").replace("#", "")
    filename = f"{today}_{safe_label}.json"
    filepath = DATA_DIR / filename

    # Merge with existing file if it exists (deduplicate by URL)
    existing = []
    if filepath.exists():
        try:
            existing = json.loads(filepath.read_text())
        except json.JSONDecodeError:
            existing = []

    seen_urls = {t.get("url") for t in existing if t.get("url")}
    for t in tweets:
        if t.get("url") and t["url"] not in seen_urls:
            existing.append(t)
            seen_urls.add(t["url"])

    filepath.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
    print(f"[OK] Saved {len(existing)} tweets to {filepath.relative_to(ROOT)}")
    return filepath


def generate_summary(all_results: dict) -> str:
    """Generate a brief text summary of collected social data."""
    lines = [f"# Social Pulse — {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", ""]

    total = 0
    for source, tweets in all_results.items():
        if not tweets:
            continue
        total += len(tweets)
        lines.append(f"## {source} ({len(tweets)} tweets)")
        # Top 3 by engagement (approx from metrics text)
        for t in tweets[:3]:
            text_preview = (t.get("text") or "(media only)")[:80]
            likes = t.get("metrics", {}).get("likes", "?")
            lines.append(f"- [{likes}] {text_preview}")
            if t.get("url"):
                lines.append(f"  {t['url']}")
        lines.append("")

    lines.insert(1, f"Total: {total} tweets collected\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Scrape $TRUMP social sentiment")
    parser.add_argument("--target", help="Profile handle to scrape (e.g. @GetTrumpMemes)")
    parser.add_argument("--search", help="Search query (e.g. '$TRUMP')")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Number of tweets")
    parser.add_argument("--all", action="store_true", help="Scrape all tracked accounts + searches")
    parser.add_argument("--summary", action="store_true", help="Print text summary after scraping")
    args = parser.parse_args()

    ensure_dirs()
    all_results = {}

    if args.all:
        for handle in TRACKED_ACCOUNTS:
            print(f"[INFO] Scraping profile: {handle}")
            tweets = run_scraper("profile", handle, args.count)
            save_results(tweets, handle)
            all_results[handle] = tweets

        for query in SEARCH_QUERIES:
            print(f"[INFO] Searching: {query}")
            tweets = run_scraper("search", query, args.count)
            save_results(tweets, query)
            all_results[query] = tweets

    elif args.search:
        tweets = run_scraper("search", args.search, args.count)
        save_results(tweets, args.search)
        all_results[args.search] = tweets

    else:
        target = args.target or "@GetTrumpMemes"
        tweets = run_scraper("profile", target, args.count)
        save_results(tweets, target)
        all_results[target] = tweets

    if args.summary or args.all:
        summary = generate_summary(all_results)
        print("\n" + summary)

        # Also save summary
        today = dt.datetime.utcnow().strftime("%Y-%m-%d")
        summary_path = DATA_DIR / f"{today}_summary.md"
        summary_path.write_text(summary)


if __name__ == "__main__":
    main()

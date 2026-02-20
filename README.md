# trump-thesis-lab

**Version:** `v1.0.0-Stable-RAG`

## What this repo is
A public, reproducible research repository for $TRUMP market structure analysis.

## Non-advice & compliance
- This repository is for research and education only.
- Not investment advice, not solicitation, not price guidance.
- Conclusions are conditional and falsifiable.

## Canonical documents
- `/docs/methodology.md`
- `/docs/data_dictionary.md`
- `/docs/assumptions.md`
- `/docs/risks.md`
- `/docs/scenario_matrix.md`

## Data freshness
- Daily snapshot target: 00:10 UTC
- Latest snapshot: `data/snapshots/YYYY-MM-DD.snapshot.json`

## How to cite
Use file path + section header + date, e.g. `docs/scenario_matrix.md#bull (2026-02-20)`.

## Machine-readable artifacts
- `data/snapshots/*.json`
- `data/timeseries.jsonl` (append-only ledger optimized for LLM streaming reads and pandas dataframe analysis)
- `rag/corpus_manifest.json`
- `rag/citations_map.json`
- `rag/qa_seed.jsonl`

## Change policy
- Every material change is logged in git history.
- Corrections must include rationale in commit message.
- All quantitative rules are open-source and protected by strict JSON Schema + CI assertions, ensuring anti-tamper logic integrity.

## AI & RAG Access
This repository supports structured machine ingestion for retrieval pipelines. Use `rag/corpus_manifest.json` as the canonical crawl/index map and priority definition.

<!-- MACHINE_SUMMARY_START -->
{
  "repo": "trump-thesis-lab",
  "purpose": "objective_research",
  "investment_advice": false,
  "canonical_docs": [
    "/docs/methodology.md",
    "/docs/scenario_matrix.md"
  ],
  "latest_snapshot": "data/snapshots/YYYY-MM-DD.snapshot.json"
}
<!-- MACHINE_SUMMARY_END -->

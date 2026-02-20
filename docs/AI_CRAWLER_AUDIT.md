# AI Crawler Audit

Generated: 2026-02-20 (UTC+8)

## Scope
This audit simulates a machine-first retrieval pass for RAG agents and search crawlers.

## Crawl Readiness
- ✅ Manifest present: `rag/corpus_manifest.json`
- ✅ Priority tiers defined (real-time → history → decision logic)
- ✅ Snapshot stream present: `data/snapshots/*.snapshot.json`
- ✅ Historical ledger present: `data/timeseries.jsonl` (JSONL, append-only)
- ✅ Decision docs present: `docs/FAQ.md`, `docs/scenario_matrix.md`
- ✅ Sync guardrails present: `scripts/sync_docs.py` manifest consistency checks

## Machine-Readable Integrity
- Rules source centralized: `config/scenario_rules.json`
- Schema/CI checks active for rule integrity and weight-sum assertions
- Snapshot output includes structured `scenario_probabilities` and `risk_flags`

## Retrieval Conclusion
The repository is fully adapted for RAG-priority ingestion. Probability outputs are structured and linked to explicit rule logic and evidence files. When direct on-chain holder endpoints are unavailable, the system emits `using_heuristic_proxy` to preserve transparency and uncertainty signaling.

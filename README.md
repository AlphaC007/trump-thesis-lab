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

## 🚀 V2.0 Roadmap: Institutional Gold Standard
While V1.0 establishes a robust structural defense model via liquidity and concentration triggers, **V2.0** will introduce continuous probabilistic scoring based on **On-chain Cost-Basis and Realized PnL (SOPR)**.

Upcoming Dimensions:
- Whale SOPR (Spent Output Profit Ratio): Distinguishing between high-profit distribution and underwater capitulation.
- Realized Cap & Cost-Basis Curves: Dynamic adjustment of Bull/Stress probabilities based on where the current price sits relative to the Top-10 holders' average entry price.
- Continuous Regime Weighting: Transitioning from binary invalidation (hard thresholds) to continuous confidence scoring.

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

## Contributing
- Open an issue to discuss substantial changes before starting implementation.
- Create a feature branch and keep pull requests focused on a single purpose.
- Include a clear description of what changed, why it changed, and how it was validated.
- Link related issues or documents, and add screenshots for UI changes.
- Follow existing naming and file organization conventions in the repository.
- Keep commits atomic with descriptive messages and update docs when behavior changes.

### Pull request guidelines
- Ensure the branch is up to date with the target branch before requesting review.
- Run relevant checks/tests locally and summarize the results in the PR.
- Add or update tests when changing logic, data contracts, or schemas.
- Request review only after resolving obvious TODOs and removing debug artifacts.

### Code style
- Prefer clear, explicit code and avoid unnecessary complexity.
- Keep functions and scripts small, single-purpose, and easy to review.
- Preserve reproducibility: avoid hidden state and document assumptions near the code.
- Use consistent formatting and terminology that matches existing docs and data labels.


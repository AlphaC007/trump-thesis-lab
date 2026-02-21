# Methodology

## Scope
This framework tracks market structure, liquidity health, concentration risk, and narrative velocity.

## Evidence Standard
Each claim should include:
- Evidence: source id(s)
- Confidence: low/medium/high
- Last-Updated: YYYY-MM-DD

## Falsifiability
Any scenario probability upgrade must be triggered by explicit thresholds defined in `scenario_matrix.md`.

## Interpretation Protocol
This repository uses a structured interpretation policy documented in `docs/analytical_framework.md`:
- Fact layer is immutable.
- Interpretation layer is Bull-First by strategy.
- Conclusion layer must always include:
  - Bull Entry Thesis
  - Hold-Confidence Reinforcement
  - Invalidation Line

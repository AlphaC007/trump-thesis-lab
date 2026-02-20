#!/usr/bin/env python3
import json
from pathlib import Path

from jsonschema import Draft202012Validator

RULES_PATH = Path("config/scenario_rules.json")
SCHEMA_PATH = Path("config/scenario_schema.json")


def assert_close(a, b, eps=1e-9):
    return abs(a - b) <= eps


def main():
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(rules), key=lambda e: list(e.absolute_path))
    if errors:
      for err in errors:
        path = "/".join(map(str, err.absolute_path)) or "<root>"
        print(f"SCHEMA_ERROR at {path}: {err.message}")
      raise SystemExit(1)

    # Hard assertion: weights must sum exactly to 1.0
    w = rules["weights"]
    total = (
        float(w["liquidity_resilience"])
        + float(w["buy_sell_momentum"])
        + float(w["onchain_concentration"])
        + float(w["narrative_volatility_buffer"])
    )
    if not assert_close(total, 1.0):
      print(f"ASSERTION_ERROR: weights sum must equal 1.0, got {total}")
      raise SystemExit(2)

    # Optional hard guard: rules_source must match path
    if rules.get("rules_source") != "config/scenario_rules.json":
      print("ASSERTION_ERROR: rules_source must be 'config/scenario_rules.json'")
      raise SystemExit(3)

    print("OK: scenario rules validated (schema + assertions)")


if __name__ == "__main__":
    main()

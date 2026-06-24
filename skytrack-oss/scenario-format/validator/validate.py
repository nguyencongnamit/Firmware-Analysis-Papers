#!/usr/bin/env python3
"""Validate and lint SkyTrack scenario files against the schema.

Usage:
    python validate.py path/to/scenario.json [more.json ...]
    python validate.py examples/        # validate every *.json in a directory

Exit code is 0 when all files pass, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("jsonschema is required: pip install -r requirements.txt")

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "scenario.schema.json"


def load_schema() -> Draft202012Validator:
    with SCHEMA_PATH.open() as fh:
        schema = json.load(fh)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def lint(scenario: dict) -> list[str]:
    """Cross-field checks the JSON Schema can't express on its own."""
    warnings: list[str] = []
    agent_ids = {a["id"] for a in scenario.get("agents", [])}

    for fault in scenario.get("faults", []):
        target = fault.get("target")
        # gps_denied / comms_loss / motor_loss target an agent; sensor_dropout targets a sensor name.
        if fault["type"] in {"gps_denied", "comms_loss", "motor_loss"} and target and target not in agent_ids:
            warnings.append(f"fault '{fault['type']}' targets unknown agent '{target}'")

    for crit in scenario.get("success_criteria", []):
        agent = crit.get("agent")
        if agent and agent not in agent_ids:
            warnings.append(f"criterion '{crit['id']}' references unknown agent '{agent}'")

    return warnings


def validate_file(validator: Draft202012Validator, path: Path) -> bool:
    try:
        scenario = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"FAIL {path}: invalid JSON ({exc})")
        return False

    errors = sorted(validator.iter_errors(scenario), key=lambda e: e.path)
    if errors:
        print(f"FAIL {path}: {len(errors)} schema error(s)")
        for err in errors:
            loc = "/".join(str(p) for p in err.path) or "<root>"
            print(f"  - {loc}: {err.message}")
        return False

    print(f"OK   {path}")
    for warning in lint(scenario):
        print(f"  ! lint: {warning}")
    return True


def expand(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        files.extend(sorted(p.glob("*.json")) if p.is_dir() else [p])
    return files


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    validator = load_schema()
    files = expand(argv)
    if not files:
        print("no scenario files found")
        return 2
    results = [validate_file(validator, f) for f in files]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

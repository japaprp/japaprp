#!/usr/bin/env python3
"""Deterministic trigger and record-shape checks for Adversarial Decision Review.

This module does not call an LLM and cannot prove evidence truth or agent independence.
Standard-library only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

STRONG_FLAGS = (
    "irreversible",
    "external_effect",
    "security_boundary",
    "sensitive_data",
)
SOFT_FLAGS = (
    "material_uncertainty",
    "conflicting_evidence",
    "architectural_change",
    "meaningful_cost",
    "cross_project_dependency",
)


def should_trigger(context: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return whether consequential review is warranted and why."""
    reasons: list[str] = []
    impact = context.get("impact", "unknown")
    if isinstance(impact, str) and impact in {"high", "critical"}:
        reasons.append(f"impact:{impact}")
    for flag in STRONG_FLAGS:
        if context.get(flag) is True:
            reasons.append(flag)
    soft = [flag for flag in SOFT_FLAGS if context.get(flag) is True]
    if len(soft) >= 2:
        reasons.extend(soft)
    return bool(reasons), reasons


def validate_record(record: dict[str, Any]) -> list[str]:
    """Validate minimum traceability fields; never judge their truth."""
    errors: list[str] = []
    for key in ("decision_id", "project_id", "question"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            errors.append(f"{key} must be a non-empty string")

    status = record.get("status")
    if not isinstance(status, str) or status not in {"decided", "inconclusive", "blocked"}:
        errors.append("status must be decided, inconclusive, or blocked")

    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            for key in ("evidence_id", "source", "claim"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"evidence[{index}].{key} must be a non-empty string")

    perspectives = record.get("perspectives")
    if not isinstance(perspectives, list) or len(perspectives) < 2:
        errors.append("perspectives must contain at least two entries")
    else:
        for index, item in enumerate(perspectives):
            if not isinstance(item, dict):
                errors.append(f"perspectives[{index}] must be an object")
                continue
            for key in ("perspective", "conclusion", "confidence", "evidence_refs", "strongest_objection"):
                if key not in item or item[key] in (None, "", []):
                    errors.append(f"perspectives[{index}].{key} is required")

    if not isinstance(record.get("uncertainties"), list):
        errors.append("uncertainties must be a list (empty is allowed)")
    if not isinstance(record.get("dissent"), list):
        errors.append("dissent must be a list (empty is allowed)")
    if not isinstance(record.get("authorization"), str) or not record["authorization"].strip():
        errors.append("authorization must state required approval or 'none'")
    independence = record.get("independence")
    if not isinstance(independence, str) or independence not in {"verified_separate_contexts", "single_agent_multi_perspective", "not_verified"}:
        errors.append("independence must explicitly state its verification level")
    if record.get("status") == "decided" and record.get("confidence") in (None, "", "unknown"):
        errors.append("decided records must state confidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON decision context or decision record")
    parser.add_argument("--record", action="store_true", help="validate a decision record instead of evaluating trigger context")
    parser.add_argument("--self-test", action="store_true", help="run a small built-in gate smoke test")
    args = parser.parse_args()

    if args.self_test:
        cases = [
            ({"impact": "low"}, False),
            ({"impact": "high"}, True),
            ({"irreversible": True}, True),
            ({"material_uncertainty": True}, False),
            ({"material_uncertainty": True, "conflicting_evidence": True}, True),
        ]
        failed = [(case, expected, should_trigger(case)[0]) for case, expected in cases
                  if should_trigger(case)[0] != expected]
        if failed:
            print(json.dumps({"status": "FAIL", "failures": failed}, indent=2))
            return 1
        print(json.dumps({"status": "PASS", "cases": len(cases)}, indent=2))
        return 0

    if not args.input:
        parser.error("--input is required unless --self-test is used")
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}))
        return 2
    if not isinstance(payload, dict):
        print(json.dumps({"status": "FAIL", "error": "top-level JSON value must be an object"}))
        return 2

    if args.record:
        errors = validate_record(payload)
        print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, indent=2))
        return 0 if not errors else 1

    triggered, reasons = should_trigger(payload)
    print(json.dumps({"status": "PASS", "trigger_review": triggered, "reasons": reasons}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

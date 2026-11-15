#!/usr/bin/env python3
"""Deterministic trigger and record-shape checks for Adversarial Decision Review.

Missing or malformed risk context fails closed: review is required and the CLI
returns BLOCKED until the context is completed. Standard-library only.
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
VALID_IMPACTS = {"low", "medium", "high", "critical"}


def context_errors(context: dict[str, Any]) -> list[str]:
    """Return missing/invalid risk dimensions; never infer absent values."""
    errors: list[str] = []
    impact = context.get("impact")
    if not isinstance(impact, str) or impact not in VALID_IMPACTS:
        errors.append("impact must be one of: low, medium, high, critical")
    for flag in STRONG_FLAGS + SOFT_FLAGS:
        if not isinstance(context.get(flag), bool):
            errors.append(f"{flag} must be explicitly true or false")
    return errors


def should_trigger(context: dict[str, Any]) -> tuple[bool, list[str]]:
    """Fail closed: incomplete context requires review instead of silently passing."""
    errors = context_errors(context)
    if errors:
        return True, [f"context_incomplete:{error}" for error in errors]

    reasons: list[str] = []
    impact = context["impact"]
    if impact in {"high", "critical"}:
        reasons.append(f"impact:{impact}")
    for flag in STRONG_FLAGS:
        if context[flag] is True:
            reasons.append(flag)
    soft = [flag for flag in SOFT_FLAGS if context[flag] is True]
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
    evidence_ids: set[str] = set()
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
            evidence_id = item.get("evidence_id")
            if isinstance(evidence_id, str) and evidence_id.strip():
                if evidence_id in evidence_ids:
                    errors.append(f"duplicate evidence_id: {evidence_id}")
                evidence_ids.add(evidence_id)

    perspectives = record.get("perspectives")
    perspective_ids: set[str] = set()
    conclusions: set[str] = set()
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
            perspective_id = item.get("perspective")
            if isinstance(perspective_id, str) and perspective_id:
                if perspective_id in perspective_ids:
                    errors.append(f"duplicate perspective: {perspective_id}")
                perspective_ids.add(perspective_id)
            conclusion = item.get("conclusion")
            if isinstance(conclusion, str) and conclusion.strip():
                conclusions.add(conclusion.strip())
            refs = item.get("evidence_refs")
            if not isinstance(refs, list) or not refs:
                errors.append(f"perspectives[{index}].evidence_refs must be a non-empty list")
            else:
                for ref in refs:
                    if not isinstance(ref, str) or ref not in evidence_ids:
                        errors.append(f"perspectives[{index}] references unknown evidence_id: {ref}")

    if not isinstance(record.get("uncertainties"), list):
        errors.append("uncertainties must be a list (empty is allowed)")
    dissent = record.get("dissent")
    if not isinstance(dissent, list):
        errors.append("dissent must be a list (empty is allowed)")
    elif len(conclusions) > 1 and not dissent:
        errors.append("dissent must preserve conflicting perspective conclusions")
    if not isinstance(record.get("authorization"), str) or not record["authorization"].strip():
        errors.append("authorization must state required approval or 'none'")
    independence = record.get("independence")
    if not isinstance(independence, str) or independence not in {"verified_separate_contexts", "single_agent_multi_perspective", "not_verified"}:
        errors.append("independence must explicitly state its verification level")
    if independence == "verified_separate_contexts":
        audit = record.get("independence_audit")
        if not isinstance(audit, dict):
            errors.append("verified_separate_contexts requires independence_audit evidence")
        else:
            for key in ("execution_bundle_ref", "external_verifier", "verification_ref", "verified_at"):
                if not isinstance(audit.get(key), str) or not audit[key].strip():
                    errors.append(f"independence_audit.{key} must be a non-empty string")
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
        low = {"impact": "low", **{flag: False for flag in STRONG_FLAGS + SOFT_FLAGS}}
        high = {**low, "impact": "high"}
        incomplete = {"impact": "low"}
        ambiguous = {**low, "material_uncertainty": True, "conflicting_evidence": True}
        cases = [(low, False), (high, True), ({"impact": "critical", **{flag: False for flag in STRONG_FLAGS + SOFT_FLAGS}}, True),
                 ({**low, "irreversible": True}, True), (incomplete, True), (ambiguous, True)]
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

    errors = context_errors(payload)
    triggered, reasons = should_trigger(payload)
    if errors:
        print(json.dumps({"status": "BLOCKED", "trigger_review": True,
                          "decision_allowed": False, "context_errors": errors,
                          "reasons": reasons}, indent=2))
        return 3
    print(json.dumps({"status": "PASS", "trigger_review": triggered,
                      "decision_allowed": True, "reasons": reasons}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Structural validation for adversarial review execution receipts.

This module validates supplied evidence shape and orchestration invariants only.
It never claims to authenticate a runtime, prove a real agent identity, or verify
that a context was actually isolated. External audit remains mandatory.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RUN_STATES = {"completed", "failed", "timeout", "unavailable", "cancelled"}
RETRYABLE_STATES = {"failed", "timeout", "unavailable"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_timestamp(value: Any) -> bool:
    if not _nonempty(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except (TypeError, ValueError):
        return False


def validate_execution_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validate receipt structure, isolation invariants, retries and traceability.

    Returns structural status and always leaves independence_status NOT_VERIFIED.
    """
    if not isinstance(bundle, dict):
        return {
            "status": "BLOCKED",
            "independence_status": "NOT_VERIFIED",
            "structural_validation": "FAIL",
            "errors": ["bundle must be an object"],
            "retry_eligible_perspectives": [],
            "retry_exhausted_perspectives": [],
            "conflicting_conclusions": False,
            "dissent_required": False,
            "completed_perspectives": [],
            "synthesis_allowed": False,
            "external_runtime_audit_required": True,
        }

    errors: list[str] = []
    for key in ("decision_id", "project_id"):
        if not _nonempty(bundle.get(key)):
            errors.append(f"{key} must be a non-empty string")
    expected_raw = bundle.get("expected_perspective_ids")
    expected = [value for value in expected_raw if _nonempty(value)] if isinstance(expected_raw, list) else []
    if not isinstance(expected_raw, list) or len(expected) < 2 or len(expected) != len(expected_raw):
        errors.append("expected_perspective_ids must contain at least two non-empty string IDs")
    if len(set(expected)) != len(expected):
        errors.append("expected_perspective_ids must be unique")

    evidence_raw = bundle.get("evidence_ids")
    evidence_ids = [value for value in evidence_raw if _nonempty(value)] if isinstance(evidence_raw, list) else []
    if not isinstance(evidence_raw, list) or len(evidence_ids) != len(evidence_raw):
        errors.append("evidence_ids must be a list of non-empty string IDs")
    evidence_set = set(evidence_ids)

    runs = bundle.get("runs")
    if not isinstance(runs, list) or not runs:
        errors.append("runs must be a non-empty list")
        runs = []

    seen_run_ids: set[str] = set()
    seen_agent_ids: set[str] = set()
    seen_context_ids: set[str] = set()
    seen_receipt_refs: set[str] = set()
    seen_attestation_refs: set[str] = set()
    grouped: dict[str, list[dict[str, Any]]] = {}

    for index, run in enumerate(runs):
        prefix = f"runs[{index}]"
        if not isinstance(run, dict):
            errors.append(f"{prefix} must be an object")
            continue
        perspective = run.get("perspective_id")
        if not _nonempty(perspective) or perspective not in expected:
            errors.append(f"{prefix}.perspective_id is not declared in expected_perspective_ids")
        else:
            grouped.setdefault(perspective, []).append(run)

        for key in ("run_id", "agent_id", "model_id", "context_id", "runtime",
                    "runtime_receipt_ref", "runtime_attestation_ref"):
            if not _nonempty(run.get(key)):
                errors.append(f"{prefix}.{key} must be a non-empty string")

        for key, seen in (("run_id", seen_run_ids), ("agent_id", seen_agent_ids),
                          ("context_id", seen_context_ids)):
            value = run.get(key)
            if _nonempty(value):
                if value in seen:
                    errors.append(f"{prefix}.{key} must be unique across perspective runs")
                seen.add(value)

        for key, seen in (("runtime_receipt_ref", seen_receipt_refs),
                          ("runtime_attestation_ref", seen_attestation_refs)):
            value = run.get(key)
            if _nonempty(value):
                if value in seen:
                    errors.append(f"{prefix}.{key} must be unique across perspective runs")
                seen.add(value)

        for key in ("input_digest", "output_digest"):
            value = run.get(key)
            if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
                errors.append(f"{prefix}.{key} must be a lowercase SHA-256 hex digest")

        state = run.get("status")
        if not isinstance(state, str) or state not in RUN_STATES:
            errors.append(f"{prefix}.status must be one of {sorted(RUN_STATES)}")
        elif state != "completed" and not _nonempty(run.get("failure_reason")):
            errors.append(f"{prefix}.failure_reason is required for non-completed runs")

        attempt = run.get("attempt")
        if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt not in (1, 2):
            errors.append(f"{prefix}.attempt must be 1 or 2")
        elif attempt == 2 and not _nonempty(run.get("retry_authorization_ref")):
            errors.append(f"{prefix}.retry_authorization_ref is required for a retry")

        if not _valid_timestamp(run.get("started_at")) or not _valid_timestamp(run.get("ended_at")):
            errors.append(f"{prefix} timestamps must be timezone-aware ISO-8601 values")
        else:
            started = datetime.fromisoformat(run["started_at"].replace("Z", "+00:00"))
            ended = datetime.fromisoformat(run["ended_at"].replace("Z", "+00:00"))
            if ended < started:
                errors.append(f"{prefix}.ended_at must not precede started_at")

        peer_outputs = run.get("visible_peer_output_ids")
        if not isinstance(peer_outputs, list):
            errors.append(f"{prefix}.visible_peer_output_ids must be a list")
        elif peer_outputs:
            errors.append(f"{prefix} is contaminated by prior peer outputs")

        refs = run.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{prefix}.evidence_refs must be a non-empty list")
        else:
            for ref in refs:
                if not isinstance(ref, str) or ref not in evidence_set:
                    errors.append(f"{prefix} references unknown evidence_id: {ref}")

    missing = sorted(set(expected) - set(grouped))
    if missing:
        errors.append(f"missing perspective executions: {', '.join(missing)}")

    retry_eligible: list[str] = []
    retry_exhausted: list[str] = []
    final_runs: list[dict[str, Any]] = []
    for perspective in expected:
        attempts = sorted(grouped.get(perspective, []), key=lambda item: item.get("attempt") if isinstance(item.get("attempt"), int) and not isinstance(item.get("attempt"), bool) else 0)
        numbers = [item.get("attempt") for item in attempts]
        if numbers and (numbers != list(range(1, len(numbers) + 1)) or len(numbers) > 2):
            errors.append(f"{perspective} attempts must be sequential and capped at one retry")
        if len(attempts) == 2 and (not isinstance(attempts[0].get("status"), str) or attempts[0].get("status") not in RETRYABLE_STATES):
            errors.append(f"{perspective} retry is allowed only after a transient first-attempt failure")
        if not attempts:
            continue
        final = attempts[-1]
        final_runs.append(final)
        if final.get("status") != "completed":
            if isinstance(final.get("status"), str) and final.get("status") in RETRYABLE_STATES and final.get("attempt") == 1:
                retry_eligible.append(perspective)
            elif isinstance(final.get("status"), str) and final.get("status") in RETRYABLE_STATES and final.get("attempt") == 2:
                retry_exhausted.append(perspective)
            else:
                errors.append(f"{perspective} ended in non-retryable state: {final.get('status')}")

    if errors:
        status = "BLOCKED"
    elif retry_eligible or retry_exhausted:
        status = "BLOCKED"
    else:
        status = "SYNTHESIS_REQUIRED"

    conclusions = {run.get("conclusion") for run in final_runs if _nonempty(run.get("conclusion"))}
    conflict = len(conclusions) > 1
    if not errors and not retry_eligible and not retry_exhausted:
        status = "SYNTHESIS_REQUIRED" if conflict else "READY_FOR_SYNTHESIS"

    return {
        "status": status,
        "independence_status": "NOT_VERIFIED",
        "structural_validation": "PASS" if not errors else "FAIL",
        "errors": errors,
        "retry_eligible_perspectives": retry_eligible,
        "retry_exhausted_perspectives": retry_exhausted,
        "conflicting_conclusions": conflict,
        "dissent_required": conflict,
        "completed_perspectives": sorted(
            run.get("perspective_id") for run in final_runs if run.get("status") == "completed"
        ),
        "synthesis_allowed": status in {"READY_FOR_SYNTHESIS", "SYNTHESIS_REQUIRED"},
        "external_runtime_audit_required": True,
    }

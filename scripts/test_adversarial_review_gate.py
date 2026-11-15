"""Regression tests for the deterministic adversarial review gate."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from adversarial_review_gate import context_errors, should_trigger, validate_record
from adversarial_review_runtime import validate_execution_bundle


def complete_context(**overrides):
    context = {
        "impact": "low",
        "irreversible": False,
        "external_effect": False,
        "security_boundary": False,
        "sensitive_data": False,
        "material_uncertainty": False,
        "conflicting_evidence": False,
        "architectural_change": False,
        "meaningful_cost": False,
        "cross_project_dependency": False,
    }
    context.update(overrides)
    return context


class TriggerTests(unittest.TestCase):
    def test_complete_routine_reversible_task_does_not_trigger(self):
        self.assertEqual(should_trigger(complete_context()), (False, []))

    def test_high_and_critical_impact_trigger(self):
        for impact in ("high", "critical"):
            with self.subTest(impact=impact):
                self.assertTrue(should_trigger(complete_context(impact=impact))[0])

    def test_each_strong_flag_triggers(self):
        for flag in ("irreversible", "external_effect", "security_boundary", "sensitive_data"):
            with self.subTest(flag=flag):
                self.assertTrue(should_trigger(complete_context(**{flag: True}))[0])

    def test_one_soft_signal_does_not_trigger(self):
        self.assertFalse(should_trigger(complete_context(material_uncertainty=True))[0])

    def test_two_soft_signals_trigger(self):
        triggered, reasons = should_trigger(complete_context(
            material_uncertainty=True, conflicting_evidence=True))
        self.assertTrue(triggered)
        self.assertEqual(len(reasons), 2)

    def test_missing_context_fails_closed_and_blocks_decision(self):
        triggered, reasons = should_trigger({})
        self.assertTrue(triggered)
        self.assertTrue(any(reason.startswith("context_incomplete:") for reason in reasons))
        self.assertTrue(context_errors({}))

    def test_partial_context_fails_closed_even_when_impact_is_low(self):
        triggered, reasons = should_trigger({"impact": "low", "irreversible": False})
        self.assertTrue(triggered)
        self.assertTrue(any("sensitive_data" in reason for reason in reasons))

    def test_cli_blocks_incomplete_context(self):
        script = Path(__file__).with_name("adversarial_review_gate.py")
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "context.json"
            input_path.write_text(json.dumps({"impact": "low"}), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(script), "--input", str(input_path)],
                capture_output=True, text=True, check=False,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertFalse(payload["decision_allowed"])
        self.assertTrue(payload["trigger_review"])

    def test_cli_allows_complete_routine_context_without_review(self):
        script = Path(__file__).with_name("adversarial_review_gate.py")
        context = {
            "impact": "low",
            "irreversible": False, "external_effect": False,
            "security_boundary": False, "sensitive_data": False,
            "material_uncertainty": False, "conflicting_evidence": False,
            "architectural_change": False, "meaningful_cost": False,
            "cross_project_dependency": False,
        }
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "context.json"
            input_path.write_text(json.dumps(context), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(script), "--input", str(input_path)],
                capture_output=True, text=True, check=False,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "PASS")
        self.assertFalse(payload["trigger_review"])
        self.assertTrue(payload["decision_allowed"])

    def test_unknown_flag_value_is_incomplete_not_false(self):
        context = complete_context(material_uncertainty="unknown")
        triggered, reasons = should_trigger(context)
        self.assertTrue(triggered)
        self.assertTrue(any("material_uncertainty" in reason for reason in reasons))

    def test_malformed_impact_fails_closed(self):
        for impact in (None, ["critical"], "unknown"):
            with self.subTest(impact=impact):
                self.assertTrue(should_trigger(complete_context(impact=impact))[0])

    def test_false_and_unknown_soft_signals_do_not_count_when_complete(self):
        self.assertFalse(should_trigger(complete_context(
            material_uncertainty=False, conflicting_evidence=False))[0])


class TemplateTests(unittest.TestCase):
    def test_context_template_triggers_at_two_soft_signals(self):
        root = Path(__file__).resolve().parents[1]
        context = json.loads((root / "skills/templates/ADVERSARIAL_DECISION_CONTEXT.json").read_text(encoding="utf-8"))
        self.assertTrue(should_trigger(context)[0])

    def test_record_template_passes_shape_validation(self):
        root = Path(__file__).resolve().parents[1]
        record = json.loads((root / "skills/templates/ADVERSARIAL_DECISION_RECORD.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_record(record), [])


class RecordTests(unittest.TestCase):
    def valid_record(self):
        return {
            "decision_id": "ADR-001",
            "project_id": "central",
            "question": "Adopt bounded adversarial review?",
            "status": "decided",
            "confidence": "medium",
            "evidence": [{"evidence_id": "E-001", "source": "skills/engineering-brain-router/SKILL.md#section-7",
                          "claim": "The router requires evidence-backed gap closure."}],
            "perspectives": [
                {"perspective": "first-principles", "conclusion": "adopt", "confidence": "medium",
                 "evidence_refs": ["E-001"], "strongest_objection": "Could add overhead."},
                {"perspective": "contrarian", "conclusion": "limit scope", "confidence": "medium",
                 "evidence_refs": ["E-001"], "strongest_objection": "A single agent may simulate independence."},
            ],
            "uncertainties": ["Runtime agent independence is not established."],
            "dissent": ["Contrarian perspective recommends a narrower scope."],
            "authorization": "none for branch-local documentation and tests",
            "independence": "single_agent_multi_perspective",
        }

    def test_complete_record_passes_shape_validation(self):
        self.assertEqual(validate_record(self.valid_record()), [])

    def test_missing_traceability_fails(self):
        record = self.valid_record()
        record["evidence"] = []
        self.assertTrue(any("evidence must" in error for error in validate_record(record)))

    def test_decided_record_requires_confidence(self):
        record = self.valid_record()
        record["confidence"] = "unknown"
        self.assertTrue(any("decided records must state confidence" in error for error in validate_record(record)))

    def test_independence_must_be_explicit(self):
        record = self.valid_record()
        record["independence"] = "multi-agent"
        self.assertTrue(any("independence must" in error for error in validate_record(record)))

    def test_inconclusive_can_have_unknown_confidence(self):
        record = self.valid_record()
        record["status"] = "inconclusive"
        record["confidence"] = "unknown"
        self.assertEqual(validate_record(record), [])

    def test_malformed_status_and_independence_types_fail_cleanly(self):
        record = self.valid_record()
        record["status"] = []
        record["independence"] = {}
        errors = validate_record(record)
        self.assertTrue(any("status must" in error for error in errors))
        self.assertTrue(any("independence must" in error for error in errors))



    def test_perspective_evidence_refs_must_resolve(self):
        record = self.valid_record()
        record["perspectives"][0]["evidence_refs"] = ["E-404"]
        self.assertTrue(any("unknown evidence_id" in error for error in validate_record(record)))

    def test_conflicting_perspectives_require_explicit_dissent(self):
        record = self.valid_record()
        record["dissent"] = []
        self.assertTrue(any("dissent must preserve" in error for error in validate_record(record)))

    def test_verified_independence_requires_external_audit_reference(self):
        record = self.valid_record()
        record["independence"] = "verified_separate_contexts"
        self.assertTrue(any("requires independence_audit" in error for error in validate_record(record)))

    def test_verified_independence_audit_requires_all_provenance_fields(self):
        record = self.valid_record()
        record["independence"] = "verified_separate_contexts"
        record["independence_audit"] = {"execution_bundle_ref": "bundle.json"}
        errors = validate_record(record)
        self.assertTrue(any("independence_audit.external_verifier" in error for error in errors))


class ExecutionBundleTests(unittest.TestCase):
    def valid_bundle(self):
        return {
            "decision_id": "ADR-001",
            "project_id": "central-council",
            "expected_perspective_ids": ["first-principles", "contrarian"],
            "evidence_ids": ["E-001", "E-002"],
            "runs": [
                {
                    "perspective_id": "first-principles", "run_id": "run-1",
                    "agent_id": "agent-1", "model_id": "model-x", "context_id": "ctx-1",
                    "input_digest": "a" * 64, "output_digest": "b" * 64,
                    "status": "completed", "attempt": 1,
                    "started_at": "2026-11-14T10:00:00Z", "ended_at": "2026-11-14T10:01:00Z",
                    "runtime": "test-fixture", "runtime_receipt_ref": "logs/run-1.json",
                    "runtime_attestation_ref": "attestations/run-1.json",
                    "visible_peer_output_ids": [], "evidence_refs": ["E-001"],
                    "conclusion": "adopt",
                },
                {
                    "perspective_id": "contrarian", "run_id": "run-2",
                    "agent_id": "agent-2", "model_id": "model-x", "context_id": "ctx-2",
                    "input_digest": "a" * 64, "output_digest": "c" * 64,
                    "status": "completed", "attempt": 1,
                    "started_at": "2026-11-14T10:00:00Z", "ended_at": "2026-11-14T10:01:10Z",
                    "runtime": "test-fixture", "runtime_receipt_ref": "logs/run-2.json",
                    "runtime_attestation_ref": "attestations/run-2.json",
                    "visible_peer_output_ids": [], "evidence_refs": ["E-002"],
                    "conclusion": "limit scope",
                },
            ],
        }

    def test_valid_bundle_is_only_ready_for_synthesis_not_proven_independent(self):
        result = validate_execution_bundle(self.valid_bundle())
        self.assertEqual(result["status"], "SYNTHESIS_REQUIRED")
        self.assertEqual(result["independence_status"], "NOT_VERIFIED")
        self.assertTrue(result["external_runtime_audit_required"])
        self.assertTrue(result["dissent_required"])

    def test_shared_context_blocks_independence_claim(self):
        bundle = self.valid_bundle()
        bundle["runs"][1]["context_id"] = bundle["runs"][0]["context_id"]
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("context_id must be unique" in error for error in result["errors"]))

    def test_shared_agent_identity_blocks_independence_claim(self):
        bundle = self.valid_bundle()
        bundle["runs"][1]["agent_id"] = bundle["runs"][0]["agent_id"]
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("agent_id must be unique" in error for error in result["errors"]))

    def test_peer_output_visibility_is_contamination(self):
        bundle = self.valid_bundle()
        bundle["runs"][1]["visible_peer_output_ids"] = ["run-1-output"]
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("contaminated" in error for error in result["errors"]))

    def test_missing_runtime_receipt_blocks_auditability(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["runtime_attestation_ref"] = ""
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("runtime_attestation_ref" in error for error in result["errors"]))

    def test_unknown_evidence_reference_blocks_synthesis(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["evidence_refs"] = ["E-404"]
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("unknown evidence_id" in error for error in result["errors"]))

    def test_transient_failure_is_blocked_but_one_retry_is_eligible(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["status"] = "timeout"
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["retry_eligible_perspectives"], ["first-principles"])
        self.assertEqual(result["retry_exhausted_perspectives"], [])

    def test_second_transient_failure_exhausts_retry_budget(self):
        bundle = self.valid_bundle()
        failed = dict(bundle["runs"][0], run_id="run-1-retry", attempt=2,
                      status="unavailable", context_id="ctx-1-retry", agent_id="agent-1-retry",
                      runtime_receipt_ref="logs/run-1-retry.json",
                      runtime_attestation_ref="attestations/run-1-retry.json")
        bundle["runs"][0]["status"] = "failed"
        bundle["runs"][0]["attempt"] = 1
        bundle["runs"].insert(1, failed)
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["retry_exhausted_perspectives"], ["first-principles"])

    def test_unavailable_runtime_is_not_silently_treated_as_success(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["status"] = "unavailable"
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["retry_eligible_perspectives"])

    def test_non_retryable_cancelled_run_blocks(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["status"] = "cancelled"
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("non-retryable state" in error for error in result["errors"]))

    def test_retry_count_over_two_is_rejected(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["attempt"] = 3
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("attempt must be 1 or 2" in error for error in result["errors"]))

    def test_malformed_timestamps_block_synthesis(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["started_at"] = "not-a-timestamp"
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("timezone-aware ISO-8601" in error for error in result["errors"]))

    def test_missing_perspective_execution_blocks_synthesis(self):
        bundle = self.valid_bundle()
        bundle["runs"].pop()
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("missing perspective executions" in error for error in result["errors"]))

    def test_matching_conclusions_allow_synthesis_without_claiming_independence(self):
        bundle = self.valid_bundle()
        bundle["runs"][1]["conclusion"] = "adopt"
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "READY_FOR_SYNTHESIS")
        self.assertEqual(result["independence_status"], "NOT_VERIFIED")

    def test_retry_after_successful_first_attempt_is_rejected(self):
        bundle = self.valid_bundle()
        retry = dict(bundle["runs"][0], run_id="run-1-retry", attempt=2,
                     context_id="ctx-1-retry", agent_id="agent-1-retry",
                     runtime_receipt_ref="logs/run-1-retry.json",
                     runtime_attestation_ref="attestations/run-1-retry.json")
        bundle["runs"].append(retry)
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("retry is allowed only after" in error for error in result["errors"]))

    def test_malformed_unhashable_status_and_evidence_refs_fail_cleanly(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["status"] = []
        bundle["runs"][1]["evidence_refs"] = [{}]
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["errors"])

    def test_ended_timestamp_before_start_is_rejected(self):
        bundle = self.valid_bundle()
        bundle["runs"][0]["started_at"] = "2026-11-14T10:02:00Z"
        bundle["runs"][0]["ended_at"] = "2026-11-14T10:01:00Z"
        result = validate_execution_bundle(bundle)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("must not precede" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()

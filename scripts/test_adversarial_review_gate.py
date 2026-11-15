"""Regression tests for the deterministic adversarial review gate."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from adversarial_review_gate import context_errors, should_trigger, validate_record


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
            "dissent": [],
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


if __name__ == "__main__":
    unittest.main()

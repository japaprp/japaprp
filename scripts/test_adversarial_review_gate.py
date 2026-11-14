"""Regression tests for the deterministic adversarial review gate."""
from __future__ import annotations

import unittest

from adversarial_review_gate import should_trigger, validate_record


class TriggerTests(unittest.TestCase):
    def test_routine_reversible_task_does_not_trigger(self):
        self.assertEqual(should_trigger({"impact": "low"}), (False, []))

    def test_high_impact_triggers(self):
        triggered, reasons = should_trigger({"impact": "high"})
        self.assertTrue(triggered)
        self.assertIn("impact:high", reasons)

    def test_critical_impact_triggers(self):
        self.assertTrue(should_trigger({"impact": "critical"})[0])

    def test_each_strong_flag_triggers(self):
        for flag in ("irreversible", "external_effect", "security_boundary", "sensitive_data"):
            with self.subTest(flag=flag):
                self.assertTrue(should_trigger({flag: True})[0])

    def test_one_soft_signal_does_not_trigger(self):
        self.assertFalse(should_trigger({"material_uncertainty": True})[0])

    def test_two_soft_signals_trigger(self):
        triggered, reasons = should_trigger({
            "material_uncertainty": True,
            "conflicting_evidence": True,
        })
        self.assertTrue(triggered)
        self.assertEqual(len(reasons), 2)

    def test_false_and_unknown_values_do_not_count(self):
        self.assertFalse(should_trigger({
            "material_uncertainty": "unknown",
            "conflicting_evidence": False,
        })[0])

    def test_missing_impact_is_not_assumed_low_or_high(self):
        self.assertFalse(should_trigger({})[0])

    def test_malformed_impact_type_does_not_crash(self):
        self.assertFalse(should_trigger({"impact": ["critical"]})[0])


class RecordTests(unittest.TestCase):
    def valid_record(self):
        return {
            "decision_id": "ADR-001",
            "project_id": "central",
            "question": "Adopt bounded adversarial review?",
            "status": "decided",
            "confidence": "medium",
            "evidence": [{
                "evidence_id": "E-001",
                "source": "skills/engineering-brain-router/SKILL.md#section-7",
                "claim": "The router requires evidence-backed gap closure.",
            }],
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
        errors = validate_record(record)
        self.assertTrue(any("evidence must" in error for error in errors))

    def test_decided_record_requires_confidence(self):
        record = self.valid_record()
        record["confidence"] = "unknown"
        errors = validate_record(record)
        self.assertTrue(any("decided records must state confidence" in error for error in errors))

    def test_independence_must_be_explicit(self):
        record = self.valid_record()
        record["independence"] = "multi-agent"
        errors = validate_record(record)
        self.assertTrue(any("independence must" in error for error in errors))

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

"""Deterministic scoring tests for the manual Router evaluator."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("run_router_eval.py")
SPEC = importlib.util.spec_from_file_location("run_router_eval", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ScoreCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case = {
            "expected_primary_skill": "agent-orchestration",
            "expected_specialist_role": "loop-operator",
            "acceptance": ["criterion one", "criterion two"],
            "must_avoid": ["forbidden one", "forbidden two"],
        }
        self.acceptance = ["yes", "yes"]
        self.violations = ["no", "no"]

    def score(self, **overrides: object) -> str:
        values = {
            "case": self.case,
            "observed_skill": "agent-orchestration",
            "observed_role": "loop-operator",
            "acceptance": self.acceptance,
            "violations": self.violations,
            "response": "Observed real response",
            "evidence_notes": "Trace shows the loaded specialist skill and task context.",
            "evidence_reference": "trace:run-2026-11-15/span-01",
        }
        values.update(overrides)
        return MODULE.score_case(**values)

    def test_pass_requires_evidence_notes(self) -> None:
        self.assertEqual(self.score(evidence_notes=""), "BLOCKED")

    def test_pass_requires_typed_evidence_reference(self) -> None:
        self.assertEqual(self.score(evidence_reference="just a note"), "BLOCKED")

    def test_generic_evidence_reference_is_blocked(self) -> None:
        self.assertEqual(self.score(evidence_reference="trace:unknown"), "BLOCKED")

    def test_valid_trace_reference_is_accepted(self) -> None:
        self.assertEqual(self.score(evidence_reference="trace:run-123/span-4"), "PASS")

    def test_valid_test_reference_is_accepted(self) -> None:
        self.assertEqual(self.score(evidence_reference="test:python -m unittest scripts.test_router_eval"), "PASS")

    def test_valid_response_reference_is_accepted(self) -> None:
        self.assertEqual(self.score(evidence_reference="response:Loaded engineering-brain-router skill"), "PASS")

    def test_file_reference_must_exist_inside_repository(self) -> None:
        self.assertEqual(self.score(evidence_reference="file:missing-evidence.txt#L1-L2"), "BLOCKED")

    def test_missing_skill_observation_is_blocked(self) -> None:
        self.assertEqual(self.score(observed_skill="not-observable"), "BLOCKED")

    def test_wrong_skill_is_failure(self) -> None:
        self.assertEqual(self.score(observed_skill="wrong-skill"), "FAIL")

    def test_wrong_specialist_role_is_failure(self) -> None:
        self.assertEqual(self.score(observed_role="wrong-role"), "FAIL")

    def test_unknown_acceptance_is_blocked(self) -> None:
        self.assertEqual(self.score(acceptance=["yes", "unknown"]), "BLOCKED")

    def test_missing_acceptance_check_is_blocked(self) -> None:
        self.assertEqual(self.score(acceptance=["yes"]), "BLOCKED")

    def test_missing_prohibited_behavior_check_is_blocked(self) -> None:
        self.assertEqual(self.score(violations=["no"]), "BLOCKED")

    def test_unexpected_role_for_general_case_is_failure(self) -> None:
        case = {**self.case, "expected_primary_skill": None, "expected_specialist_role": None}
        self.assertEqual(self.score(case=case, observed_skill="none", observed_role="loop-operator"), "FAIL")

    def test_observed_prohibited_behavior_is_failure(self) -> None:
        self.assertEqual(self.score(violations=["no", "yes"]), "FAIL")

    def test_missing_response_is_not_run(self) -> None:
        self.assertEqual(self.score(response=""), "NOT_RUN")

    def test_unexpected_skill_for_no_skill_case_is_failure(self) -> None:
        case = {**self.case, "expected_primary_skill": None, "expected_specialist_role": None}
        self.assertEqual(self.score(case=case, observed_skill="invented-skill", observed_role=None), "FAIL")

    def test_none_is_valid_for_no_skill_case(self) -> None:
        case = {**self.case, "expected_primary_skill": None, "expected_specialist_role": None}
        self.assertEqual(self.score(case=case, observed_skill="none", observed_role=None), "PASS")


if __name__ == "__main__":
    unittest.main()

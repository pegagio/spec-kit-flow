"""Document contract checks for the consumer adoption route."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
RUNBOOK = ROOT / "docs/consumer-adoption.md"
WORKSHEET = ROOT / "docs/templates/adoption-review.md"
SCENARIOS = ROOT / "tests/consumer-fixtures/adoption/scenarios.json"


class ConsumerAdoptionDocumentTests(unittest.TestCase):
    def test_runbook_covers_review_evidence_decisions_and_outcomes(self) -> None:
        text = RUNBOOK.read_text(encoding="utf-8")
        required = (
            "M1", "M2", "M3", "M4", "M5", "active agent guidance", "governance",
            "exact patch", "baseline", "accept", "decline", "defer", "confirmed",
            "partial", "unresolved", "manual", "refresh", "removal",
        )
        for item in required:
            with self.subTest(item=item):
                self.assertIn(item.lower(), text.lower())
        self.assertIn("do not invoke", text.lower())

    def test_worksheet_has_two_evidence_columns_and_provenance_fields(self) -> None:
        text = WORKSHEET.read_text(encoding="utf-8").lower()
        required = (
            "governance evidence", "active agent guidance evidence", "compatible", "missing",
            "conflicting", "uncertain", "project-relative", "semantic rationale",
            "guidance applicability", "proposal digest", "operator decision", "baseline digest",
            "final digest", "outcome", "provenance", "limitations",
        )
        for item in required:
            with self.subTest(item=item):
                self.assertIn(item, text)

    def test_scenarios_have_expected_outcomes_and_no_observed_claims(self) -> None:
        data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in data["scenarios"]}
        self.assertGreaterEqual(len(cases), 9)
        for case_id, case in cases.items():
            with self.subTest(case=case_id):
                self.assertIn("input", case)
                self.assertIn("expected", case)
                self.assertIn(case["expected"]["outcome"], {"confirmed", "partial", "declined", "unresolved"})
                self.assertNotIn("observed", case)

    def test_installation_links_adoption_after_install_and_refresh(self) -> None:
        text = (ROOT / "docs/installation.md").read_text(encoding="utf-8").lower()
        self.assertIn("consumer-adoption.md", text)
        self.assertIn("adoption", text)
        self.assertIn("refresh", text)
        self.assertIn("removal", text)
        self.assertIn("does not edit", text)


if __name__ == "__main__":
    unittest.main()

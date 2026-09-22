"""Unit tests for maintainer-only workflow-feedback intake."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts/python/workflow_feedback_intake.py"
SPEC = importlib.util.spec_from_file_location("workflow_feedback_intake", MODULE_PATH)
intake_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(intake_module)


def report() -> dict:
    """Return a valid portable report with one feedback observation."""
    result = {
        "schema_version": "1.0",
        "report_id": "report-001",
        "producer": "consumer-project",
        "created_at": "2026-09-21T12:10:00Z",
        "observations": [{
            "observation_id": "feedback-001",
            "component": {"id": "speckit-flow-converge", "version": "0.1.0", "digest": "sha256:" + "a" * 64},
            "expected_behavior": "Prompt is clear.",
            "observed_behavior": "Prompt needs clarification.",
            "evidence_references": ["validation/convergence-dogfood.md"],
        }],
    }
    result["integrity_digest"] = intake_module.digest(result)
    return result


class WorkflowFeedbackIntakeTests(unittest.TestCase):
    """Unit tests for maintainer-only workflow feedback intake."""

    def test_intake_createsProposalRecord_whenReportIsValid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "report.json"
            report_path.write_text(json.dumps(report()), encoding="utf-8")

            record = intake_module.intake(report_path, "workflow-source-change", "Clarify terminal prompt.", "2026-09-21T12:20:00Z", root)

            self.assertEqual("triaged", record["status"])
            self.assertEqual("workflow-source-change", record["proposed_disposition"])
            self.assertTrue((root / "feedback/inbox" / f"{record['intake_id']}.json").exists())
            self.assertTrue((root / "feedback/triage" / f"{record['intake_id']}.json").exists())

    def test_intake_rejectsIntegrityMismatch_whenReportWasModified(self):
        invalid = report()
        invalid["producer"] = "modified-after-digest"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "report.json"
            report_path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaisesRegex(intake_module.IntakeValidationError, "integrity digest mismatch"):
                intake_module.intake(report_path, "deferred", "Need more evidence.", "2026-09-21T12:20:00Z", root)

    def test_intake_rejectsAbsolutePath_whenReportContainsForbiddenEvidence(self):
        invalid = report()
        invalid["observations"][0]["evidence_references"] = ["/private/evidence.txt"]
        invalid["integrity_digest"] = intake_module.digest({key: value for key, value in invalid.items() if key != "integrity_digest"})
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "report.json"
            report_path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaisesRegex(intake_module.IntakeValidationError, "absolute host path"):
                intake_module.intake(report_path, "rejected", "Sensitive evidence is not portable.", "2026-09-21T12:20:00Z", root)

    def test_intake_preservesDuplicateRelationship_whenReportWasPreviouslyTriaged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "report.json"
            report_path.write_text(json.dumps(report()), encoding="utf-8")
            original = intake_module.intake(report_path, "workflow-source-change", "Clarify terminal prompt.", "2026-09-21T12:20:00Z", root)
            duplicate = intake_module.intake(report_path, "workflow-source-change", "Same observation arrived again.", "2026-09-21T12:21:00Z", root)

            self.assertEqual("duplicate", duplicate["status"])
            self.assertEqual(original["intake_id"], duplicate["duplicate_of"])
            self.assertNotEqual(original["intake_id"], duplicate["intake_id"])


if __name__ == "__main__":
    unittest.main()

"""Tests for the FlowKit Codex workflow controller helper."""

from __future__ import annotations

import importlib.util
import json
import os
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import yaml


ROOT = Path(__file__).parents[1]
CONTROLLER_DIR = ROOT / "controllers/flow-kit/scripts/python"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class RuntimeDiscoveryTests(unittest.TestCase):
    """Runtime discovery must fail closed before loading a workflow."""

    def setUp(self) -> None:
        self.controller = load_module("flowkit_controller_runtime", CONTROLLER_DIR / "controller.py")

    def test_locateRuntime_prefersMiseSelectedExecutable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            selected = Path(temporary) / "mise-specify"
            other = Path(temporary) / "path-specify"
            selected.write_text("#!/bin/sh\n", encoding="utf-8")
            other.write_text("#!/bin/sh\n", encoding="utf-8")
            selected.chmod(0o755)
            other.chmod(0o755)
            self.assertEqual(selected, self.controller.select_specify_executable(selected, [selected, other]))

    def test_locateRuntime_acceptsOneOrdinaryExecutable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            selected = Path(temporary) / "specify"
            selected.write_text("#!/bin/sh\n", encoding="utf-8")
            selected.chmod(0o755)
            self.assertEqual(selected, self.controller.select_specify_executable(None, [selected]))

    def test_locateRuntime_rejectsMissingOrAmbiguousExecutables(self) -> None:
        with self.assertRaisesRegex(ValueError, "not found"):
            self.controller.select_specify_executable(None, [])
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first"
            second = Path(temporary) / "second"
            first.write_text("#!/bin/sh\n", encoding="utf-8")
            second.write_text("#!/bin/sh\n", encoding="utf-8")
            first.chmod(0o755)
            second.chmod(0o755)
            with self.assertRaisesRegex(ValueError, "ambiguous"):
                self.controller.select_specify_executable(None, [first, second])

    def test_locateRuntime_rejectsVersionMismatch(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected Specify"):
            self.controller.check_specify_version("specify 1.0.9", "1.0.10.dev0+pegagio.2")


class InstalledDefinitionTests(unittest.TestCase):
    """The controller reads the composed definition without native execution."""

    def setUp(self) -> None:
        self.controller = load_module("flowkit_controller_definition", CONTROLLER_DIR / "controller.py")

    def test_loadDefinition_usesSelectedProjectAndReturnsProvenance(self) -> None:
        selected = Path("/consumer/project")
        definition = {"workflow": {"id": "speckit-flow-tasks", "version": "0.2.0"}, "steps": []}
        with patch.object(self.controller, "WorkflowEngine") as engine_class:
            engine_class.return_value.load_workflow.return_value = type(
                "Definition", (), {"data": definition, "source_path": Path("/consumer/project/.specify/workflows/tasks/workflow.yml"), "version": "0.2.0"}
            )()
            result = self.controller.load_installed_definition(selected, "speckit-flow-tasks")
        engine_class.assert_called_once_with(selected)
        engine_class.return_value.load_workflow.assert_called_once_with("speckit-flow-tasks")
        self.assertEqual("0.2.0", result["version"])
        self.assertEqual("speckit-flow-tasks", result["workflow"]["id"])
        self.assertTrue(result["source_path"].endswith("workflow.yml"))

    def test_loadDefinition_neverExecutesNativeWorkflow(self) -> None:
        with patch.object(self.controller, "WorkflowEngine") as engine_class:
            engine = engine_class.return_value
            engine.load_workflow.return_value = type(
                "Definition", (), {"data": {"workflow": {"id": "test", "version": "1"}, "steps": []}, "source_path": Path("workflow.yml"), "version": "1"}
            )()
            self.controller.load_installed_definition(Path("/consumer"), "test")
            engine.execute.assert_not_called()

    def test_fingerprint_recordsContentAndFileIdentity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.json"
            path.write_text("{}", encoding="utf-8")
            result = self.controller.file_fingerprint(path)
        self.assertEqual({"sha256", "device", "inode"}, set(result))

    def test_verifyInstall_requiresInstalledBindingAndUnchangedHelper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            paths = [
                ".agents/skills/flow-kit-tasks/SKILL.md",
                ".agents/skills/flow-kit-tasks/agents/openai.yaml",
                ".specify/flow-kit/manifest.yml",
                ".specify/flow-kit/controller-protocol.md",
                ".specify/flow-kit/scripts/bootstrap.sh",
                ".specify/flow-kit/scripts/python/controller.py",
                ".specify/flow-kit/scripts/python/recovery.py",
            ]
            files = {}
            for relative in paths:
                target = project / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                content = f"name: flow-kit-tasks\n" if relative.endswith("SKILL.md") else "fixture\n"
                if relative.endswith("manifest.yml"):
                    content = 'package:\n  version: "0.1.0"\n'
                target.write_text(content, encoding="utf-8")
                files[relative] = __import__("hashlib").sha256(content.encode()).hexdigest()
            record = {
                "package": "flow-kit-controllers", "version": "0.1.0", "status": "installed", "files": files,
                "controllers": [{"skill_id": "flow-kit-tasks", "workflow_id": "speckit-flow-tasks"}],
            }
            record_path = project / ".specify/flow-kit/skills-install.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            self.controller.verify_controller_install(project, "flow-kit-tasks", "speckit-flow-tasks")
            (project / paths[0]).write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "was changed"):
                self.controller.verify_controller_install(project, "flow-kit-tasks", "speckit-flow-tasks")


class GraphPreflightTests(unittest.TestCase):
    """Graph validation covers nested branches before any execution starts."""

    def setUp(self) -> None:
        self.controller = load_module("flowkit_controller_graph", CONTROLLER_DIR / "controller.py")
        self.workflow = {
            "inputs": {"feature_context": {"required": True}},
            "steps": [
                {"id": "modeled-prompt", "type": "prompt", "model": "gpt-6-sol"},
                {"id": "review-verdict", "type": "gate"},
                {"id": "route-result", "type": "switch", "cases": {"primary": [
                    {"id": "nested-modeled-command", "command": "speckit.fixture", "model": "gpt-6-luna", "reasoning_effort": "high"}
                ]}, "default": [
                    {"id": "unavailable-model-branch", "type": "prompt", "model": "flowkit-test-unavailable-model"}
                ]},
            ],
        }

    def test_collectModels_includesUntakenNestedBranchesAndMediumDefault(self) -> None:
        models = self.controller.collect_model_assignments(self.workflow["steps"], {})
        self.assertEqual(
            [("modeled-prompt", "gpt-6-sol", "medium"), ("nested-modeled-command", "gpt-6-luna", "high"), ("unavailable-model-branch", "flowkit-test-unavailable-model", "medium")],
            [(item["step_id"], item["model"], item["reasoning_effort"]) for item in models],
        )

    def test_requiredInputs_failBeforeWorkflowExecution(self) -> None:
        with self.assertRaisesRegex(ValueError, "feature_context"):
            self.controller.validate_required_inputs(self.workflow, {})

    def test_requiredInputs_rejectBlankValues(self) -> None:
        for value in ("", "  "):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "feature_context"):
                self.controller.validate_required_inputs(self.workflow, {"feature_context": value})

    def test_validateDefinition_rejectsUnsupportedTemplateInLaterBranch(self) -> None:
        definition = {
            "workflow": {"id": "probe", "version": "1.0"},
            "inputs": {"feature_context": {"required": True, "type": "string"}},
            "steps": [
                {"id": "first", "type": "prompt", "prompt": "Start {{ inputs.feature_context }}", "model": "gpt-6-sol"},
                {"id": "route", "type": "switch", "expression": "{{ steps.first.output.choice }}", "cases": {
                    "later": [{"id": "bad", "type": "prompt", "prompt": "{{ unsupported.value }}"}],
                }},
            ],
        }
        with self.assertRaisesRegex(ValueError, "unsupported template"):
            self.controller.validate_workflow_definition(definition)

    def test_validateGraph_rejectsDuplicateStepIDs(self) -> None:
        graph = [{"id": "same", "type": "prompt"}, {"id": "route", "type": "switch", "cases": {"a": [{"id": "same", "type": "prompt"}]}}]
        with self.assertRaisesRegex(ValueError, "duplicate step id"):
            self.controller.validate_workflow_graph(graph)

    def test_collectModels_appliesOverrideToExactlyOneNamedStep(self) -> None:
        models = self.controller.collect_model_assignments(
            self.workflow["steps"],
            {"step_id": "nested-modeled-command", "model": "gpt-6-sol", "reasoning_effort": "medium"},
        )
        nested = next(item for item in models if item["step_id"] == "nested-modeled-command")
        self.assertEqual(("gpt-6-sol", "medium"), (nested["model"], nested["reasoning_effort"]))
        self.assertEqual("gpt-6-sol", models[0]["model"])

    def test_collectModels_rejectsUnknownOrUnmodeledOverride(self) -> None:
        with self.assertRaisesRegex(ValueError, "one modeled step"):
            self.controller.collect_model_assignments(self.workflow["steps"], {"step_id": "review-verdict", "model": "gpt-6-sol"})
        with self.assertRaisesRegex(ValueError, "one modeled step"):
            self.controller.collect_model_assignments(self.workflow["steps"], {"step_id": "missing", "model": "gpt-6-sol"})

    def test_collectModels_rejectsEmptyModelAndUnsupportedEffort(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonempty concrete ID"):
            self.controller.collect_model_assignments([{"id": "empty", "type": "prompt", "model": " "}])
        with self.assertRaisesRegex(ValueError, "unsupported reasoning effort"):
            self.controller.collect_model_assignments([{"id": "bad-effort", "type": "prompt", "model": "gpt-6-sol", "reasoning_effort": "sometimes"}])

    def test_validateGraph_rejectsModelAndEffortOnGateAndEffortWithoutModel(self) -> None:
        for node in (
            {"id": "gate-model", "type": "gate", "model": "gpt-6-sol"},
            {"id": "switch-effort", "type": "switch", "reasoning_effort": "high", "cases": {}},
            {"id": "effort-only", "type": "prompt", "reasoning_effort": "high"},
        ):
            with self.subTest(node=node), self.assertRaises(ValueError):
                self.controller.validate_workflow_graph([node])

    def test_resolveSkill_usesPinnedCommandNamingAndChecksDeclaredName(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / ".agents/skills/speckit-flow-wiki-ingest"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: speckit-flow-wiki-ingest\n---\n", encoding="utf-8")
            result = self.controller.resolve_installed_skill(Path(temporary), "speckit.flow-wiki.ingest")
        self.assertEqual("speckit-flow-wiki-ingest", result["name"])

    def test_resolveSkill_failsClosedWhenMissingOrMismatched(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "not found"):
                self.controller.resolve_installed_skill(Path(temporary), "speckit.tasks")
            skill_dir = Path(temporary) / ".agents/skills/speckit-tasks"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: unrelated\n---\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "different name"):
                self.controller.resolve_installed_skill(Path(temporary), "speckit.tasks")

    def test_validateDefinition_rejectsWorkflowLevelModelDefaults(self) -> None:
        definition = {"workflow": {"id": "test", "model": "gpt-6-sol"}, "steps": []}
        with self.assertRaisesRegex(ValueError, "workflow-level"):
            self.controller.validate_workflow_definition(definition)

    def test_renderTemplate_resolvesInputsAndPriorOutputsAndRejectsUnknownForms(self) -> None:
        value = "Implement {{ inputs.feature }} after {{ steps.plan.output.summary }}"
        rendered = self.controller.render_template(value, {"feature": "013"}, {"plan": {"summary": "review"}})
        self.assertEqual("Implement 013 after review", rendered)
        with self.assertRaisesRegex(ValueError, "unresolved input"):
            self.controller.render_template("{{ inputs.absent }}", {}, {})
        with self.assertRaisesRegex(ValueError, "unsupported or unresolved"):
            self.controller.render_template("{{ unsupported.value }}", {}, {})


class HumanInteractionTests(unittest.TestCase):
    """Interactive answers stay explicit and bound to the original child."""

    def setUp(self) -> None:
        self.controller = load_module("flowkit_controller_interaction", CONTROLLER_DIR / "controller.py")
        self.question = {
            "kind": "question", "step_id": "clarify-specification",
            "question": "Which workflows should the dashboard show?",
            "options": ["A", "B"], "allow_custom": True,
        }

    def test_validateChildQuestion_normalizesCustomFlagAndRejectsInvalidRequests(self) -> None:
        validated = self.controller.validate_child_question(self.question, "clarify-specification")
        self.assertTrue(validated["allow_custom_answer"])
        with self.assertRaisesRegex(ValueError, "step_id"):
            self.controller.validate_child_question(self.question, "different-step")
        with self.assertRaisesRegex(ValueError, "options"):
            self.controller.validate_child_question({**self.question, "options": ["A", "A"]}, "clarify-specification")

    def test_resolveChildAnswer_requiresSameChildAndExplicitAllowedAnswer(self) -> None:
        resolved = self.controller.resolve_child_answer(self.question, "A", "child-1", "child-1")
        self.assertEqual({"step_id": "clarify-specification", "child_id": "child-1", "answer": "A"}, resolved)
        with self.assertRaisesRegex(ValueError, "same child"):
            self.controller.resolve_child_answer(self.question, "A", "child-1", "child-2")
        with self.assertRaisesRegex(ValueError, "explicit"):
            self.controller.resolve_child_answer(self.question, "", "child-1", "child-1")
        with self.assertRaisesRegex(ValueError, "allowed"):
            self.controller.resolve_child_answer({**self.question, "allow_custom": False}, "another answer", "child-1", "child-1")

    def test_childQuestion_acceptsDescribedChoicesAndResolvesTheirIds(self) -> None:
        request = {**self.question, "options": [
            {"id": "A", "description": "Select an active workflow."},
            {"id": "B", "description": "Display the designated current workflow."},
        ], "allow_custom": False}
        normalized = self.controller.validate_child_question(request, "clarify-specification")
        self.assertEqual(request["options"], normalized["options"])
        self.assertEqual("B", self.controller.resolve_child_answer(normalized, "2", "child-1", "child-1")["answer"])
        self.assertEqual("A", self.controller.resolve_child_answer(normalized, "a", "child-1", "child-1")["answer"])
        with self.assertRaisesRegex(ValueError, "distinct"):
            self.controller.validate_child_question({**request, "options": [request["options"][0]] * 2}, "clarify-specification")
        with self.assertRaisesRegex(ValueError, "options"):
            self.controller.validate_child_question({**request, "options": [{"id": "A", "description": ""}]}, "clarify-specification")

    def test_validateGateChoice_requiresHumanVerdictAndOnlySelectedBranch(self) -> None:
        gate = {"id": "review", "type": "gate", "options": ["analyze", "defer"]}
        self.assertEqual("analyze", self.controller.validate_gate_choice(gate, "1"))
        with self.assertRaisesRegex(ValueError, "explicit"):
            self.controller.validate_gate_choice(gate, "")
        with self.assertRaisesRegex(ValueError, "allowed"):
            self.controller.validate_gate_choice(gate, "implement")
        switch = {"id": "route", "type": "switch", "cases": {
            "analyze": [{"id": "stop", "type": "prompt", "prompt": "Start analysis separately."}],
            "defer": [{"id": "deferred", "type": "prompt", "prompt": "Stop."}],
        }}
        self.assertEqual(["stop"], [step["id"] for step in self.controller.select_switch_branch(switch, "analyze")])

    def test_interactionCli_validatesQuestionAnswerAndGateWithoutPersistingThem(self) -> None:
        output = io.StringIO()
        with patch.object(sys, "stdin", io.StringIO(json.dumps(self.question))), redirect_stdout(output):
            self.assertEqual(0, self.controller.main(["question", "--step-id", "clarify-specification"]))
        normalized = json.loads(output.getvalue())
        self.assertTrue(normalized["allow_custom_answer"])
        output = io.StringIO()
        payload = {"request": normalized, "answer": "1"}
        with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), redirect_stdout(output):
            self.assertEqual(0, self.controller.main(["answer", "--child-id", "child-1", "--target-child-id", "child-1"]))
        self.assertEqual("A", json.loads(output.getvalue())["answer"])
        output = io.StringIO()
        gate_payload = {"gate": {"id": "review", "type": "gate", "options": ["analyze", "defer"]}, "answer": "2"}
        with patch.object(sys, "stdin", io.StringIO(json.dumps(gate_payload))), redirect_stdout(output):
            self.assertEqual(0, self.controller.main(["gate"]))
        self.assertEqual({"choice": "defer"}, json.loads(output.getvalue()))

    def test_clarifyGateBranches_stopWithoutLaunchingPlanning(self) -> None:
        workflow = yaml.safe_load((ROOT / "workflows/speckit-flow-clarify/workflow.yml").read_text(encoding="utf-8"))
        gate = next(step for step in workflow["steps"] if step["id"] == "choose-clarification-result")
        switch = next(step for step in workflow["steps"] if step["id"] == "route-clarification-result")
        for option in gate["options"]:
            with self.subTest(option=option):
                choice = self.controller.validate_gate_choice(gate, option)
                branch = self.controller.select_switch_branch(switch, choice)
                self.assertEqual(1, len(branch))
                self.assertEqual("prompt", branch[0]["type"])


class RecoveryTests(unittest.TestCase):
    """Stopped runs keep compact, portable evidence without reverting edits."""

    def setUp(self) -> None:
        self.recovery = load_module("flowkit_controller_recovery", CONTROLLER_DIR / "recovery.py")

    def test_createAndUpdateSummary_recordsBoundedStepEvidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            summary = self.recovery.create_summary(
                project,
                {"workflow": {"id": "speckit-flow-tasks", "version": "0.2.0"}, "sha256": "a" * 64},
                {"bundle_record": {"sha256": "b" * 64, "device": 1, "inode": 2}, "skill_record": {"sha256": "c" * 64, "device": 1, "inode": 3}},
                [{"step_id": "generate-tasks", "model": "gpt-6-luna", "reasoning_effort": "high"}],
                preflight_passed=True,
            )
            path = project / ".specify/flow-controllers/runs" / summary["run_id"] / "summary.json"
            for status in ("pending", "waiting_for_human", "running", "completed"):
                self.recovery.update_step(path, f"status-{status}", status)
            self.recovery.update_step(path, "generate-tasks", "running")
            partial_edit = project / "created.md"
            partial_edit.write_text("preserve", encoding="utf-8")
            self.recovery.update_step(path, "generate-tasks", "completed", changed_files=["created.md"])
            saved = json.loads(path.read_text(encoding="utf-8"))
            preserved = partial_edit.read_text(encoding="utf-8")
        self.assertEqual("completed", saved["steps"]["generate-tasks"]["status"])
        self.assertEqual({"pending", "waiting_for_human", "running", "completed"}, {saved["steps"][f"status-{status}"]["status"] for status in ("pending", "waiting_for_human", "running", "completed")})
        self.assertEqual(["created.md"], saved["changed_files"])
        self.assertEqual("preserve", preserved)

    def test_createSummary_rejectsPreflightFailureAndSensitiveEvidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "successful preflight"):
                self.recovery.create_summary(Path(temporary), {}, {}, [], preflight_passed=False)
            with self.assertRaisesRegex(ValueError, "repository-relative"):
                self.recovery.validate_summary({"changed_files": ["/private/file"]})
            with self.assertRaisesRegex(ValueError, "escape the repository"):
                self.recovery.validate_summary({"changed_files": ["../outside"]})
            with self.assertRaisesRegex(ValueError, "transcript"):
                self.recovery.validate_summary({"child_transcript": "raw conversation"})

    def test_interruptionMarksRunningStepIncomplete_andRefreshStopsOnEitherRecord(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            summary = self.recovery.create_summary(project, {"workflow": {"id": "x", "version": "1"}, "sha256": "d" * 64}, {}, [], preflight_passed=True)
            path = project / ".specify/flow-controllers/runs" / summary["run_id"] / "summary.json"
            self.recovery.update_step(path, "step-one", "running")
            recovered = self.recovery.mark_interrupted_steps_incomplete(path)
        self.assertEqual("incomplete", recovered["steps"]["step-one"]["status"])
        initial = {"workflow_sha256": "a", "bundle_record": {"sha256": "b"}, "skill_record": {"sha256": "c"}}
        changed = {**initial, "skill_record": {"sha256": "new"}}
        self.assertTrue(self.recovery.installation_changed(initial, changed))

    def test_stopRun_marksWaitingStepIncomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            summary = self.recovery.create_summary(project, {"workflow": {"id": "x", "version": "1"}, "sha256": "d" * 64}, {}, [], preflight_passed=True)
            path = project / ".specify/flow-controllers/runs" / summary["run_id"] / "summary.json"
            self.recovery.update_step(path, "review", "waiting_for_human")
            stopped = self.recovery.stop_run(path, "operator-deferred")
        self.assertEqual("stopped", stopped["status"])
        self.assertEqual("incomplete", stopped["steps"]["review"]["status"])
        self.assertEqual("operator-deferred", stopped["blocker"])

    def test_recoveryRejectsUnboundedBlockerText(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            summary = self.recovery.create_summary(project, {"workflow": {"id": "x", "version": "1"}, "sha256": "d" * 64}, {}, [], preflight_passed=True)
            path = project / ".specify/flow-controllers/runs" / summary["run_id"] / "summary.json"
            for blocker in ("Child transcript: private answer", "secret private-key-material"):
                with self.subTest(blocker=blocker), self.assertRaisesRegex(ValueError, "blocker"):
                    self.recovery.stop_run(path, blocker)
            self.assertIsNone(self.recovery.read_summary(path)["blocker"])

    def test_recoveryRead_sanitizesLegacyTextBlocker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            summary = self.recovery.create_summary(project, {"workflow": {"id": "x", "version": "1"}, "sha256": "d" * 64}, {}, [], preflight_passed=True)
            path = project / ".specify/flow-controllers/runs" / summary["run_id"] / "summary.json"
            legacy = json.loads(path.read_text(encoding="utf-8"))
            legacy["blocker"] = "Legacy free-text stop reason"
            path.write_text(json.dumps(legacy), encoding="utf-8")
            self.assertEqual("unspecified-stop", self.recovery.read_summary(path)["blocker"])
            self.assertEqual("Legacy free-text stop reason", json.loads(path.read_text(encoding="utf-8"))["blocker"])

    def test_recoveryCli_createsSummaryFromSuccessfulPreflightInput(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            payload = {
                "workflow": {"workflow": {"id": "speckit-flow-tasks", "version": "0.2.0"}, "sha256": "a" * 64},
                "fingerprints": {}, "assignments": [], "preflight_passed": True,
            }
            output = io.StringIO()
            with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), redirect_stdout(output):
                self.assertEqual(0, self.recovery.main(["create", "--project", temporary]))
            result = json.loads(output.getvalue())
            summary_path = Path(result["summary_path"])
            self.assertTrue(summary_path.is_file())
            self.assertEqual("running", json.loads(summary_path.read_text(encoding="utf-8"))["status"])


if __name__ == "__main__":
    unittest.main()

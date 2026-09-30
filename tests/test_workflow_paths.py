"""Workflow continuation, gate, and artifact-order checks across F014 stories."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from zipfile import ZipFile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).parents[1]
WORKFLOWS = ROOT / "workflows"
CONTROLLER_PATH = ROOT / "controllers/flow-kit/scripts/python/controller.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_workflow(workflow_id: str) -> dict[str, Any]:
    return yaml.safe_load((WORKFLOWS / workflow_id / "workflow.yml").read_text(encoding="utf-8"))


def find_step(nodes: list[dict[str, Any]], step_id: str) -> dict[str, Any] | None:
    for node in nodes:
        if node.get("id") == step_id:
            return node
        for branch in node.get("cases", {}).values() if isinstance(node.get("cases"), dict) else []:
            found = find_step(branch, step_id)
            if found is not None:
                return found
        found = find_step(node.get("default", []), step_id)
        if found is not None:
            return found
        found = find_step(node.get("steps", []), step_id)
        if found is not None:
            return found
    return None


def commands(nodes: list[dict[str, Any]]) -> list[str]:
    result = []
    for node in nodes:
        if "command" in node:
            result.append(node["command"])
        elif node.get("type") == "switch":
            for branch in node.get("cases", {}).values():
                result.extend(commands(branch))
            result.extend(commands(node.get("default", [])))
        elif node.get("type") == "do-while":
            result.extend(commands(node.get("steps", [])))
    return result


def walk(nodes: list[dict[str, Any]]) -> list[tuple[dict[str, Any], str | None, str | None]]:
    result = []
    for node in nodes:
        result.append((node, None, None))
        for branch_id, branch in node.get("cases", {}).items() if isinstance(node.get("cases"), dict) else []:
            result.extend(walk(branch))
        result.extend(walk(node.get("default", [])))
        result.extend(walk(node.get("steps", [])))
    return result


class WorkflowPathTests(unittest.TestCase):
    """Corrective routes preserve ordering, re-assessment, and human authority."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.controller = load_module("flowkit_workflow_path_controller", CONTROLLER_PATH)

    def test_analyzeStartsWithEvidenceAssessmentAndReassessesEveryBoundedPass(self) -> None:
        workflow = load_workflow("speckit-flow-analyze-remediate")
        steps = workflow["steps"]
        self.assertEqual("assess-analysis", steps[0]["id"])
        self.assertEqual("Verifier", steps[0]["flow_kit"]["agent"])
        loop = find_step(steps, "analysis-correction-loop")
        self.assertIsNotNone(loop)
        self.assertEqual(5, loop["max_iterations"])
        self.assertTrue(loop["condition"].startswith("{{ steps.reassess-analysis.output.state =="))
        self.assertEqual("reassess-analysis-before-pass", loop["steps"][0]["id"])
        self.assertEqual("reassess-analysis", loop["steps"][-1]["id"])
        route = find_step(steps, "select-analysis-flowback")
        self.assertEqual(["remediate-specification", "remediate-plan", "remediate-tasks"], list(route["cases"]))
        expected = {
            "remediate-specification": ["speckit.specify", "speckit.plan", "speckit.tasks", "speckit.analyze"],
            "remediate-plan": ["speckit.plan", "speckit.tasks", "speckit.analyze"],
            "remediate-tasks": ["speckit.tasks", "speckit.analyze"],
        }
        for route_name, expected_commands in expected.items():
            self.assertEqual(expected_commands, commands(route["cases"][route_name]))
        self.assertTrue(find_step(steps, "analysis-consequential-gate"))
        self.assertTrue(find_step(steps, "analysis-final-blocked-stop"))
        self.assertFalse(any(command.startswith("speckit.flow-kit-") for command in commands(steps)))

    def test_implementReconcilesDependenciesAnalyzesBeforeEligibleWork(self) -> None:
        workflow = load_workflow("speckit-flow-implement")
        steps = workflow["steps"]
        self.assertEqual("assess-implementation", steps[0]["id"])
        loop = find_step(steps, "implementation-correction-loop")
        self.assertIsNotNone(loop)
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual("reassess-implementation-before-pass", loop["steps"][0]["id"])
        self.assertEqual("reassess-implementation", loop["steps"][-1]["id"])
        route = find_step(steps, "select-implementation-flowback")
        expected = {
            "remediate-implementation-specification": ["speckit.specify", "speckit.plan", "speckit.tasks", "speckit.analyze", "speckit.implement"],
            "remediate-implementation-plan": ["speckit.plan", "speckit.tasks", "speckit.analyze", "speckit.implement"],
            "remediate-implementation-tasks": ["speckit.tasks", "speckit.analyze", "speckit.implement"],
            "analyze-before-implementation-resumes": ["speckit.analyze", "speckit.implement"],
            "continue-eligible-implementation": ["speckit.implement"],
        }
        for route_name, expected_commands in expected.items():
            self.assertEqual(expected_commands, commands(route["cases"][route_name]))
        self.assertTrue(find_step(steps, "implementation-consequential-gate"))
        self.assertTrue(find_step(steps, "implementation-final-blocked-stop"))
        self.assertFalse(any(command.startswith("speckit.flow-kit-") for command in commands(steps)))

    def testLoopRoutingStopsForNoProgressAndCapButAcceptsCleanBeforeCorrectivePass(self) -> None:
        complete = {"state": "complete"}
        self.assertEqual({"action": "complete"}, self.controller.route_loop_assessment(
            complete, iteration=0, max_iterations=5, loop_body_step_ids={"correct"}
        ))
        initial = {"state": "continue", "next_step_id": "correct", "remaining_ids": ["T001"]}
        self.assertEqual({"action": "continue", "next_step_id": "correct"}, self.controller.route_loop_assessment(
            initial, iteration=0, max_iterations=5, loop_body_step_ids={"correct"}
        ))
        no_progress = {**initial, "evidence": [{"path": "tasks.md", "sha256": "f" * 64}]}
        self.assertEqual({"action": "blocked", "blocker": "no-progress"}, self.controller.route_loop_assessment(
            no_progress, iteration=1, max_iterations=5, loop_body_step_ids={"correct"}, previous_assessment=initial
        ))
        progress = {"state": "continue", "next_step_id": "correct", "remaining_ids": ["T002"], "resolved_ids": ["T001"]}
        self.assertEqual({"action": "continue", "next_step_id": "correct"}, self.controller.route_loop_assessment(
            progress, iteration=1, max_iterations=5, loop_body_step_ids={"correct"}, previous_assessment=initial
        ))
        self.assertEqual({"action": "blocked", "blocker": "loop-cap-exhausted"}, self.controller.route_loop_assessment(
            progress, iteration=5, max_iterations=5, loop_body_step_ids={"correct"}, previous_assessment=initial
        ))

    def testConsequentialGateIsMainTaskOnlyAndNoNestedWorkflowIsDeclared(self) -> None:
        for workflow_id, gate_id, expected_options in (
            ("speckit-flow-analyze-remediate", "analysis-consequential-gate", ["defer", "escalate", "abort"]),
            ("speckit-flow-implement", "implementation-consequential-gate", ["defer", "escalate", "abort"]),
        ):
            workflow = load_workflow(workflow_id)
            gate = find_step(workflow["steps"], gate_id)
            self.assertEqual(expected_options, gate["options"])
            self.assertNotIn("flow_kit", gate)
            self.assertTrue(all(not command.startswith("speckit.flow-kit-") for command in commands(workflow["steps"])))

    def testManualAnalyzeAndImplementPathsMatchBoundedContinuationContract(self) -> None:
        readme = (ROOT / "workflows/README.md").read_text(encoding="utf-8")
        analyze = readme.split("## Manual analysis and remediation path", 1)[1].split("## Manual implementation path", 1)[0]
        implement = readme.split("## Manual implementation path", 1)[1].split("## Manual convergence path", 1)[0]
        for section, classification_text in (
            (analyze, "do not ask the operator to classify a routine result"),
            (implement, "without asking the operator to classify routine results"),
        ):
            self.assertIn(classification_text, section)
            self.assertIn("repeated findings", section)
            self.assertIn("no measurable progress", section)
            self.assertIn("five-pass safety cap", section)
            self.assertIn("smallest safe resumption action", section)
        self.assertIn("Converge as a separate operator invocation", implement)

    def testStartFeatureLinkageCasesRequireExactApprovalAndRefreshBriefEvidence(self) -> None:
        workflow = load_workflow("speckit-flow-start-feature")
        steps = workflow["steps"]
        initial_route = find_step(steps, "route-roadmap-decision")
        self.assertEqual("apply-approved-roadmap-patch", initial_route["cases"]["approve"][0]["id"])
        for decision in ("amend-roadmap", "resolve-context", "defer"):
            self.assertEqual([], commands(initial_route["cases"][decision]))

        linkage_route = find_step(steps, "route-created-spec-linkage")
        self.assertIsNotNone(linkage_route)
        self.assertEqual({"linked", "repairable", "conflict", "ambiguous"}, set(linkage_route["cases"]))
        self.assertEqual("brief-against-roadmap", linkage_route["cases"]["linked"][0]["id"])
        self.assertEqual("review-spec-dir-patch", linkage_route["cases"]["repairable"][0]["id"])
        self.assertEqual("stop-on-linkage-conflict", linkage_route["cases"]["conflict"][0]["id"])
        self.assertEqual("stop-on-ambiguous-linkage", linkage_route["cases"]["ambiguous"][0]["id"])
        self.assertEqual([], commands(linkage_route["cases"]["conflict"]))
        self.assertEqual([], commands(linkage_route["cases"]["ambiguous"]))

        gate = find_step(steps, "review-spec-dir-patch")
        self.assertEqual(["approve-exact-patch", "amend", "defer"], gate["options"])
        patch_route = find_step(steps, "route-spec-dir-patch-decision")
        self.assertEqual("apply-approved-spec-dir-patch", patch_route["cases"]["approve-exact-patch"][0]["id"])
        self.assertEqual("stop-for-linkage-amendment", patch_route["cases"]["amend"][0]["id"])
        self.assertEqual("stop-with-deferred-linkage", patch_route["cases"]["defer"][0]["id"])
        self.assertEqual([], commands(patch_route["cases"]["amend"]))
        self.assertEqual([], commands(patch_route["cases"]["defer"]))
        approved_steps = patch_route["cases"]["approve-exact-patch"]
        self.assertEqual([
            "apply-approved-spec-dir-patch",
            "verify-repaired-spec-linkage",
            "route-rechecked-spec-linkage",
        ], [step["id"] for step in approved_steps])
        self.assertIn("proposed_patch", gate["message"])
        self.assertIn("proposed_patch", approved_steps[0]["input"]["args"])
        self.assertIn("Do not infer", approved_steps[0]["input"]["args"])
        verified = find_step(steps, "route-rechecked-spec-linkage")
        self.assertEqual("brief-after-linkage-repair", verified["cases"]["linked"][0]["id"])
        self.assertEqual("stop-after-linkage-recheck-repairable", verified["cases"]["repairable"][0]["id"])
        self.assertEqual("stop-after-linkage-recheck-conflict", verified["cases"]["conflict"][0]["id"])
        assessor_prompt = find_step(steps, "assess-created-spec-linkage")["prompt"]
        self.assertIn("structured result", assessor_prompt)
        self.assertIn("no trailing punctuation inside the backticks", assessor_prompt)
        self.assertIn("SPEC_TARGET={{ steps.assess-created-spec-linkage.output.actual_spec_dir }}",
                      linkage_route["cases"]["linked"][0]["input"]["args"])
        self.assertIn("ROADMAP_ENTRY={{ steps.assess-created-spec-linkage.output.selected_entry_id }}",
                      linkage_route["cases"]["linked"][0]["input"]["args"])

        fixture = json.loads((ROOT / "tests/consumer-fixtures/start-feature-linkage.json").read_text(encoding="utf-8"))
        self.assertEqual({
            "unique-existing-mapping", "missing-spec-dir", "stale-spec-dir",
            "conflicting-spec-dir-ownership", "ambiguous-roadmap-target",
            "patch-amended-before-approval", "patch-deferred-before-approval",
            "mapping-still-invalid-after-approved-patch",
        }, {scenario["id"] for scenario in fixture["scenarios"]})
        expected_terminal = {
            "unique-existing-mapping": "brief-against-roadmap",
            "missing-spec-dir": "brief-after-linkage-repair",
            "stale-spec-dir": "brief-after-linkage-repair",
            "conflicting-spec-dir-ownership": "stop-on-linkage-conflict",
            "ambiguous-roadmap-target": "stop-on-ambiguous-linkage",
            "patch-amended-before-approval": "stop-for-linkage-amendment",
            "patch-deferred-before-approval": "stop-with-deferred-linkage",
            "mapping-still-invalid-after-approved-patch": "stop-after-linkage-recheck-conflict",
        }
        expected_state = {
            "unique-existing-mapping": "linked",
            "missing-spec-dir": "repairable",
            "stale-spec-dir": "repairable",
            "conflicting-spec-dir-ownership": "conflict",
            "ambiguous-roadmap-target": "ambiguous",
            "patch-amended-before-approval": "repairable",
            "patch-deferred-before-approval": "repairable",
            "mapping-still-invalid-after-approved-patch": "repairable",
        }
        for scenario in fixture["scenarios"]:
            with self.subTest(scenario=scenario["id"]):
                self.assertEqual(expected_terminal[scenario["id"]], scenario["expected_terminal"])
                self.assertEqual(expected_state[scenario["id"]], scenario["observed_state"])
                if scenario["gate_choice"] != "approve-exact-patch":
                    self.assertFalse(scenario["roadmap_write_allowed"])
                if scenario["observed_state"] == "linked":
                    self.assertEqual("brief-against-roadmap", scenario["expected_terminal"])
                elif scenario["observed_state"] == "repairable" and scenario["gate_choice"] in {"amend", "defer"}:
                    self.assertFalse(scenario["roadmap_write_allowed"])

    def testRoadmapBriefResolverRequiresTheExplicitExactPairInDisposableFixtures(self) -> None:
        archive = ROOT / "catalog/packages/flow-roadmap-0.2.1.zip"
        with tempfile.TemporaryDirectory(prefix="flowkit-roadmap-linkage-") as temporary:
            fixture_root = Path(temporary).resolve()
            with ZipFile(archive) as bundle:
                for source in (
                    "flow-roadmap/scripts/python/load_config.py",
                    "flow-roadmap/scripts/python/review_contract.py",
                ):
                    destination = fixture_root / source
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(bundle.read(source))
            contract_path = fixture_root / "flow-roadmap/scripts/python/review_contract.py"
            contract = load_module("flowkit_linkage_review_contract", contract_path)

            target = "specs/014-flowkit-workflow-improvements/"
            selected_id = "014"
            feature_dir = fixture_root / target
            feature_dir.mkdir(parents=True)
            (feature_dir / "spec.md").write_text("# Fixture spec\n", encoding="utf-8")
            roadmap_path = fixture_root / ".specify/memory/roadmap.md"
            roadmap_path.parent.mkdir(parents=True)

            def resolve(mapping: str | None) -> dict[str, Any]:
                field = f"- **Spec dir**: `{mapping}`\n" if mapping is not None else ""
                roadmap_path.write_text(
                    "### 014 — Fixture Feature [status: in-progress]\n" + field,
                    encoding="utf-8",
                )
                arguments = argparse.Namespace(
                    roadmap_path=".specify/memory/roadmap.md",
                    spec_target=target,
                    roadmap_entry=selected_id,
                    ambient_feature=None,
                    selected_entry=None,
                )
                return contract.resolve_target(fixture_root, arguments)

            unique = resolve("specs/014-flowkit-workflow-improvements/")
            self.assertEqual("selected", unique["state"])
            self.assertEqual(selected_id, unique["entry"]["id"])
            self.assertEqual("exact-spec-dir", unique["match_method"])
            for mapping in (None, "specs/old-location/"):
                with self.subTest(mapping=mapping):
                    self.assertEqual("conflict", resolve(mapping)["state"])
                    # The fixture remains unmodified until the workflow's exact-patch gate approves.
                    approved_patch = "specs/014-flowkit-workflow-improvements/"
                    repaired = resolve(approved_patch)
                    self.assertEqual("selected", repaired["state"])
                    self.assertEqual(selected_id, repaired["entry"]["id"])

    def testClarifyRepeatsBoundedSessionsOnlyWhileFreshAmbiguityEvidenceProgresses(self) -> None:
        workflow = load_workflow("speckit-flow-clarify")
        steps = workflow["steps"]
        self.assertEqual("clarification-session-loop", steps[0]["id"])
        loop = find_step(steps, "clarification-session-loop")
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual(["clarify-session", "assess-clarification-after-session"],
                         [step["id"] for step in loop["steps"]])
        command = find_step(steps, "clarify-session")
        self.assertEqual("speckit.clarify", command["command"])
        self.assertIn("five-question cap per session", command["input"]["args"])
        self.assertIn("operator", command["input"]["args"])
        self.assertEqual(["speckit.clarify"], commands(loop["steps"]))
        self.assertEqual("clarification-outcome-stop", steps[-1]["id"])
        self.assertFalse(any(step.get("type") in {"switch", "gate"} for step in steps))
        self.assertFalse(any("speckit-flow-plan" in command for command in commands(steps)))

        initial = {"state": "continue", "next_step_id": "clarify-session", "remaining_ids": ["Q1", "Q2"]}
        progress = {"state": "continue", "next_step_id": "clarify-session", "remaining_ids": ["Q2"], "resolved_ids": ["Q1"]}
        self.assertEqual({"action": "continue", "next_step_id": "clarify-session"}, self.controller.route_loop_assessment(
            progress, iteration=1, max_iterations=5, loop_body_step_ids={"clarify-session"}
        ))
        self.assertEqual({"action": "blocked", "blocker": "no-progress"}, self.controller.route_loop_assessment(
            {**initial, "resolved_ids": []}, iteration=1, max_iterations=5, loop_body_step_ids={"clarify-session"}
        ))
        self.assertEqual({"action": "continue", "next_step_id": "clarify-session"}, self.controller.route_loop_assessment(
            {"state": "continue", "next_step_id": "clarify-session", "remaining_ids": ["Q3"], "resolved_ids": ["Q2"]},
            iteration=2, max_iterations=5, loop_body_step_ids={"clarify-session"}, previous_assessment=progress
        ))
        self.assertEqual({"action": "blocked", "blocker": "no-progress"}, self.controller.route_loop_assessment(
            {**initial, "resolved_ids": []}, iteration=1, max_iterations=5,
            loop_body_step_ids={"clarify-session"}, previous_assessment=initial
        ))
        self.assertEqual({"action": "blocked", "blocker": "loop-cap-exhausted"}, self.controller.route_loop_assessment(
            progress, iteration=5, max_iterations=5, loop_body_step_ids={"clarify-session"}, previous_assessment=initial
        ))

    def testPlanProceedsWhenReadyAndStopsWithEvidenceForMissingOrMaterialProductInputs(self) -> None:
        workflow = load_workflow("speckit-flow-plan")
        steps = workflow["steps"]
        self.assertEqual("assess-plan-readiness", steps[0]["id"])
        initial_route = find_step(steps, "route-initial-plan-readiness")
        self.assertEqual({"complete", "continue", "needs-human", "blocked"}, set(initial_route["cases"]))
        self.assertEqual("plan-correction-loop", initial_route["cases"]["continue"][0]["id"])
        self.assertEqual("plan-prerequisite-stop", initial_route["cases"]["blocked"][0]["id"])
        self.assertEqual("plan-material-decision-gate", initial_route["cases"]["needs-human"][0]["id"])
        loop = find_step(steps, "plan-correction-loop")
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual("assess-plan-before-pass", loop["steps"][0]["id"])
        self.assertEqual("assess-plan-after-pass", loop["steps"][-1]["id"])
        before_route = find_step(steps, "route-plan-pass")
        self.assertEqual("select-plan-action", before_route["cases"]["continue"][0]["id"])
        self.assertEqual("create-plan", find_step(steps, "select-plan-action")["cases"]["create-plan"][0]["id"])
        self.assertEqual("speckit.plan", find_step(steps, "create-plan")["command"])
        self.assertEqual("Architect", find_step(steps, "create-plan")["flow_kit"]["agent"])
        self.assertEqual([], commands(initial_route["cases"]["blocked"]))
        self.assertEqual([], commands(initial_route["cases"]["needs-human"]))
        final_route = find_step(steps, "route-final-plan-readiness")
        self.assertEqual({"complete", "needs-human", "blocked", "continue", "default"}, set(final_route["cases"]))
        self.assertEqual("plan-loop-bounded-stop", final_route["cases"]["continue"][0]["id"])
        self.assertFalse(any(command.startswith("speckit.clarify") or command.startswith("speckit.flow-kit-")
                             for command in commands(steps)))
        self.assertFalse(any(step.get("type") == "gate" and "ready" in step.get("message", "").lower()
                             for step in steps))

    def testTasksGeneratesWithoutRoutineGateAndAssessesCoverageBeforeSuccess(self) -> None:
        workflow = load_workflow("speckit-flow-tasks")
        steps = workflow["steps"]
        self.assertEqual("assess-task-readiness", steps[0]["id"])
        self.assertIn("next_step_id to assess-task-coverage-before-pass", steps[0]["prompt"])
        initial_route = find_step(steps, "route-initial-task-readiness")
        self.assertEqual({"complete", "continue", "needs-human", "blocked"}, set(initial_route["cases"]))
        self.assertEqual("task-generation-loop", initial_route["cases"]["continue"][0]["id"])
        self.assertEqual("task-material-decision-gate", initial_route["cases"]["needs-human"][0]["id"])
        self.assertEqual("task-design-gap-stop", initial_route["cases"]["blocked"][0]["id"])
        loop = find_step(steps, "task-generation-loop")
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual("assess-task-coverage-before-pass", loop["steps"][0]["id"])
        self.assertEqual("assess-task-coverage-after-pass", loop["steps"][-1]["id"])
        self.assertIn("next_step_id to route-task-generation-pass", loop["steps"][0]["prompt"])
        self.assertIn("task-final-material-decision-gate", loop["steps"][0]["prompt"])
        route = find_step(steps, "route-task-generation-pass")
        self.assertEqual("select-task-action", route["cases"]["continue"][0]["id"])
        self.assertEqual("speckit.tasks", find_step(steps, "generate-tasks")["command"])
        final_route = find_step(steps, "route-final-task-coverage")
        self.assertEqual({"complete", "needs-human", "blocked", "continue", "default"}, set(final_route["cases"]))
        self.assertEqual("tasks-coverage-complete-stop", final_route["cases"]["complete"][0]["id"])
        self.assertEqual("task-coverage-bounded-stop", final_route["cases"]["continue"][0]["id"])
        self.assertFalse(any(node.get("type") == "gate" and "review" in node.get("message", "").lower()
                             for node in steps))
        self.assertFalse(any(command.startswith("speckit.flow-") or command.startswith("speckit.analyze")
                             for command in commands(steps)))
        manual = (ROOT / "workflows/README.md").read_text(encoding="utf-8").split(
            "## Manual task-generation path", 1
        )[1].split("## Manual analysis and remediation path", 1)[0]
        self.assertIn("without a routine pre-generation question", manual)
        self.assertIn("Stop with the exact material design gap", manual)
        self.assertIn("separately invoke Analyze", manual)

        initial = {"state": "continue", "next_step_id": "generate-tasks", "remaining_ids": ["COV-1", "COV-2"]}
        progress = {"state": "continue", "next_step_id": "generate-tasks", "remaining_ids": ["COV-2"],
                    "resolved_ids": ["COV-1"]}
        self.assertEqual({"action": "continue", "next_step_id": "generate-tasks"}, self.controller.route_loop_assessment(
            progress, iteration=1, max_iterations=5, loop_body_step_ids={"generate-tasks"},
            previous_assessment=initial,
        ))
        self.assertEqual({"action": "blocked", "blocker": "no-progress"}, self.controller.route_loop_assessment(
            {**initial, "resolved_ids": []}, iteration=1, max_iterations=5,
            loop_body_step_ids={"generate-tasks"}, previous_assessment=initial,
        ))

    def testConvergeRunsOrderedRemediationAndReassessesUntilCleanOrBoundedStop(self) -> None:
        workflow = load_workflow("speckit-flow-converge")
        steps = workflow["steps"]
        self.assertEqual("assess-convergence", steps[0]["id"])
        self.assertIn("next_step_id to assess-convergence-before-pass", steps[0]["prompt"])
        initial_route = find_step(steps, "route-initial-convergence")
        self.assertEqual({"complete", "continue", "needs-human", "blocked"}, set(initial_route["cases"]))
        self.assertEqual("convergence-remediation-loop", initial_route["cases"]["continue"][0]["id"])
        self.assertEqual("convergence-consequential-gate", initial_route["cases"]["needs-human"][0]["id"])
        self.assertEqual("convergence-initial-blocked-stop", initial_route["cases"]["blocked"][0]["id"])
        loop = find_step(steps, "convergence-remediation-loop")
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual("assess-convergence-before-pass", loop["steps"][0]["id"])
        self.assertEqual("assess-convergence-after-pass", loop["steps"][-1]["id"])
        self.assertIn("next_step_id to route-convergence-pass", loop["steps"][0]["prompt"])
        self.assertIn("convergence-final-consequential-gate", loop["steps"][0]["prompt"])
        self.assertEqual("{{ steps.assess-convergence-before-pass.output.reason_code }}",
                         find_step(steps, "select-convergence-remediation")["expression"])
        for branch_id, expected in {
            "append-task-remediation": ["speckit.converge", "speckit.analyze", "speckit.implement"],
            "reconcile-specification": ["speckit.converge", "speckit.specify", "speckit.plan", "speckit.tasks",
                                        "speckit.analyze", "speckit.implement"],
            "reconcile-plan": ["speckit.converge", "speckit.plan", "speckit.tasks", "speckit.analyze",
                               "speckit.implement"],
            "reconcile-tasks": ["speckit.converge", "speckit.tasks", "speckit.analyze", "speckit.implement"],
            "implement-eligible": ["speckit.implement"],
        }.items():
            branch = find_step(steps, "select-convergence-remediation")["cases"][branch_id]
            self.assertEqual(expected, commands(branch))
            if "speckit.analyze" in expected:
                self.assertLess(expected.index("speckit.analyze"), expected.index("speckit.implement"))
        final_route = find_step(steps, "route-final-convergence")
        self.assertEqual({"complete", "needs-human", "blocked", "continue", "default"}, set(final_route["cases"]))
        self.assertEqual("convergence-remediation-complete-stop", final_route["cases"]["complete"][0]["id"])
        self.assertEqual("convergence-loop-bounded-stop", final_route["cases"]["continue"][0]["id"])
        self.assertFalse(any(command.startswith("speckit.flow-") for command in commands(steps)))
        self.assertFalse(any("speckit-flow-closeout" in str(node) for node in steps))
        for gate_id in ("convergence-consequential-gate", "convergence-final-consequential-gate"):
            gate = find_step(steps, gate_id)
            self.assertEqual(["defer", "abort"], gate["options"])
            self.assertNotIn("flow_kit", gate)

        before = {"state": "continue", "next_step_id": "implement-eligible", "remaining_ids": ["GAP-1", "GAP-2"]}
        after = {"state": "continue", "next_step_id": "implement-eligible", "remaining_ids": ["GAP-2"],
                 "resolved_ids": ["GAP-1"]}
        self.assertEqual({"action": "continue", "next_step_id": "implement-eligible"},
                         self.controller.route_loop_assessment(
                             after, iteration=1, max_iterations=5,
                             loop_body_step_ids={"implement-eligible"}, previous_assessment=before,
                         ))
        self.assertEqual({"action": "blocked", "blocker": "no-progress"},
                         self.controller.route_loop_assessment(
                             {**before, "resolved_ids": []}, iteration=1, max_iterations=5,
                             loop_body_step_ids={"implement-eligible"}, previous_assessment=before,
                         ))
        self.assertEqual({"action": "blocked", "blocker": "loop-cap-exhausted"},
                         self.controller.route_loop_assessment(
                             after, iteration=5, max_iterations=5,
                             loop_body_step_ids={"implement-eligible"}, previous_assessment=before,
                         ))

    def testCloseoutCompletesOnlyWithEvidenceAndRepeatsDebriefBeforeExactPatchGate(self) -> None:
        workflow = load_workflow("speckit-flow-closeout")
        steps = workflow["steps"]
        self.assertIn("exact repository-relative spec directory", workflow["inputs"]["feature_context"]["prompt"])
        self.assertEqual("assess-closeout-readiness", steps[0]["id"])
        initial_route = find_step(steps, "route-initial-closeout")
        self.assertEqual({"complete", "continue", "needs-human", "blocked"}, set(initial_route["cases"]))
        self.assertEqual("closeout-debrief-loop", initial_route["cases"]["continue"][0]["id"])
        self.assertEqual("closeout-initial-consequential-gate", initial_route["cases"]["needs-human"][0]["id"])
        self.assertEqual("closeout-initial-blocked-stop", initial_route["cases"]["blocked"][0]["id"])
        initial_gate = initial_route["cases"]["needs-human"][0]
        self.assertEqual(["defer", "abort"], initial_gate["options"])
        self.assertFalse(any(node.get("type") == "gate" and "operation" in node.get("message", "").lower()
                             for node, _, _ in walk(steps)))

        loop = find_step(steps, "closeout-debrief-loop")
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual("assess-closeout-before-pass", loop["steps"][0]["id"])
        self.assertEqual("assess-closeout-after-pass", loop["steps"][-1]["id"])
        self.assertIn("Draft specification Complete", loop["steps"][0]["prompt"])
        self.assertIn("next_step_id to route-closeout-pass", loop["steps"][0]["prompt"])
        self.assertEqual("{{ steps.assess-closeout-before-pass.output.reason_code }}",
                         find_step(steps, "select-closeout-action")["expression"])

        for branch_id, expected in {
            "mark-spec-complete": ["speckit.specify", "speckit.flow-roadmap.debrief"],
            "debrief-current-spec": ["speckit.flow-roadmap.debrief"],
            "reconcile-specification": ["speckit.specify", "speckit.plan", "speckit.tasks", "speckit.analyze",
                                        "speckit.implement", "speckit.flow-roadmap.debrief"],
            "reconcile-plan": ["speckit.plan", "speckit.tasks", "speckit.analyze", "speckit.implement",
                               "speckit.flow-roadmap.debrief"],
            "reconcile-tasks": ["speckit.tasks", "speckit.analyze", "speckit.implement",
                                "speckit.flow-roadmap.debrief"],
            "implement-eligible": ["speckit.implement", "speckit.flow-roadmap.debrief"],
        }.items():
            branch = find_step(steps, "select-closeout-action")["cases"][branch_id]
            self.assertEqual(expected, commands(branch))
            if "speckit.analyze" in expected:
                self.assertLess(expected.index("speckit.analyze"), expected.index("speckit.implement"))

        final_route = find_step(steps, "route-final-closeout")
        self.assertEqual({"complete", "needs-human", "blocked", "continue", "default"}, set(final_route["cases"]))
        self.assertEqual("route-supported-roadmap-result", final_route["cases"]["complete"][0]["id"])
        self.assertEqual("closeout-loop-bounded-stop", final_route["cases"]["continue"][0]["id"])
        final_gate = find_step(steps, "closeout-final-consequential-gate")
        self.assertEqual(["defer", "abort"], final_gate["options"])
        final_gate_route = find_step(steps, "route-closeout-consequential-decision")
        self.assertEqual("{{ steps.closeout-final-consequential-gate.output.choice }}",
                         final_gate_route["expression"])
        patch_gate = find_step(steps, "approve-roadmap-transition")
        self.assertEqual(["approve-patch", "return-to-workflow", "defer"], patch_gate["options"])
        patch_route = find_step(steps, "route-roadmap-transition")
        self.assertEqual("apply-approved-roadmap-verification",
                         patch_route["cases"]["approve-patch"][0]["id"])
        for choice in ("return-to-workflow", "defer"):
            self.assertNotIn("speckit.flow-roadmap.write", commands(patch_route["cases"][choice]))
        for node, _, _ in walk(steps):
            if node.get("command") in {"speckit.flow-roadmap.debrief", "speckit.flow-roadmap.write"}:
                self.assertIn("SPEC_TARGET={{ inputs.feature_context }}", node["input"]["args"])
        self.assertFalse(any(command.startswith("speckit-flow-") or command == "speckit.flow-closeout"
                             for command in commands(steps)))

        before = {"state": "continue", "next_step_id": "debrief-current-spec", "remaining_ids": ["FIND-1", "FIND-2"]}
        after = {"state": "continue", "next_step_id": "debrief-current-spec", "remaining_ids": ["FIND-2"],
                 "resolved_ids": ["FIND-1"]}
        self.assertEqual({"action": "continue", "next_step_id": "debrief-current-spec"},
                         self.controller.route_loop_assessment(
                             after, iteration=1, max_iterations=5,
                             loop_body_step_ids={"debrief-current-spec"}, previous_assessment=before,
                         ))
        self.assertEqual({"action": "blocked", "blocker": "no-progress"},
                         self.controller.route_loop_assessment(
                             {**before, "resolved_ids": []}, iteration=1, max_iterations=5,
                             loop_body_step_ids={"debrief-current-spec"}, previous_assessment=before,
                         ))
        self.assertEqual({"action": "blocked", "blocker": "loop-cap-exhausted"},
                         self.controller.route_loop_assessment(
                             after, iteration=5, max_iterations=5,
                             loop_body_step_ids={"debrief-current-spec"}, previous_assessment=before,
                         ))


if __name__ == "__main__":
    unittest.main()

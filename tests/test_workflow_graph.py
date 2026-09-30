"""Machine-checkable branch and gate coverage for every FlowKit workflow."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_step(nodes: list[dict], step_id: str) -> dict | None:
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


def commands(nodes: list[dict]) -> list[str]:
    result = []
    for node in nodes:
        if "command" in node:
            result.append(node["command"])
        for branch in node.get("cases", {}).values() if isinstance(node.get("cases"), dict) else []:
            result.extend(commands(branch))
        result.extend(commands(node.get("default", [])))
        result.extend(commands(node.get("steps", [])))
    return result


class WorkflowGraphInventoryTests(unittest.TestCase):
    """Every source workflow has a static projection of its complete graph."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = load_module("flowkit_workflow_inventory", ROOT / "tools/validate_workflows.py")

    def test_activeAndDeprecatedWorkflowsExposeStopsAndAssignmentsWithRequiredGates(self) -> None:
        projections = [self.inventory.project_workflow(item) for item in self.inventory.load_workflows()]
        expected = {
            "speckit-flow-start-feature", "speckit-flow-select-feature", "speckit-flow-specify", "speckit-flow-clarify", "speckit-flow-plan", "speckit-flow-tasks",
            "speckit-flow-analyze-remediate", "speckit-flow-implement", "speckit-flow-converge", "speckit-flow-closeout", "speckit-flow-wiki-lint-update",
        }
        self.assertEqual(expected, {item["workflow_id"] for item in projections})
        for projection in projections:
            with self.subTest(workflow=projection["workflow_id"]):
                self.assertTrue(projection["entry_step_id"])
                if projection["workflow_id"] == "speckit-flow-start-feature":
                    self.assertFalse(projection["assignments"])
                    self.assertFalse(projection["branches"])
                    continue
                if projection["workflow_id"] in {"speckit-flow-clarify", "speckit-flow-implement", "speckit-flow-plan", "speckit-flow-tasks", "speckit-flow-analyze-remediate", "speckit-flow-converge", "speckit-flow-wiki-lint-update"}:
                    if projection["workflow_id"] in {"speckit-flow-analyze-remediate", "speckit-flow-converge", "speckit-flow-wiki-lint-update"}:
                        self.assertTrue(projection["branches"])
                    else:
                        self.assertFalse(projection["branches"])
                    self.assertFalse(projection["human_decisions"])
                else:
                    self.assertTrue(projection["branches"])
                    self.assertTrue(projection["human_decisions"])
                self.assertTrue(projection["assignments"])
                self.assertIn("unexplained_terminal_paths", projection)
        analyze = next(item for item in projections if item["workflow_id"] == "speckit-flow-analyze-remediate")
        implement = next(item for item in projections if item["workflow_id"] == "speckit-flow-implement")
        self.assertEqual("analysis-remediation-loop", analyze["entry_step_id"])
        self.assertTrue(analyze["continuation_edges"])
        self.assertEqual("assess-implementation-state", implement["entry_step_id"])
        self.assertTrue(implement["continuation_edges"])
        self.assertTrue(all(not item["unexplained_terminal_paths"] for item in projections))
        returned = {
            item["workflow_id"]: {path["terminal_step_id"] for path in item["bounded_stops"]
                                   if path.get("reason") == "operator-selected-return-command-ends-current-workflow"}
            for item in projections
        }
        self.assertEqual(set(), returned["speckit-flow-plan"])
        self.assertEqual(set(), returned["speckit-flow-tasks"])

    def testOnlyGatedReturnCommandsReceiveTheExplicitBoundedReturnClassification(self) -> None:
        definition = {
            "workflow": {"id": "fixture", "version": "1.0"},
            "steps": [
                {"id": "decision", "type": "gate", "options": ["return"]},
                {"id": "route", "type": "switch", "cases": {
                    "return": [{"id": "return-to-plan", "command": "speckit.plan"}],
                }},
            ],
        }
        projection = self.inventory.project_workflow(definition)
        self.assertEqual([], projection["unexplained_terminal_paths"])
        self.assertEqual("operator-selected-return-command-ends-current-workflow",
                         projection["bounded_stops"][0]["reason"])

    def test_unexplainedTerminalDetectionReportsUnclassifiedLeaf(self) -> None:
        definition = {
            "workflow": {"id": "fixture", "version": "1.0"},
            "steps": [{"id": "finish", "type": "prompt", "prompt": "Continue working."}],
        }
        projection = self.inventory.project_workflow(definition)
        self.assertEqual("finish", projection["unexplained_terminal_paths"][0]["terminal_step_id"])
        explained = {
            **definition,
            "steps": [{"id": "finish", "type": "prompt", "prompt": "Stop with the bounded blocker."}],
        }
        self.assertEqual([], self.inventory.project_workflow(explained)["unexplained_terminal_paths"])

    def testInventoryCLIListsAllWorkflows(self) -> None:
        projections = [self.inventory.project_workflow(item) for item in self.inventory.load_workflows()]
        self.assertEqual(11, len(projections))
        self.assertTrue(all("continuation_edges" in item and "bounded_stops" in item for item in projections))

    def testSelectionAndSpecificationSeparateMutationAuthority(self) -> None:
        workflows = {w["workflow"]["id"]: w for w in self.inventory.load_workflows()}
        selection = workflows["speckit-flow-select-feature"]
        authoring = workflows["speckit-flow-specify"]
        self.assertEqual(["speckit.flow-roadmap.write"], commands(selection["steps"]))
        self.assertNotIn("speckit.specify", commands(selection["steps"]))
        self.assertEqual(2, len(self.inventory.project_workflow(selection)["human_decisions"]))
        self.assertEqual(1, len(self.inventory.project_workflow(authoring)["human_decisions"]))
        self.assertEqual("inspect-active-feature", authoring["steps"][0]["id"])
        self.assertEqual(["speckit.flow-wiki.query", "speckit.specify", "speckit.flow-roadmap.write", "speckit.flow-roadmap.brief"], commands(authoring["steps"]))
        deprecated = workflows["speckit-flow-start-feature"]
        self.assertTrue(deprecated["workflow"]["deprecated"])
        self.assertEqual([], commands(deprecated["steps"]))
        self.assertEqual(1, len(deprecated["steps"]))

    def testPlanGraphLoopsThroughCorePlanningAndOutputVerification(self) -> None:
        workflow = next(item for item in self.inventory.load_workflows()
                        if item["workflow"]["id"] == "speckit-flow-plan")
        self.assertEqual(["plan-output-loop", "report-plan-outcome"],
                         [step["id"] for step in workflow["steps"]])
        self.assertEqual(["speckit.plan"], commands(workflow["steps"]))
        graph = self.inventory.project_workflow(workflow)
        self.assertFalse(graph["branches"])
        self.assertFalse(graph["human_decisions"])
        self.assertTrue(graph["continuation_edges"])
        self.assertFalse(graph["unexplained_terminal_paths"])

    def testClarifyGraphKeepsOperatorQuestionsAndNeverStartsPlan(self) -> None:
        workflow = next(item for item in self.inventory.load_workflows()
                        if item["workflow"]["id"] == "speckit-flow-clarify")
        steps = workflow["steps"]
        loop = find_step(steps, "clarification-session-loop")
        self.assertEqual(5, loop["max_iterations"])
        command_ids = {node.get("id") for node, _, _ in self.inventory._walk(steps) if "command" in node}
        self.assertEqual({"clarify-session"}, command_ids)
        self.assertEqual(["clarify-session", "assess-clarification-after-session"],
                         [node["id"] for node in loop["steps"]])
        readme = (ROOT / "workflows/README.md").read_text(encoding="utf-8")
        manual = readme.split("## Manual clarification path", 1)[1].split("## Manual planning path", 1)[0]
        self.assertIn("five-question cap applies per session", manual)
        self.assertIn("same invocation", manual)
        self.assertIn("wait for the operator's answer", manual)
        self.assertIn("without invoking Plan", manual)

    def testTasksGraphUsesOnlyCoreSkillAndOutputLoop(self) -> None:
        workflow = next(item for item in self.inventory.load_workflows()
                        if item["workflow"]["id"] == "speckit-flow-tasks")
        self.assertEqual(["tasks-output-loop", "report-task-outcome"],
                         [step["id"] for step in workflow["steps"]])
        self.assertEqual(["speckit.tasks"], commands(workflow["steps"]))
        graph = self.inventory.project_workflow(workflow)
        self.assertFalse(graph["branches"])
        self.assertFalse(graph["human_decisions"])
        self.assertTrue(graph["continuation_edges"])
        self.assertFalse(graph["unexplained_terminal_paths"])
        manual = (ROOT / "workflows/README.md").read_text().split(
            "## Manual task-generation path", 1)[1].split("## Manual analysis and remediation path", 1)[0]
        self.assertIn("without a routine pre-generation question", manual)
        self.assertIn("separately invoke Analyze", manual)
        self.assertIn("preserving task IDs, completion markers", manual)

    def testConvergeGraphOrdersRemediationAndStopsWithoutStartingCloseOut(self) -> None:
        workflow = next(item for item in self.inventory.load_workflows()
                        if item["workflow"]["id"] == "speckit-flow-converge")
        steps = workflow["steps"]
        loop, report = steps
        self.assertEqual("convergence-remediation-loop", loop["id"])
        self.assertTrue(loop["assessment_before_correction"])
        self.assertEqual(6, loop["max_iterations"])
        self.assertEqual("assess-convergence", loop["steps"][1]["id"])
        self.assertEqual("report-convergence-outcome", report["id"])
        self.assertEqual(["speckit.converge", "speckit.specify", "speckit.plan", "speckit.tasks",
                          "speckit.analyze", "speckit.implement"], commands(steps))
        eligibility = find_step(steps, "route-remediation-implementation")
        self.assertEqual({"continue", "complete", "blocked"}, set(eligibility["cases"]))
        for state in ("complete", "blocked"):
            self.assertEqual([], eligibility["cases"][state])
        self.assertFalse(any(command.startswith("speckit.flow-") for command in commands(steps)))
        self.assertFalse(any(node.get("type") == "gate" for node, _, _ in self.inventory._walk(steps)))
        manual = (ROOT / "workflows/README.md").read_text(encoding="utf-8").split(
            "## Manual convergence path", 1
        )[1].split("## Manual closeout path", 1)[0]
        self.assertIn("same invocation", manual)
        self.assertIn("Analyze changed tasks before implementation", manual)
        self.assertIn("separate operator instruction", manual)

    def testCloseoutGraphSharesCorrectionAndMaintainsVerifiedContext(self) -> None:
        workflow = next(item for item in self.inventory.load_workflows()
                        if item["workflow"]["id"] == "speckit-flow-closeout")
        steps = workflow["steps"]
        self.assertEqual("assess-closeout-readiness", steps[0]["id"])
        loop = find_step(steps, "closeout-debrief-loop")
        self.assertTrue(loop["assessment_before_correction"])
        self.assertEqual(6, loop["max_iterations"])
        self.assertEqual("debrief-roadmap", loop["steps"][0]["id"])
        self.assertEqual("assess-closeout-debrief", loop["steps"][1]["id"])
        self.assertEqual({"continue", "complete", "blocked"}, set(loop["steps"][2]["cases"]))
        self.assertEqual("report-closeout-outcome", steps[-1]["id"])
        self.assertEqual(1, commands(steps).count("speckit.flow-roadmap.debrief"))
        self.assertEqual(1, commands(steps).count("speckit.plan"))
        self.assertEqual(1, commands(steps).count("speckit.tasks"))
        self.assertEqual(1, sum(n.get("type") == "gate" for n, _, _ in self.inventory._walk(steps)))
        self.assertEqual([], self.inventory.project_workflow(workflow)["unexplained_terminal_paths"])
        manual = (ROOT / "workflows/README.md").read_text().split("## Manual closeout path", 1)[1]
        for phrase in ("in-place Draft-to-Complete", "rerun debrief", "exact roadmap verification patch", "does not commit"):
            self.assertIn(phrase, manual)


if __name__ == "__main__":
    unittest.main()

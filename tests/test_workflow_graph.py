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

    def test_allEightWorkflowsExposeStopsAndAssignmentsWithRequiredGates(self) -> None:
        projections = [self.inventory.project_workflow(item) for item in self.inventory.load_workflows()]
        expected = {
            "speckit-flow-start-feature", "speckit-flow-clarify", "speckit-flow-plan", "speckit-flow-tasks",
            "speckit-flow-analyze-remediate", "speckit-flow-implement", "speckit-flow-converge", "speckit-flow-closeout",
        }
        self.assertEqual(expected, {item["workflow_id"] for item in projections})
        for projection in projections:
            with self.subTest(workflow=projection["workflow_id"]):
                self.assertTrue(projection["entry_step_id"])
                if projection["workflow_id"] in {"speckit-flow-clarify", "speckit-flow-implement", "speckit-flow-plan", "speckit-flow-tasks"}:
                    self.assertFalse(projection["branches"])
                    self.assertFalse(projection["human_decisions"])
                else:
                    self.assertTrue(projection["branches"])
                    self.assertTrue(projection["human_decisions"])
                self.assertTrue(projection["assignments"])
                self.assertIn("unexplained_terminal_paths", projection)
        analyze = next(item for item in projections if item["workflow_id"] == "speckit-flow-analyze-remediate")
        implement = next(item for item in projections if item["workflow_id"] == "speckit-flow-implement")
        self.assertTrue(analyze["success_paths"])
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
        self.assertEqual(8, len(projections))
        self.assertTrue(all("continuation_edges" in item and "bounded_stops" in item for item in projections))

    def testStartFeatureManualFallbackAndLinkageFixtureStayExplicit(self) -> None:
        workflow = next(item for item in self.inventory.load_workflows()
                        if item["workflow"]["id"] == "speckit-flow-start-feature")
        graph = self.inventory.project_workflow(workflow)
        self.assertEqual("0.5.0", graph["version"])
        self.assertIn("assess-created-spec-linkage", {item["step_id"] for item in graph["nodes"]})
        self.assertIn("verify-repaired-spec-linkage", {item["step_id"] for item in graph["nodes"]})
        readme = (ROOT / "workflows/README.md").read_text(encoding="utf-8")
        manual = readme.split("## Manual start-feature path", 1)[1].split("## Manual clarification path", 1)[0]
        for required in (
            "exact roadmap entry identifier", "Never infer the entry from its feature number alone",
            "SPEC_TARGET", "ROADMAP_ENTRY", "minimal exact `Spec dir` patch",
            "Apply only that exact approved patch", "no other entry claims that directory",
            "no punctuation before the closing backtick",
            "Amendment or deferral makes no roadmap change",
        ):
            self.assertIn(required, manual)
        fixture = json.loads((ROOT / "tests/consumer-fixtures/start-feature-linkage.json").read_text(encoding="utf-8"))
        self.assertEqual(8, len(fixture["scenarios"]))
        self.assertEqual({"linked", "repairable", "conflict", "ambiguous"},
                         {case["observed_state"] for case in fixture["scenarios"]})

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
        self.assertEqual("assess-convergence", steps[0]["id"])
        route = find_step(steps, "route-initial-convergence")
        self.assertEqual({"complete", "continue", "needs-human", "blocked"}, set(route["cases"]))
        self.assertEqual("convergence-clean-stop", route["cases"]["complete"][0]["id"])
        self.assertEqual("convergence-remediation-loop", route["cases"]["continue"][0]["id"])
        loop = find_step(steps, "convergence-remediation-loop")
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual("assess-convergence-before-pass", loop["steps"][0]["id"])
        self.assertEqual("assess-convergence-after-pass", loop["steps"][-1]["id"])
        route = find_step(steps, "select-convergence-remediation")
        expected = {
            "append-task-remediation": ["speckit.converge", "speckit.analyze", "speckit.implement"],
            "reconcile-specification": ["speckit.converge", "speckit.specify", "speckit.plan", "speckit.tasks",
                                        "speckit.analyze", "speckit.implement"],
            "reconcile-plan": ["speckit.converge", "speckit.plan", "speckit.tasks", "speckit.analyze",
                               "speckit.implement"],
            "reconcile-tasks": ["speckit.converge", "speckit.tasks", "speckit.analyze", "speckit.implement"],
            "implement-eligible": ["speckit.implement"],
        }
        for branch, ordered_commands in expected.items():
            actual = commands(route["cases"][branch])
            self.assertEqual(ordered_commands, actual)
            if "speckit.analyze" in actual:
                self.assertLess(actual.index("speckit.analyze"), actual.index("speckit.implement"))
        final = find_step(steps, "route-final-convergence")
        self.assertEqual({"complete", "needs-human", "blocked", "continue", "default"}, set(final["cases"]))
        self.assertFalse(any(command.startswith("speckit.flow-") for command in commands(steps)))
        self.assertFalse(any("speckit-flow-closeout" in str(node) for node, _, _ in self.inventory._walk(steps)))
        manual = (ROOT / "workflows/README.md").read_text(encoding="utf-8").split(
            "## Manual convergence path", 1
        )[1].split("## Manual closeout path", 1)[0]
        self.assertIn("same invocation", manual)
        self.assertIn("Analyze changed tasks before implementation", manual)
        self.assertIn("separate operator instruction", manual)

    def testCloseoutGraphContinuesDebriefAndRetainsIndependentApprovalGates(self) -> None:
        workflow = next(item for item in self.inventory.load_workflows()
                        if item["workflow"]["id"] == "speckit-flow-closeout")
        steps = workflow["steps"]
        self.assertEqual("assess-closeout-readiness", steps[0]["id"])
        route = find_step(steps, "route-initial-closeout")
        self.assertEqual({"complete", "continue", "needs-human", "blocked"}, set(route["cases"]))
        self.assertEqual("closeout-debrief-loop", route["cases"]["continue"][0]["id"])
        loop = find_step(steps, "closeout-debrief-loop")
        self.assertEqual(5, loop["max_iterations"])
        self.assertEqual("assess-closeout-before-pass", loop["steps"][0]["id"])
        self.assertEqual("assess-closeout-after-pass", loop["steps"][-1]["id"])
        self.assertEqual("route-supported-roadmap-result",
                         find_step(steps, "route-final-closeout")["cases"]["complete"][0]["id"])
        self.assertEqual("closeout-loop-bounded-stop",
                         find_step(steps, "route-final-closeout")["cases"]["continue"][0]["id"])
        patch_gate = find_step(steps, "approve-roadmap-transition")
        self.assertEqual(["approve-patch", "return-to-workflow", "defer"], patch_gate["options"])
        patch_route = find_step(steps, "route-roadmap-transition")
        self.assertEqual("apply-approved-roadmap-verification",
                         patch_route["cases"]["approve-patch"][0]["id"])
        for choice in ("return-to-workflow", "defer"):
            self.assertFalse(any(node.get("id") == "apply-approved-roadmap-verification"
                                 for node, _, _ in self.inventory._walk(patch_route["cases"][choice])))
        self.assertEqual([], self.inventory.project_workflow(workflow)["unexplained_terminal_paths"])
        manual = (ROOT / "workflows/README.md").read_text(encoding="utf-8").split(
            "## Manual closeout path", 1
        )[1]
        self.assertIn("in-place Draft-to-Complete", manual)
        self.assertIn("rerun debrief", manual)
        self.assertIn("exact roadmap verification patch", manual)
        self.assertIn("does not commit", manual)


if __name__ == "__main__":
    unittest.main()

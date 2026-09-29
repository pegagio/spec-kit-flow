#!/usr/bin/env python3
"""Read and preflight an installed FlowKit workflow for a Codex task."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from specify_cli.workflows.engine import WorkflowEngine
except ImportError:  # The controller is executed with the selected Specify runtime.
    WorkflowEngine = None  # type: ignore[assignment,misc]


REVIEWED_AGENT_NAMES = {"Architect", "Builder", "Coder", "Verifier"}
INPUT_REFERENCE = re.compile(r"\{\{\s*inputs\.([A-Za-z0-9_-]+)\s*\}\}")
STEP_REFERENCE = re.compile(r"\{\{\s*steps\.([A-Za-z0-9_-]+)\.output\.([A-Za-z0-9_.-]+)\s*\}\}")


@dataclass(frozen=True)
class StepAssignmentIntent:
    """Identify the native Codex agent assigned to one delegated workflow step."""

    step_id: str
    agent_name: str

    def to_dict(self) -> dict[str, str]:
        """Return the portable representation used by controller output and recovery."""
        return asdict(self)


def select_specify_executable(mise_selected: Path | None, path_candidates: Iterable[Path]) -> Path:
    """Choose the selected mise runtime or one unambiguous PATH executable."""
    candidates = list(dict.fromkeys(Path(item) for item in path_candidates))
    if mise_selected is not None:
        selected = Path(mise_selected)
        if not selected.is_file() or not os.access(selected, os.X_OK):
            raise ValueError("mise-selected Specify executable is missing or not executable")
        return selected
    if not candidates:
        raise ValueError("Specify executable not found in mise or PATH")
    if len(candidates) != 1:
        raise ValueError("ambiguous Specify executables in PATH")
    selected = candidates[0]
    if not selected.is_file() or not os.access(selected, os.X_OK):
        raise ValueError("Specify executable is missing or not executable")
    return selected


def check_specify_version(actual_output: str, expected_version: str) -> str:
    """Require the selected Specify CLI to match the controller package pin."""
    actual = actual_output.strip()
    expected = f"specify {expected_version}"
    if actual != expected:
        raise ValueError(f"expected Specify {expected_version}, found {actual or 'no version output'}")
    return actual


def load_installed_definition(project_root: Path, workflow_id: str) -> dict[str, Any]:
    """Load the composed workflow definition without creating native run state."""
    if WorkflowEngine is None:
        raise RuntimeError("Specify workflow loader is unavailable in this Python runtime")
    project = Path(project_root).resolve()
    definition = WorkflowEngine(project).load_workflow(workflow_id)
    data = definition.data
    metadata = data.get("workflow", {})
    if metadata.get("id") != workflow_id:
        raise ValueError(f"loaded workflow ID mismatch: expected {workflow_id}, found {metadata.get('id')}")
    source_path = getattr(definition, "source_path", None)
    if source_path:
        try:
            source_path = Path(source_path).resolve().relative_to(project.resolve()).as_posix()
        except ValueError:
            source_path = None
    serialized = json.loads(json.dumps(data))
    return {
        "workflow": serialized["workflow"],
        "version": metadata.get("version"),
        "inputs": serialized.get("inputs", {}),
        "steps": serialized.get("steps", []),
        "requires": serialized.get("requires", {}),
        "source_path": source_path,
        "sha256": hashlib.sha256(json.dumps(serialized, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
    }


def validate_workflow_definition(definition: dict[str, Any]) -> None:
    """Validate named-agent metadata placement before returning a workflow graph."""
    workflow = definition.get("workflow", {})
    if any(key in workflow for key in ("agent", "model", "reasoning_effort", "default_agent", "default_model", "default_reasoning_effort")):
        raise ValueError("workflow-level agent and model defaults are unsupported")
    if any(key in definition for key in ("agent", "model", "reasoning_effort", "default_agent", "default_model", "default_reasoning_effort")):
        raise ValueError("top-level agent and model defaults are unsupported")
    if not isinstance(workflow.get("id"), str) or not isinstance(workflow.get("version"), str):
        raise ValueError("workflow ID and version must be strings")
    validate_workflow_graph(definition["steps"])
    collect_agent_assignments(definition["steps"])
    validate_template_forms(definition["steps"], set(definition.get("inputs", {})))


def validate_template_forms(steps: list[dict[str, Any]], input_names: set[str]) -> None:
    """Reject unsupported expressions anywhere in the installed step graph."""
    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, str) and ("{{" in value or "}}" in value):
            expressions = re.findall(r"\{\{.*?\}\}", value, flags=re.DOTALL)
            for expression in expressions:
                input_match = INPUT_REFERENCE.fullmatch(expression)
                if input_match:
                    if input_match.group(1) not in input_names:
                        raise ValueError(f"unsupported template input: {input_match.group(1)}")
                elif not STEP_REFERENCE.fullmatch(expression):
                    raise ValueError("unsupported template expression in workflow graph")
            remainder = re.sub(r"\{\{.*?\}\}", "", value, flags=re.DOTALL)
            if "{{" in remainder or "}}" in remainder:
                raise ValueError("unsupported template expression in workflow graph")

    visit(steps)


def file_fingerprint(path: Path) -> dict[str, int | str] | None:
    """Return stable content and file-identity evidence, or None if absent."""
    candidate = Path(path)
    try:
        details = candidate.stat()
        content_digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(details.st_mode):
        raise ValueError(f"installation record is not a regular file: {candidate.name}")
    return {"sha256": content_digest, "device": details.st_dev, "inode": details.st_ino}


def installation_fingerprints(project_root: Path) -> dict[str, dict[str, int | str] | None]:
    """Snapshot both Specify and FlowKit installation records without writing."""
    root = Path(project_root)
    return {
        "bundle_record": file_fingerprint(root / ".specify/bundle-records.json"),
        "skill_record": file_fingerprint(root / ".specify/flow-kit/skills-install.json"),
    }


def verify_controller_install(project_root: Path, skill_id: str, workflow_id: str) -> dict[str, Any]:
    """Verify the selected skill and shared helper against their ownership record."""
    project = Path(project_root)
    record_path = project / ".specify/flow-kit/skills-install.json"
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"FlowKit controller ownership record is missing or unreadable: {error}") from error
    if record.get("package") != "flow-kit-controllers" or record.get("status") != "installed":
        raise ValueError("FlowKit controller package is not in installed state")
    controllers = record.get("controllers")
    matches = [item for item in controllers or [] if item.get("skill_id") == skill_id]
    if len(matches) != 1 or matches[0].get("workflow_id") != workflow_id:
        raise ValueError("FlowKit skill-to-workflow binding differs from the installed ownership record")
    owned_files = record.get("files")
    if not isinstance(owned_files, dict):
        raise ValueError("FlowKit controller ownership file inventory is malformed")
    required = {
        f".agents/skills/{skill_id}/SKILL.md",
        f".agents/skills/{skill_id}/agents/openai.yaml",
        ".specify/flow-kit/manifest.yml",
        ".specify/flow-kit/controller-protocol.md",
        ".specify/flow-kit/scripts/bootstrap.sh",
        ".specify/flow-kit/scripts/python/controller.py",
        ".specify/flow-kit/scripts/python/recovery.py",
    }
    for relative in required:
        expected = owned_files.get(relative)
        target = project / relative
        if not isinstance(expected, str) or not target.is_file():
            raise ValueError(f"FlowKit-owned controller file is missing: {relative}")
        observed = hashlib.sha256(target.read_bytes()).hexdigest()
        if observed != expected:
            raise ValueError(f"FlowKit-owned controller file was changed: {relative}")
    installed_manifest = (project / ".specify/flow-kit/manifest.yml").read_text(encoding="utf-8")
    manifest_version = re.search(r'^  version:\s*["\']?([^"\'\n]+)', installed_manifest.split("package:\n", 1)[1], re.MULTILINE)
    if manifest_version is None or manifest_version.group(1).strip() != record.get("version"):
        raise ValueError("FlowKit controller manifest version differs from the installation record")
    skill_text = (project / f".agents/skills/{skill_id}/SKILL.md").read_text(encoding="utf-8")
    declared_name = re.search(r"^name:\s*([^\n]+)", skill_text, re.MULTILINE)
    if declared_name is None or declared_name.group(1).strip() != skill_id:
        raise ValueError("installed FlowKit skill frontmatter differs from its ID")
    return record


def _node_kind(step: dict[str, Any]) -> str:
    if "type" in step:
        return str(step["type"])
    if "command" in step:
        return "command"
    if "prompt" in step or "input" in step:
        return "prompt"
    return "unknown"


def validate_workflow_graph(steps: list[dict[str, Any]]) -> None:
    """Reject unsupported nodes, duplicate IDs, and invalid model placement."""
    seen: set[str] = set()

    def visit(nodes: list[dict[str, Any]]) -> None:
        for node in nodes:
            if not isinstance(node, dict):
                raise ValueError("workflow step must be a mapping")
            step_id = node.get("id")
            if not isinstance(step_id, str) or not step_id.strip():
                raise ValueError("workflow step is missing a nonempty id")
            if step_id in seen:
                raise ValueError(f"duplicate step id: {step_id}")
            seen.add(step_id)
            kind = _node_kind(node)
            if kind not in {"prompt", "command", "gate", "switch"}:
                raise ValueError(f"unsupported workflow step type {kind}: {step_id}")
            if kind == "command" and node.get("integration") not in (None, "codex", "{{ inputs.integration }}"):
                raise ValueError(f"unsupported command integration on step {step_id}")
            if "model" in node or "reasoning_effort" in node:
                raise ValueError(f"concrete model and effort settings are unsupported on step {step_id}; use a named Codex agent")
            if "agent" in node or "delegated" in node:
                raise ValueError(f"agent assignment on step {step_id} must use explicit flow_kit metadata")
            assignment = node.get("flow_kit")
            if "flow_kit" in node:
                if kind not in {"prompt", "command"}:
                    raise ValueError(f"agent delegation is not allowed on {kind} step {step_id}")
                if not isinstance(assignment, dict) or set(assignment) != {"delegated", "agent"} or assignment.get("delegated") is not True:
                    raise ValueError(f"flow_kit metadata must explicitly delegate step {step_id}")
                agent_name = assignment.get("agent")
                if not isinstance(agent_name, str) or agent_name not in REVIEWED_AGENT_NAMES:
                    raise ValueError(f"step {step_id} names an unknown or invalid Codex agent: {agent_name!r}")
            if kind == "switch":
                cases = node.get("cases", {})
                if not isinstance(cases, dict):
                    raise ValueError(f"switch cases must be a mapping: {step_id}")
                for branch in cases.values():
                    if not isinstance(branch, list):
                        raise ValueError(f"switch case must contain a step list: {step_id}")
                    visit(branch)
                default = node.get("default", [])
                if not isinstance(default, list):
                    raise ValueError(f"switch default must contain a step list: {step_id}")
                visit(default)

    if not isinstance(steps, list):
        raise ValueError("workflow steps must be a list")
    visit(steps)


def validate_required_inputs(workflow: dict[str, Any], supplied: dict[str, Any]) -> dict[str, Any]:
    """Apply declared defaults and reject missing required workflow inputs."""
    declared = workflow.get("inputs", {})
    values: dict[str, Any] = {}
    unknown = sorted(set(supplied) - set(declared))
    if unknown:
        raise ValueError(f"unknown workflow input: {', '.join(unknown)}")
    for name, definition in declared.items():
        if name in supplied:
            values[name] = supplied[name]
        elif "default" in definition:
            values[name] = definition["default"]
        elif definition.get("required"):
            raise ValueError(f"missing required workflow input: {name}")
        if name in values:
            expected_type = definition.get("type")
            if expected_type == "string" and not isinstance(values[name], str):
                raise ValueError(f"workflow input must be a string: {name}")
            if definition.get("required") and isinstance(values[name], str) and not values[name].strip():
                raise ValueError(f"missing required workflow input: {name}")
            options = definition.get("enum")
            if options and values[name] not in options:
                raise ValueError(f"workflow input is not an allowed value: {name}")
    return values


def parse_key_values(arguments: list[str] | None, *, argument_name: str) -> dict[str, str]:
    """Parse unique key=value CLI tokens without printing supplied values."""
    values: dict[str, str] = {}
    for token in arguments or []:
        if "=" not in token:
            raise ValueError(f"{argument_name} must use key=value syntax")
        key, value = token.split("=", 1)
        if not key or key in values:
            raise ValueError(f"{argument_name} key is empty or repeated: {key}")
        values[key] = value
    return values


def collect_agent_assignments(steps: list[dict[str, Any]]) -> list[StepAssignmentIntent]:
    """Enumerate explicitly delegated steps and their native agent names across every branch."""
    validate_workflow_graph(steps)

    def collect(nodes: list[dict[str, Any]]) -> list[StepAssignmentIntent]:
        assignments: list[StepAssignmentIntent] = []
        for step in nodes:
            step_id = step["id"]
            kind = _node_kind(step)
            assignment = step.get("flow_kit")
            if "flow_kit" in step:
                assignments.append(StepAssignmentIntent(step_id=step_id, agent_name=assignment["agent"]))
            if kind == "switch":
                for branch in step.get("cases", {}).values():
                    assignments.extend(collect(branch))
                assignments.extend(collect(step.get("default", [])))
        return assignments

    return collect(steps)


def render_template(value: Any, inputs: dict[str, Any], outputs: dict[str, dict[str, Any]]) -> Any:
    """Render only the documented input and prior-step-output references."""
    if isinstance(value, list):
        return [render_template(item, inputs, outputs) for item in value]
    if isinstance(value, dict):
        return {key: render_template(item, inputs, outputs) for key, item in value.items()}
    if not isinstance(value, str):
        return value

    def input_value(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in inputs:
            raise ValueError(f"unresolved input reference: {name}")
        return str(inputs[name])

    rendered = INPUT_REFERENCE.sub(input_value, value)

    def output_value(match: re.Match[str]) -> str:
        step_id, key_path = match.groups()
        current: Any = outputs.get(step_id)
        for key in key_path.split("."):
            if not isinstance(current, dict) or key not in current:
                raise ValueError(f"unresolved step output reference: {step_id}.{key_path}")
            current = current[key]
        return str(current)

    rendered = STEP_REFERENCE.sub(output_value, rendered)
    if "{{" in rendered or "}}" in rendered:
        raise ValueError(f"unsupported or unresolved template expression: {rendered}")
    return rendered


def installed_skill_name(command_id: str) -> str:
    """Apply the pinned Specify command-to-skill naming rule."""
    return command_id.replace(".", "-")


def resolve_installed_skill(project_root: Path, command_id: str) -> dict[str, str]:
    """Find exactly one project-local Codex skill matching a Specify command."""
    expected_name = installed_skill_name(command_id)
    project = Path(project_root)
    roots = [project / ".agents/skills", project / ".codex/skills"]
    matches: list[Path] = []
    for root in roots:
        candidate = root / expected_name / "SKILL.md"
        if candidate.is_file():
            matches.append(candidate)
    if not matches:
        raise ValueError(f"installed Codex command skill not found: {expected_name}")
    if len(matches) > 1:
        raise ValueError(f"ambiguous installed Codex command skill: {expected_name}")
    skill_file = matches[0]
    text = skill_file.read_text(encoding="utf-8")
    name_match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, re.MULTILINE)
    if name_match is None or name_match.group(1).strip() != expected_name:
        raise ValueError(f"installed Codex skill declares a different name: {expected_name}")
    project_relative = skill_file.relative_to(project).as_posix()
    provenance: str | None = None
    manifest_path = project / ".specify/integrations/codex.manifest.json"
    if manifest_path.is_file():
        try:
            integration_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError("selected project's Codex skill provenance manifest is malformed") from error
        recorded_digest = integration_manifest.get("files", {}).get(project_relative)
        actual_digest = hashlib.sha256(skill_file.read_bytes()).hexdigest()
        if recorded_digest is None:
            raise ValueError(f"selected project's Codex manifest has no skill provenance: {expected_name}")
        if recorded_digest != actual_digest:
            raise ValueError(f"installed Codex command skill differs from its provenance record: {expected_name}")
        provenance = "codex.manifest.json"
    return {"name": expected_name, "path": str(skill_file), "command_id": command_id, "provenance": provenance or "unrecorded"}


def validate_child_question(request: dict[str, Any], expected_step_id: str) -> dict[str, Any]:
    """Validate one child question before presenting it in the main task."""
    if not isinstance(request, dict) or request.get("kind") != "question":
        raise ValueError("child request must have kind question")
    if request.get("step_id") != expected_step_id:
        raise ValueError("child question step_id differs from the active step")
    question = request.get("question")
    if not isinstance(question, str) or not question.strip():
        raise ValueError("child question text must be nonempty")
    options = request.get("options")
    if not isinstance(options, list) or len(options) > 5:
        raise ValueError("child question options must be a list of up to five choices")
    option_ids: list[str] = []
    for option in options:
        if isinstance(option, str):
            option_id = option
        elif isinstance(option, dict) and isinstance(option.get("description"), str) and option["description"].strip():
            option_id = option.get("id")
        else:
            raise ValueError("child question options need nonempty IDs and descriptions")
        if not isinstance(option_id, str) or not option_id.strip():
            raise ValueError("child question options need nonempty IDs and descriptions")
        option_ids.append(option_id)
    if len(set(option_ids)) != len(option_ids):
        raise ValueError("child question options must be distinct")
    flags = [request[key] for key in ("allow_custom_answer", "allow_custom", "custom_allowed") if key in request]
    if not flags or any(not isinstance(flag, bool) for flag in flags) or len(set(flags)) != 1:
        raise ValueError("child question custom-answer flag is missing or conflicting")
    if not options and not flags[0]:
        raise ValueError("child question needs options or a custom answer")
    return {
        "kind": "question", "step_id": expected_step_id, "question": question.strip(),
        "options": options, "allow_custom_answer": flags[0],
    }


def resolve_child_answer(request: dict[str, Any], answer: str, child_id: str, target_child_id: str) -> dict[str, str]:
    """Require an explicit answer addressed to the child that asked."""
    question = validate_child_question(request, request.get("step_id", "") if isinstance(request, dict) else "")
    if not child_id or target_child_id != child_id:
        raise ValueError("answer must continue the same child")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("an explicit human answer is required")
    chosen = answer.strip()
    options = question["options"]
    option_ids = [option if isinstance(option, str) else option["id"] for option in options]
    if chosen.isdigit() and 1 <= int(chosen) <= len(option_ids):
        chosen = option_ids[int(chosen) - 1]
    else:
        matching = [option for option in option_ids if option.casefold() == chosen.casefold()]
        if matching:
            chosen = matching[0]
        elif not question["allow_custom_answer"]:
            raise ValueError("human answer is not an allowed option")
    return {"step_id": question["step_id"], "child_id": child_id, "answer": chosen}


def validate_gate_choice(gate: dict[str, Any], answer: str) -> str:
    """Resolve one explicit human verdict against installed gate options."""
    if not isinstance(gate, dict) or gate.get("type") != "gate":
        raise ValueError("human verdict requires a gate step")
    options = gate.get("options")
    if not isinstance(options, list) or not options or any(not isinstance(option, str) or not option.strip() for option in options):
        raise ValueError("gate options must be nonempty strings")
    if len(set(options)) != len(options):
        raise ValueError("gate options must be distinct")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("an explicit human gate choice is required")
    choice = answer.strip()
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1]
    for option in options:
        if option.casefold() == choice.casefold():
            return option
    raise ValueError("human gate choice is not an allowed option")


def select_switch_branch(switch: dict[str, Any], choice: str) -> list[dict[str, Any]]:
    """Return only the branch selected by a validated gate result."""
    if not isinstance(switch, dict) or switch.get("type") != "switch":
        raise ValueError("branch selection requires a switch step")
    cases = switch.get("cases", {})
    if not isinstance(cases, dict) or not isinstance(choice, str):
        raise ValueError("switch cases or choice are invalid")
    branch = cases.get(choice, switch.get("default"))
    if not isinstance(branch, list):
        raise ValueError("switch has no branch for the selected choice")
    return branch


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect_parser = subparsers.add_parser("inspect", help="load an installed workflow without executing it")
    inspect_parser.add_argument("--project", type=Path, required=True)
    inspect_parser.add_argument("--workflow-id", required=True)
    inspect_parser.add_argument("--specify", type=Path, required=True)
    inspect_parser.add_argument("--expected-version", required=True)
    inspect_parser.add_argument("--skill-id", required=True)
    inspect_parser.add_argument("--input", action="append", default=[])
    question_parser = subparsers.add_parser("question", help="validate a structured child question from JSON on stdin")
    question_parser.add_argument("--step-id", required=True)
    answer_parser = subparsers.add_parser("answer", help="validate an answer and same-child relay from JSON on stdin")
    answer_parser.add_argument("--child-id", required=True)
    answer_parser.add_argument("--target-child-id", required=True)
    gate_parser = subparsers.add_parser("gate", help="validate an explicit gate verdict from JSON on stdin")
    branch_parser = subparsers.add_parser("branch", help="select only the chosen switch branch from JSON on stdin")
    args = parser.parse_args(argv)
    if args.command == "inspect":
        verify_controller_install(args.project, args.skill_id, args.workflow_id)
        output = subprocess.run([str(args.specify), "--version"], cwd=args.project, text=True, capture_output=True, check=True).stdout
        check_specify_version(output, args.expected_version)
        definition = load_installed_definition(args.project, args.workflow_id)
        validate_workflow_definition(definition)
        supplied_inputs = parse_key_values(args.input, argument_name="workflow input")
        definition["resolved_inputs"] = validate_required_inputs(definition, supplied_inputs)
        definition["agent_assignments"] = [item.to_dict() for item in collect_agent_assignments(definition["steps"])]
        definition["preflight_inputs_valid"] = True
        definition["installation_fingerprints"] = installation_fingerprints(args.project)
        print(json.dumps(definition, sort_keys=True))
        return 0
    payload = json.load(sys.stdin)
    if args.command == "question":
        result = validate_child_question(payload, args.step_id)
    elif args.command == "answer":
        result = resolve_child_answer(payload["request"], payload["answer"], args.child_id, args.target_child_id)
    elif args.command == "gate":
        result = {"choice": validate_gate_choice(payload["gate"], payload["answer"])}
    elif args.command == "branch":
        result = {"steps": select_switch_branch(payload["switch"], payload["choice"])}
    else:
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        print(f"FlowKit controller preflight failed: {error}", file=sys.stderr)
        raise SystemExit(1)

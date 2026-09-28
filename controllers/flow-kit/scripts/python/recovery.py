"""Atomic, transcript-free workflow recovery summaries for consumer projects."""

from __future__ import annotations

import json
import argparse
import os
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STEP_STATES = {"pending", "running", "waiting_for_human", "completed", "incomplete"}
STOP_BLOCKERS = {
    "child-unavailable", "command-unavailable", "human-input-missing",
    "human-relay-failed", "installation-changed", "main-task-interrupted",
    "operator-deferred", "preflight-failed", "step-failed",
    "unsupported-workflow", "unspecified-stop", "workflow-changed",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validate_summary(summary: dict[str, Any]) -> None:
    """Reject transcript-like fields and nonportable paths before persistence."""
    def visit(value: Any, key: str = "") -> None:
        if any(term in key.lower() for term in ("transcript", "secret", "token", "credential", "file_contents")):
            raise ValueError(f"recovery summary cannot contain {key or 'sensitive evidence'}")
        if isinstance(value, dict):
            for child_key, child in value.items():
                visit(child, str(child_key))
        elif isinstance(value, list):
            for child in value:
                visit(child, key)
        elif isinstance(value, str):
            if key == "blocker" and value not in STOP_BLOCKERS:
                raise ValueError("recovery blocker must be a supported non-sensitive code")
            if value.startswith("/") or ("/" + "Users/") in value or "\\Users\\" in value:
                raise ValueError("recovery paths must be repository-relative")
            if key in {"changed_files", "path"} and ".." in Path(value).parts:
                raise ValueError("recovery paths cannot escape the repository")
            if key.endswith("status") and value not in STEP_STATES and value not in {"stopped", "completed"}:
                raise ValueError(f"invalid recovery status: {value}")

    visit(summary)


def _atomic_write(path: Path, summary: dict[str, Any]) -> None:
    validate_summary(summary)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".summary-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(summary, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def create_summary(
    project_root: Path,
    workflow: dict[str, Any],
    fingerprints: dict[str, Any],
    assignments: list[dict[str, str]],
    *,
    preflight_passed: bool,
) -> dict[str, Any]:
    """Create a run record only after every preflight gate passed."""
    if not preflight_passed:
        raise ValueError("recovery summary requires successful preflight")
    run_id = str(uuid.uuid4())
    started = _now()
    summary = {
        "schema_version": "1.0",
        "run_id": run_id,
        "workflow_id": workflow["workflow"]["id"],
        "workflow_version": workflow["workflow"]["version"],
        "workflow_sha256": workflow["sha256"],
        "bundle_record": fingerprints.get("bundle_record"),
        "skill_record": fingerprints.get("skill_record"),
        "effective_assignments": assignments,
        "steps": {},
        "changed_files": [],
        "blocker": None,
        "started_at": started,
        "updated_at": started,
        "status": "running",
    }
    validate_summary(summary)
    path = Path(project_root) / ".specify/flow-controllers/runs" / run_id / "summary.json"
    _atomic_write(path, summary)
    return summary


def read_summary(path: Path) -> dict[str, Any]:
    """Read and validate one existing consumer-local summary."""
    summary = json.loads(Path(path).read_text(encoding="utf-8"))
    if summary.get("blocker") is not None and summary["blocker"] not in STOP_BLOCKERS:
        summary["blocker"] = "unspecified-stop"
    validate_summary(summary)
    return summary


def update_step(
    path: Path,
    step_id: str,
    status: str,
    *,
    changed_files: list[str] | None = None,
    blocker: str | None = None,
) -> dict[str, Any]:
    """Atomically record a step boundary and accumulated changed paths."""
    if status not in STEP_STATES:
        raise ValueError(f"invalid step status: {status}")
    if blocker is not None and blocker not in STOP_BLOCKERS:
        raise ValueError("recovery blocker must be a supported non-sensitive code")
    summary = read_summary(path)
    summary.setdefault("steps", {})[step_id] = {"status": status, "updated_at": _now()}
    if changed_files is not None:
        current = set(summary.get("changed_files", []))
        current.update(changed_files)
        summary["changed_files"] = sorted(current)
    if blocker is not None:
        summary["blocker"] = blocker
        summary["status"] = "stopped"
    summary["updated_at"] = _now()
    _atomic_write(Path(path), summary)
    return summary


def mark_interrupted_steps_incomplete(path: Path) -> dict[str, Any]:
    """Mark active work incomplete after an interrupted main-task session."""
    summary = read_summary(path)
    for step in summary.get("steps", {}).values():
        if step.get("status") in {"running", "waiting_for_human"}:
            step["status"] = "incomplete"
            step["updated_at"] = _now()
    summary["status"] = "incomplete"
    summary["updated_at"] = _now()
    _atomic_write(Path(path), summary)
    return summary


def installation_changed(initial: dict[str, Any], current: dict[str, Any]) -> bool:
    """Detect workflow edits and Specify or FlowKit install-record refreshes."""
    return any(initial.get(key) != current.get(key) for key in ("workflow_sha256", "bundle_record", "skill_record"))


def changed_paths(project_root: Path) -> list[str]:
    """Return Git's changed paths relative to the selected repository root."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "-z"],
        cwd=project_root, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        return []
    paths: set[str] = set()
    for item in result.stdout.split("\0"):
        if len(item) < 4:
            continue
        path = item[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            continue
        paths.add(candidate.as_posix())
    return sorted(paths)


def stop_run(path: Path, blocker: str, changed_files: list[str] | None = None) -> dict[str, Any]:
    """Record an operator-visible stop while preserving all project edits."""
    if blocker not in STOP_BLOCKERS:
        raise ValueError("recovery blocker must be a supported non-sensitive code")
    summary = read_summary(path)
    for step in summary.get("steps", {}).values():
        if step.get("status") in {"pending", "running", "waiting_for_human"}:
            step["status"] = "incomplete"
            step["updated_at"] = _now()
    if changed_files is not None:
        summary["changed_files"] = sorted(set(summary.get("changed_files", [])) | set(changed_files))
    summary["blocker"] = blocker
    summary["status"] = "stopped"
    summary["updated_at"] = _now()
    _atomic_write(Path(path), summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    """Expose safe summary updates to the main Codex task without a private runtime."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="create a run summary after successful preflight")
    create.add_argument("--project", type=Path, required=True)
    step = commands.add_parser("step", help="record a step boundary from JSON on stdin")
    step.add_argument("--summary", type=Path, required=True)
    step.add_argument("--step-id", required=True)
    step.add_argument("--status", choices=sorted(STEP_STATES), required=True)
    stop = commands.add_parser("stop", help="record a blocker and preserve changed paths")
    stop.add_argument("--summary", type=Path, required=True)
    stop.add_argument("--blocker", required=True)
    interrupt = commands.add_parser("interrupt", help="mark active steps incomplete after interruption")
    interrupt.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = json.load(sys.stdin) if args.command in {"create", "step", "stop"} else {}
    if args.command == "create":
        summary = create_summary(
            args.project,
            payload["workflow"],
            payload["fingerprints"],
            payload["assignments"],
            preflight_passed=payload.get("preflight_passed") is True,
        )
        result: dict[str, Any] = {"summary_path": str(args.project / ".specify/flow-controllers/runs" / summary["run_id"] / "summary.json"), "summary": summary}
    elif args.command == "step":
        result = update_step(args.summary, args.step_id, args.status, changed_files=payload.get("changed_files"), blocker=payload.get("blocker"))
    elif args.command == "stop":
        result = stop_run(args.summary, args.blocker, payload.get("changed_files"))
    else:
        result = mark_interrupted_steps_incomplete(args.summary)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"FlowKit recovery update failed: {error}", file=sys.stderr)
        raise SystemExit(1)

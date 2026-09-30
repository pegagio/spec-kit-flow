"""Build and serve the checked-in Spec Kit Flow catalog for bundle installation."""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import tomllib
import zipfile
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from posixpath import normpath


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "bundles/spec-kit-flow/bundle.yml"
CATALOG = ROOT / "catalog"
RELEASE = CATALOG / "release.json"
CONTROLLER_SOURCE = ROOT / "controllers/flow-kit"
CONTROLLER_PACKAGE_ID = "flow-kit-controllers"
EXTENSION_SOURCES = {
    "flow-roadmap": "roadmap",
    "flow-wiki": "wiki",
    "flow-feedback": "feedback",
}
CONTROLLER_BINDINGS = (
    ("flow-kit-select-feature", "FlowKit Select Feature", "speckit-flow-select-feature"),
    ("flow-kit-specify", "FlowKit Specify", "speckit-flow-specify"),
    ("flow-kit-clarify", "FlowKit Clarify", "speckit-flow-clarify"),
    ("flow-kit-plan", "FlowKit Plan", "speckit-flow-plan"),
    ("flow-kit-tasks", "FlowKit Tasks", "speckit-flow-tasks"),
    ("flow-kit-analyze-remediate", "FlowKit Analyze", "speckit-flow-analyze-remediate"),
    ("flow-kit-implement", "FlowKit Implement", "speckit-flow-implement"),
    ("flow-kit-converge", "FlowKit Converge", "speckit-flow-converge"),
    ("flow-kit-closeout", "FlowKit Close Out", "speckit-flow-closeout"),
    ("flow-kit-wiki-lint-update", "FlowKit Wiki Lint Update", "speckit-flow-wiki-lint-update"),
)


def fail(message: str) -> None:
    raise ValueError(message)


def selected_specify(cwd: Path) -> str | None:
    """Use the project's mise-selected Specify before considering PATH."""
    mise = shutil.which("mise")
    if mise:
        result = subprocess.run([mise, "which", "specify"], cwd=cwd, text=True, capture_output=True, check=False)
        if result.returncode == 0 and result.stdout.strip():
            selected = result.stdout.strip()
            if not Path(selected).is_file() or not os.access(selected, os.X_OK):
                fail("mise-selected Specify executable is missing or not executable")
            return selected
    return shutil.which("specify")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field(text: str, name: str, indent: int = 2) -> str:
    match = re.search(rf"^{' ' * indent}{re.escape(name)}:\s*([^\n]+)", text, re.MULTILINE)
    if match is None:
        fail(f"missing {name}")
    return match.group(1).strip().strip('"\'')


def bundle_components() -> tuple[str, dict[str, dict[str, str]]]:
    """Read the fixed, simple component lists in this repository's bundle manifest."""
    lines = BUNDLE.read_text(encoding="utf-8").splitlines()
    version = field("\n".join(lines), "version", 2)
    components: dict[str, dict[str, str]] = {"extensions": {}, "workflows": {}}
    kind: str | None = None
    component_id: str | None = None
    in_provides = False
    for line in lines:
        if line == "provides:":
            in_provides = True
        elif line and not line.startswith(" "):
            in_provides = False
            kind = None
        elif in_provides and (match := re.fullmatch(r"  ([a-z_]+):", line)):
            if match.group(1) not in components:
                fail(f"unsupported bundle component kind: {match.group(1)}")
        if line == "  extensions:":
            kind = "extensions"
        elif line == "  workflows:":
            kind = "workflows"
        elif kind and (match := re.fullmatch(r'    - id: "?([^" ]+)"?', line)):
            component_id = match.group(1)
        elif kind and component_id and (match := re.fullmatch(r'      version: "?([^" ]+)"?', line)):
            components[kind][component_id] = match.group(1)
            component_id = None
    if set(components["extensions"]) != set(EXTENSION_SOURCES) or not components["workflows"]:
        fail("bundle component list is incomplete or has changed; review the catalog builder")
    return version, components


def source_commit(source: Path, tracked_path: str = ".") -> str:
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", tracked_path], cwd=source,
        text=True, capture_output=True, check=True,
    )
    if status.stdout.strip():
        fail(f"source has uncommitted changes in {tracked_path}: {source}")
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=source,
        text=True, capture_output=True, check=True,
    ).stdout.strip()


def require_local_release_sources_clean(root: Path) -> None:
    """Require committed bundle and workflow definitions for a released catalog."""
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "bundles/spec-kit-flow/bundle.yml", "workflows"],
        cwd=root, text=True, capture_output=True, check=True,
    ).stdout.strip()
    if status:
        fail("bundle or workflow source has uncommitted changes; release builds require clean source")


def release_tag(source: Path, version: str, commit: str) -> str:
    tag = f"v{version}"
    tag_type = subprocess.run(
        ["git", "cat-file", "-t", f"refs/tags/{tag}"], cwd=source,
        text=True, capture_output=True, check=False,
    )
    if tag_type.returncode or tag_type.stdout.strip() != "tag":
        fail(f"{source} needs an annotated {tag} release tag")
    resolved = subprocess.run(
        ["git", "rev-parse", f"refs/tags/{tag}^{{commit}}"], cwd=source,
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    if resolved != commit:
        fail(f"{source} HEAD differs from release tag {tag}")
    return tag


def extension_metadata(source: Path) -> dict[str, str]:
    manifest = (source / "extension.yml").read_text(encoding="utf-8")
    if "extension:\n" not in manifest:
        fail(f"extension manifest has no extension section: {source}")
    section = manifest.split("extension:\n", 1)[1].split("\nrequires:", 1)[0]
    return {name: field(section, name) for name in ("id", "name", "version", "author")}


def runtime_files(source: Path) -> list[Path]:
    files = [source / name for name in ("extension.yml", "config-template.yml", "LICENSE") if (source / name).is_file()]
    for dirname in ("commands", "scripts", "templates"):
        directory = source / dirname
        if directory.is_dir():
            files.extend(path for path in directory.rglob("*") if path.is_file() and not path.is_symlink() and "__pycache__" not in path.parts)
    return sorted(files, key=lambda path: str(path.relative_to(source)))


def controller_manifest() -> dict[str, object]:
    """Read the deliberately small, reviewed controller package manifest."""
    text = (CONTROLLER_SOURCE / "manifest.yml").read_text(encoding="utf-8")
    package_section = text.split("package:\n", 1)[1].split("\nrequires:", 1)[0]
    require_section = text.split("requires:\n", 1)[1].split("\ncontrollers:", 1)[0]
    package_id = field(package_section, "id")
    version = field(package_section, "version")
    specify_version = field(require_section, "specify_cli_version")
    controllers: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if line.startswith("  - skill_id:"):
            if current is not None:
                controllers.append(current)
            current = {"skill_id": line.split(":", 1)[1].strip().strip("\"'")}
        elif current is not None and line.startswith("    ") and ":" in line:
            key, value = line.strip().split(":", 1)
            current[key] = value.strip().strip("\"'")
    if current is not None:
        controllers.append(current)
    if package_id != CONTROLLER_PACKAGE_ID or not version or not specify_version:
        fail("controller package manifest identity or version is invalid")
    actual = [(item.get("skill_id"), item.get("display_name"), item.get("workflow_id")) for item in controllers]
    if actual != list(CONTROLLER_BINDINGS):
        fail("controller manifest must declare the reviewed controller inventory in order")
    if len({item["skill_id"] for item in controllers}) != len(CONTROLLER_BINDINGS) or len({item["workflow_id"] for item in controllers}) != len(CONTROLLER_BINDINGS):
        fail("controller skill and workflow bindings must be unique")
    return {
        "package_id": package_id,
        "version": version,
        "specify_cli_version": specify_version,
        "controllers": controllers,
    }


def controller_package_files() -> dict[str, Path]:
    """Map reviewed source files to their consumer installation paths."""
    manifest = controller_manifest()
    files: dict[str, Path] = {}
    shared = [CONTROLLER_SOURCE / "manifest.yml", CONTROLLER_SOURCE / "controller-protocol.md"]
    scripts = CONTROLLER_SOURCE / "scripts"
    shared.extend(
        path for path in scripts.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    for source in shared:
        if source.is_symlink():
            fail(f"controller package cannot contain symlinks: {source.name}")
        relative = source.relative_to(CONTROLLER_SOURCE)
        files[(Path(".specify/flow-kit") / relative).as_posix()] = source
    declared_ids = {item["skill_id"] for item in manifest["controllers"]}
    skill_root = CONTROLLER_SOURCE / "skills"
    observed_ids = {path.name for path in skill_root.iterdir() if path.is_dir()}
    if observed_ids != declared_ids:
        fail("controller skill directories differ from the reviewed manifest inventory")
    for item in manifest["controllers"]:
        skill_id = item["skill_id"]
        skill_dir = skill_root / skill_id
        skill_file = skill_dir / "SKILL.md"
        metadata_file = skill_dir / "agents/openai.yaml"
        if not skill_file.is_file() or not metadata_file.is_file():
            fail(f"controller skill is incomplete: {skill_id}")
        skill_text = skill_file.read_text(encoding="utf-8")
        display_text = metadata_file.read_text(encoding="utf-8")
        name_match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", skill_text, re.MULTILINE)
        display_match = re.search(r'^  display_name:\s*[\"\']([^\"\']+)', display_text, re.MULTILINE)
        if name_match is None or name_match.group(1).strip() != skill_id:
            fail(f"Codex skill name differs from manifest: {skill_id}")
        if display_match is None or display_match.group(1) != item["display_name"]:
            fail(f"Codex display name differs from manifest: {skill_id}")
        for source in sorted(skill_dir.rglob("*")):
            if source.is_file():
                if source.is_symlink():
                    fail(f"controller package cannot contain symlinks: {source.name}")
                relative = source.relative_to(skill_root)
                files[(Path(".agents/skills") / relative).as_posix()] = source
    return dict(sorted(files.items()))


def package_controller(destination: Path) -> dict[str, object]:
    """Build a deterministic direct Codex skill package without host paths."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    files = controller_package_files()
    home = str(Path.home()).encode()
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, source in files.items():
            data = source.read_bytes()
            if (home and home in data) or (b"/" + b"Users/") in data:
                fail(f"host-specific path in controller package file: {name}")
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    manifest = controller_manifest()
    return {
        "package_id": manifest["package_id"],
        "version": manifest["version"],
        "artifact": destination.name,
        "sha256": digest(destination),
        "files": sorted(files),
        "controllers": manifest["controllers"],
    }


def _safe_package_members(archive_path: Path) -> dict[str, bytes]:
    """Validate the package archive before any consumer path is written."""
    members: dict[str, bytes] = {}
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            name = member.filename
            path = Path(name)
            if path.is_absolute() or ".." in path.parts or name.startswith(("/", "\\")):
                fail("controller package contains an unsafe path")
            if member.is_dir():
                continue
            if not (name.startswith(".specify/flow-kit/") or re.match(r"^\.agents/skills/flow-kit-[^/]+/", name)):
                fail(f"controller package contains an unexpected path: {name}")
            members[name] = archive.read(member)
    if not members or ".specify/flow-kit/manifest.yml" not in members:
        fail("controller package is missing its manifest")
    return members


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _read_ownership_record(record_path: Path) -> dict[str, object]:
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"FlowKit skill ownership record is unreadable: {error}")
    if record.get("package") != CONTROLLER_PACKAGE_ID or not isinstance(record.get("files"), dict):
        fail("FlowKit skill ownership record is malformed")
    if record.get("status") != "installed":
        fail(f"FlowKit skill package is in incomplete state: {record.get('status')}")
    return record


def _owned_target(project: Path, relative: str) -> Path:
    """Confine recorded package files to the direct FlowKit package inventory."""
    if not isinstance(relative, str) or not relative or "\\" in relative:
        fail("invalid FlowKit ownership path")
    path = Path(relative)
    parts = path.parts
    if path.is_absolute() or path.as_posix() != relative or ".." in parts:
        fail(f"invalid FlowKit ownership path: {relative}")
    skills = {skill_id for skill_id, _, _ in CONTROLLER_BINDINGS} | {"flow-kit-start-feature"}
    skill_path = (
        len(parts) >= 4 and parts[:2] == (".agents", "skills")
        and parts[2] in skills and parts[3:] in {("SKILL.md",), ("agents", "openai.yaml")}
    )
    helper_path = (
        parts[:2] == (".specify", "flow-kit")
        and (parts[2:] in {("manifest.yml",), ("controller-protocol.md",)} or
             (len(parts) >= 4 and parts[2] == "scripts"))
    )
    if not (skill_path or helper_path):
        fail(f"invalid FlowKit ownership path: {relative}")
    target = project / path
    cursor = project
    for part in parts:
        cursor /= part
        if cursor.is_symlink():
            fail(f"FlowKit ownership path crosses a symlink: {relative}")
    if not target.resolve(strict=False).is_relative_to(project.resolve()):
        fail(f"FlowKit ownership path escapes consumer project: {relative}")
    return target


def install_controller_package(
    project: Path,
    archive_path: Path,
    *,
    refresh: bool,
    source_digest: str,
    catalog_status: str,
    preflight_only: bool = False,
) -> None:
    """Install or refresh the direct skill package with digest-based ownership."""
    project = Path(project).resolve()
    members = _safe_package_members(Path(archive_path))
    manifest_text = members[".specify/flow-kit/manifest.yml"].decode("utf-8")
    package_version = field(manifest_text.split("package:\n", 1)[1].split("\nrequires:", 1)[0], "version")
    record_path = project / ".specify/flow-kit/skills-install.json"
    record_exists = record_path.is_file()
    old_record: dict[str, object] | None = None
    old_record_bytes: bytes | None = None
    old_files: dict[str, bytes | None] = {}
    if refresh and record_exists:
        old_record_bytes = record_path.read_bytes()
        old_record = _read_ownership_record(record_path)
        old_owned = old_record["files"]
    else:
        if record_exists:
            fail("FlowKit skills are already installed; use refresh")
        old_owned = {}
    for relative, content in members.items():
        target = _owned_target(project, relative)
        owned_before = isinstance(old_owned, dict) and relative in old_owned
        if owned_before:
            expected = old_owned[relative]
            if not target.is_file() or digest(target) != expected:
                fail(f"locally changed FlowKit-owned file blocks replacement: {relative}")
            old_files[relative] = target.read_bytes()
        elif target.exists():
            fail(f"consumer-owned path conflicts with FlowKit skills: {relative}")
        else:
            old_files[relative] = None
    if refresh and isinstance(old_owned, dict):
        for relative, expected in old_owned.items():
            target = _owned_target(project, relative)
            if relative not in members:
                if not target.is_file() or digest(target) != expected:
                    fail(f"locally changed obsolete FlowKit-owned file blocks refresh: {relative}")
                old_files[relative] = target.read_bytes()
    manifest = json.loads(json.dumps(controller_manifest())) if CONTROLLER_SOURCE.is_dir() else {}
    current_bindings = manifest.get("controllers", [])
    files_record = {relative: _sha256_bytes(content) for relative, content in members.items()}
    provisional = {
        "schema_version": "1.0",
        "package": CONTROLLER_PACKAGE_ID,
        "version": package_version,
        "source_sha256": source_digest,
        "catalog_status": catalog_status,
        "controllers": current_bindings,
        "files": files_record,
        "status": "refreshing" if old_record is not None else "installing",
    }
    if preflight_only:
        return
    _atomic_bytes(record_path, (json.dumps(provisional, indent=2, sort_keys=True) + "\n").encode())
    try:
        for relative, content in members.items():
            _atomic_bytes(_owned_target(project, relative), content)
        observed = {relative: digest(_owned_target(project, relative)) for relative in members}
        if observed != files_record:
            fail("installed FlowKit skill inventory differs from the package")
        if refresh and isinstance(old_owned, dict):
            for relative in old_owned:
                if relative not in members:
                    _owned_target(project, relative).unlink()
        provisional["status"] = "installed"
        _atomic_bytes(record_path, (json.dumps(provisional, indent=2, sort_keys=True) + "\n").encode())
    except Exception:
        for relative, content in old_files.items():
            target = _owned_target(project, relative)
            if content is None:
                try:
                    target.unlink()
                except FileNotFoundError:
                    pass
            else:
                _atomic_bytes(target, content)
        if old_record_bytes is None:
            record_path.unlink(missing_ok=True)
        else:
            _atomic_bytes(record_path, old_record_bytes)
        raise


def remove_controller_package(project: Path, *, preflight_only: bool = False) -> None:
    """Remove only unchanged files recorded as FlowKit-owned."""
    project = Path(project).resolve()
    record_path = project / ".specify/flow-kit/skills-install.json"
    if not record_path.is_file():
        fail("FlowKit skill ownership record is missing")
    record = _read_ownership_record(record_path)
    owned = record["files"]
    assert isinstance(owned, dict)
    for relative, expected in owned.items():
        target = _owned_target(project, relative)
        if not target.is_file() or digest(target) != expected:
            fail(f"locally changed FlowKit-owned file blocks removal: {relative}")
    if preflight_only:
        return
    record["status"] = "removing"
    _atomic_bytes(record_path, (json.dumps(record, indent=2, sort_keys=True) + "\n").encode())
    for relative in sorted(owned, key=lambda item: item.count("/"), reverse=True):
        _owned_target(project, relative).unlink()
    remaining = [relative for relative in owned if _owned_target(project, relative).exists()]
    if remaining:
        fail(f"FlowKit skill removal incomplete: {', '.join(remaining)}")
    record_path.unlink()
    for relative in owned:
        parent = _owned_target(project, relative).parent
        while parent != project and parent.name not in {"runs", "flow-controllers", ".specify", ".agents", "skills"}:
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def remove(project: Path) -> None:
    """Remove the Specify bundle and unchanged FlowKit-owned Codex skills."""
    project = Path(project).resolve()
    if not project.is_dir() or ROOT in project.parents:
        fail("removal target must be an existing consumer outside the source checkout")
    if not (project / ".specify").is_dir():
        fail("removal target is not an initialized Specify consumer")
    record = project / ".specify/flow-kit/skills-install.json"
    if not record.is_file():
        fail("FlowKit skill ownership record is missing")
    remove_controller_package(project, preflight_only=True)
    expected_specify = tomllib.loads((ROOT / "mise.toml").read_text(encoding="utf-8"))["tools"]["pipx:specify-cli"]
    specify = selected_specify(project)
    if specify is None:
        fail("specify is unavailable; run mise trust and mise install in this checkout")
    version = subprocess.run([specify, "--version"], cwd=project, text=True, capture_output=True, check=True).stdout.strip()
    if version != f"specify {expected_specify}":
        fail(f"expected Specify {expected_specify}, found {version}")
    subprocess.run([specify, "bundle", "remove", "spec-kit-flow"], cwd=project, check=True)
    remove_controller_package(project)


def package_extension(source: Path, destination: Path, extension_id: str) -> None:
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in runtime_files(source):
            data = path.read_bytes()
            if str(Path.home()).encode() in data:
                fail(f"host-specific home path in {extension_id}/{path.relative_to(source)}")
            info = zipfile.ZipInfo(str(Path(extension_id) / path.relative_to(source)), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)


def build(roadmap: Path, wiki: Path, snapshot: bool = False) -> None:
    if not snapshot:
        require_local_release_sources_clean(ROOT)
    bundle_version, components = bundle_components()
    sources = {
        "flow-roadmap": roadmap.resolve(),
        "flow-wiki": wiki.resolve(),
        "flow-feedback": ROOT / "extensions/flow-feedback",
    }
    release: dict[str, object] = {
        "schema_version": "1.0", "bundle_version": bundle_version,
        "status": "snapshot" if snapshot else "released",
        "extensions": {}, "workflows": {},
    }
    with tempfile.TemporaryDirectory(prefix="spec-kit-flow-build-") as temporary:
        packages = Path(temporary)
        for extension_id, source in sources.items():
            metadata = extension_metadata(source)
            expected = components["extensions"][extension_id]
            if metadata["id"] != extension_id or metadata["version"] != expected:
                fail(f"{source} must declare {extension_id} version {expected}")
            tracked_path = "extensions/flow-feedback" if extension_id == "flow-feedback" else "."
            commit = source_commit(ROOT if extension_id == "flow-feedback" else source, tracked_path)
            tag = None if extension_id == "flow-feedback" or snapshot else release_tag(source, expected, commit)
            artifact = f"{extension_id}-{expected}.zip"
            package_extension(source, packages / artifact, extension_id)
            release["extensions"][extension_id] = {
                "version": expected, "name": metadata["name"], "author": metadata["author"],
                "source_repository": "https://github.com/pegagio/spec-kit-flow" if extension_id == "flow-feedback" else f"https://github.com/pegagio/spec-kit-flow-{EXTENSION_SOURCES[extension_id]}",
                "source_commit": commit, "source_tag": tag,
                "artifact": artifact, "sha256": digest(packages / artifact),
            }
        for workflow_id, version in components["workflows"].items():
            path = ROOT / "workflows" / workflow_id / "workflow.yml"
            source = path.read_text(encoding="utf-8")
            if field(source.split("workflow:\n", 1)[1], "id") != workflow_id or field(source.split("workflow:\n", 1)[1], "version") != version:
                fail(f"workflow source does not match bundle pin: {workflow_id} {version}")
            release["workflows"][workflow_id] = {"version": version, "sha256": digest(path)}
        controller_archive = packages / f"{CONTROLLER_PACKAGE_ID}-{controller_manifest()['version']}.zip"
        controller = package_controller(controller_archive)
        status = subprocess.run(
            ["git", "status", "--porcelain", "--", "controllers/flow-kit"],
            cwd=ROOT, text=True, capture_output=True, check=True,
        ).stdout.strip()
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
        if not snapshot and status:
            fail("controller source has uncommitted changes; release builds require clean source")
        release["controller_package"] = {
            "id": controller["package_id"], "version": controller["version"],
            "artifact": controller["artifact"], "sha256": controller["sha256"],
            "source_commit": commit, "source_dirty": bool(status),
            "source_sha256": controller["sha256"], "controllers": controller["controllers"],
        }
        if RELEASE.exists():
            previous = json.loads(RELEASE.read_text(encoding="utf-8"))
            if not snapshot and previous.get("status") == "released" and previous["bundle_version"] == bundle_version and previous != release:
                fail("catalog content changed without a bundle version change")
        (CATALOG / "packages").mkdir(parents=True, exist_ok=True)
        for artifact in packages.iterdir():
            shutil.copy2(artifact, CATALOG / "packages" / artifact.name)
        RELEASE.write_text(json.dumps(release, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Built catalog for spec-kit-flow {bundle_version} with {len(sources)} extensions and {len(components['workflows'])} workflows")


def verified_release(catalog_dir: Path | None = None, release_path: Path | None = None) -> dict[str, object]:
    catalog_dir = catalog_dir or CATALOG
    release_path = release_path or (catalog_dir / "release.json")
    release = json.loads(release_path.read_text(encoding="utf-8"))
    bundle_version, components = bundle_components()
    if release.get("status") not in ("snapshot", "released"):
        fail("catalog status must be snapshot or released")
    if release["bundle_version"] != bundle_version:
        fail("catalog bundle version differs from bundle.yml")
    if set(release["extensions"]) != set(components["extensions"]) or set(release["workflows"]) != set(components["workflows"]):
        fail("catalog components differ from bundle.yml")
    for extension_id, version in components["extensions"].items():
        entry = release["extensions"][extension_id]
        artifact = catalog_dir / "packages" / entry["artifact"]
        if entry["version"] != version or not artifact.is_file() or digest(artifact) != entry["sha256"]:
            fail(f"catalog artifact is missing or mismatched: {extension_id}")
        if release["status"] == "released" and extension_id in ("flow-roadmap", "flow-wiki") and entry.get("source_tag") != f"v{version}":
            fail(f"catalog source tag differs from bundle pin: {extension_id}")
        with zipfile.ZipFile(artifact) as archive:
            manifest_name = f"{extension_id}/extension.yml"
            if manifest_name not in archive.namelist():
                fail(f"catalog archive has no extension manifest: {extension_id}")
            manifest = archive.read(manifest_name).decode("utf-8")
            section = manifest.split("extension:\n", 1)[1].split("\nrequires:", 1)[0]
            if field(section, "id") != extension_id or field(section, "version") != version:
                fail(f"catalog archive manifest differs from bundle pin: {extension_id}")
    for workflow_id, version in components["workflows"].items():
        entry = release["workflows"][workflow_id]
        path = ROOT / "workflows" / workflow_id / "workflow.yml"
        if entry["version"] != version or digest(path) != entry["sha256"]:
            fail(f"workflow source differs from catalog release: {workflow_id}")
    controller = release.get("controller_package")
    if not isinstance(controller, dict) or controller.get("id") != CONTROLLER_PACKAGE_ID:
        fail("catalog has no FlowKit controller package record")
    current_manifest = controller_manifest()
    if controller.get("version") != current_manifest["version"]:
        fail("catalog controller package version differs from the reviewed manifest")
    package_path = catalog_dir / "packages" / str(controller.get("artifact", ""))
    if not package_path.is_file() or digest(package_path) != controller.get("sha256"):
        fail("catalog controller package is missing or has a checksum mismatch")
    members = _safe_package_members(package_path)
    packaged_manifest = members[".specify/flow-kit/manifest.yml"].decode("utf-8")
    packaged_bindings = re.findall(
        r'^  - skill_id: "([^"]+)"\n    display_name: "([^"]+)"\n    workflow_id: "([^"]+)"',
        packaged_manifest, re.MULTILINE,
    )
    if packaged_bindings != list(CONTROLLER_BINDINGS) or controller.get("controllers") != current_manifest["controllers"]:
        fail("catalog controller inventory differs from the reviewed package manifest")
    if release["status"] == "released" and controller.get("source_dirty"):
        fail("released controller package cannot have dirty source provenance")
    return release


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_: object) -> None:
        pass


def build_development_snapshot(destination: Path) -> dict[str, object]:
    """Compose a disposable snapshot catalog without changing checked-in release files."""
    destination = Path(destination)
    package_dir = destination / "packages"
    package_dir.mkdir(parents=True, exist_ok=True)
    previous = json.loads(RELEASE.read_text(encoding="utf-8"))
    extensions: dict[str, object] = {}
    for extension_id, entry in previous["extensions"].items():
        artifact = CATALOG / "packages" / entry["artifact"]
        if not artifact.is_file() or digest(artifact) != entry["sha256"]:
            fail(f"released extension package is missing or mismatched: {extension_id}")
        shutil.copy2(artifact, package_dir / artifact.name)
        extensions[extension_id] = entry
    bundle_version, components = bundle_components()
    workflows = {}
    for workflow_id, version in components["workflows"].items():
        source = ROOT / "workflows" / workflow_id / "workflow.yml"
        metadata = source.read_text(encoding="utf-8").split("workflow:\n", 1)[1]
        if field(metadata, "id") != workflow_id or field(metadata, "version") != version:
            fail(f"workflow source does not match bundle pin: {workflow_id}")
        workflows[workflow_id] = {"version": version, "sha256": digest(source)}
    controller_path = package_dir / f"{CONTROLLER_PACKAGE_ID}-{controller_manifest()['version']}.zip"
    controller = package_controller(controller_path)
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "controllers/flow-kit"],
        cwd=ROOT, text=True, capture_output=True, check=True,
    ).stdout.strip()
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    release: dict[str, object] = {
        "schema_version": "1.0",
        "bundle_version": bundle_version,
        "status": "snapshot",
        "extensions": extensions,
        "workflows": workflows,
        "controller_package": {
            "id": controller["package_id"], "version": controller["version"],
            "artifact": controller["artifact"], "sha256": controller["sha256"],
            "source_commit": commit, "source_dirty": bool(status),
            "source_sha256": controller["sha256"], "controllers": controller["controllers"],
        },
    }
    release_file = destination / "release.json"
    release_file.write_text(json.dumps(release, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    verified_release(destination, release_file)
    return release


def install(project: Path, refresh: bool, development_snapshot: bool = False) -> None:
    project = project.resolve()
    if not project.is_dir():
        fail(f"consumer project directory does not exist: {project}")
    if ROOT in project.parents:
        fail("consumer project must not be nested inside the Spec Kit Flow source checkout")
    snapshot_directory: tempfile.TemporaryDirectory[str] | None = None
    catalog_dir = CATALOG
    release_path = RELEASE
    if development_snapshot:
        temporary_root = Path(tempfile.gettempdir()).resolve()
        if temporary_root not in project.parents:
            fail("development snapshots may only be installed into a disposable consumer under the system temporary directory")
        if not (project / ".specify").is_dir():
            fail("development snapshot target must already be initialized as a Specify consumer")
        snapshot_directory = tempfile.TemporaryDirectory(prefix="flowkit-snapshot-catalog-")
        catalog_dir = Path(snapshot_directory.name)
        try:
            release = build_development_snapshot(catalog_dir)
        except Exception:
            snapshot_directory.cleanup()
            raise
        release_path = catalog_dir / "release.json"
    else:
        release = verified_release(catalog_dir, release_path)
        if release["status"] != "released":
            fail("catalog is a development snapshot; use --development-snapshot only with a disposable initialized consumer")
    expected_specify = tomllib.loads((ROOT / "mise.toml").read_text(encoding="utf-8"))["tools"]["pipx:specify-cli"]
    specify = selected_specify(project)
    if specify is None:
        fail("specify is unavailable; run mise trust and mise install in this checkout")
    version = subprocess.run([specify, "--version"], text=True, capture_output=True, check=True).stdout.strip()
    if version != f"specify {expected_specify}":
        fail(f"expected specify {expected_specify}, found {version}")
    controller_record = release["controller_package"]
    controller_archive = catalog_dir / "packages" / controller_record["artifact"]
    install_controller_package(
        project, controller_archive, refresh=refresh,
        source_digest=controller_record["source_sha256"], catalog_status=release["status"],
        preflight_only=True,
    )
    with tempfile.TemporaryDirectory(prefix="spec-kit-flow-catalog-") as temporary:
        directory = Path(temporary)
        assets = directory / "assets"
        assets.mkdir()
        for entry in release["extensions"].values():
            shutil.copy2(catalog_dir / "packages" / entry["artifact"], assets / entry["artifact"])
        workflows = assets / "workflows"
        workflows.mkdir()
        for workflow_id in release["workflows"]:
            shutil.copy2(ROOT / "workflows" / workflow_id / "workflow.yml", workflows / f"{workflow_id}.yml")
        handler = functools.partial(QuietHandler, directory=str(directory))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}"
            extensions = {
                extension_id: {
                    "name": entry["name"], "version": entry["version"],
                    "description": "Spec Kit Flow release component", "author": entry["author"],
                    "download_url": f"{base}/assets/{entry['artifact']}", "sha256": entry["sha256"],
                }
                for extension_id, entry in release["extensions"].items()
            }
            workflow_entries = {
                workflow_id: {
                    "id": workflow_id, "name": workflow_id, "version": entry["version"],
                    "description": "Spec Kit Flow workflow", "author": "pegagio",
                    "url": f"{base}/assets/workflows/{workflow_id}.yml", "tags": ["spec-kit-flow"],
                }
                for workflow_id, entry in release["workflows"].items()
            }
            (directory / "extensions.json").write_text(json.dumps({"schema_version": "1.0", "extensions": extensions}), encoding="utf-8")
            (directory / "workflows.json").write_text(json.dumps({"schema_version": "1.0", "workflows": workflow_entries}), encoding="utf-8")
            environment = os.environ.copy()
            environment["SPECKIT_CATALOG_URL"] = f"{base}/extensions.json"
            environment["SPECKIT_WORKFLOW_CATALOG_URL"] = f"{base}/workflows.json"
            command = [specify, "bundle", "install", str(BUNDLE)]
            if refresh:
                command.append("--refresh")
            action = "Refreshing" if refresh else "Installing"
            print(f"{action} spec-kit-flow {release['bundle_version']} in {project}", flush=True)
            subprocess.run(command, cwd=project, env=environment, check=True)
            install_controller_package(
                project, controller_archive, refresh=refresh,
                source_digest=controller_record["source_sha256"], catalog_status=release["status"],
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
            if snapshot_directory is not None:
                snapshot_directory.cleanup()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    builder = commands.add_parser("build", help="Build versioned catalog packages")
    builder.add_argument("roadmap", type=Path)
    builder.add_argument("wiki", type=Path)
    builder.add_argument("--snapshot", action="store_true", help="Build development packages that cannot be installed through catalog tasks")
    for name in ("install", "refresh"):
        consumer = commands.add_parser(name, help=f"{name} the bundle in a consumer project")
        consumer.add_argument("project", type=Path)
        consumer.add_argument("--development-snapshot", action="store_true", help="build and use an unreleased snapshot only in a disposable initialized consumer")
    remover = commands.add_parser("remove", help="remove the bundle and unchanged FlowKit-owned controllers")
    remover.add_argument("project", type=Path)
    arguments = parser.parse_args()
    try:
        if arguments.command == "build":
            build(arguments.roadmap, arguments.wiki, arguments.snapshot)
        elif arguments.command == "remove":
            remove(arguments.project)
        else:
            install(arguments.project, arguments.command == "refresh", arguments.development_snapshot)
    except (ValueError, OSError, subprocess.CalledProcessError, KeyError, zipfile.BadZipFile) as error:
        print(f"catalog: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

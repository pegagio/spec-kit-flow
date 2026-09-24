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
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "bundles/spec-kit-flow/bundle.yml"
CATALOG = ROOT / "catalog"
RELEASE = CATALOG / "release.json"
EXTENSION_SOURCES = {
    "flow-roadmap": "roadmap",
    "flow-wiki": "wiki",
    "flow-feedback": "feedback",
}


def fail(message: str) -> None:
    raise ValueError(message)


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
        if RELEASE.exists():
            previous = json.loads(RELEASE.read_text(encoding="utf-8"))
            if previous.get("status") == "released" and previous["bundle_version"] == bundle_version and previous != release:
                fail("catalog content changed without a bundle version change")
        (CATALOG / "packages").mkdir(parents=True, exist_ok=True)
        for artifact in packages.iterdir():
            shutil.copy2(artifact, CATALOG / "packages" / artifact.name)
        RELEASE.write_text(json.dumps(release, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Built catalog for spec-kit-flow {bundle_version} with {len(sources)} extensions and {len(components['workflows'])} workflows")


def verified_release() -> dict[str, object]:
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    bundle_version, components = bundle_components()
    if release.get("status") not in ("snapshot", "released"):
        fail("catalog status must be snapshot or released")
    if release["bundle_version"] != bundle_version:
        fail("catalog bundle version differs from bundle.yml")
    if set(release["extensions"]) != set(components["extensions"]) or set(release["workflows"]) != set(components["workflows"]):
        fail("catalog components differ from bundle.yml")
    for extension_id, version in components["extensions"].items():
        entry = release["extensions"][extension_id]
        artifact = CATALOG / "packages" / entry["artifact"]
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
    return release


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_: object) -> None:
        pass


def install(project: Path, refresh: bool) -> None:
    project = project.resolve()
    if not project.is_dir():
        fail(f"consumer project directory does not exist: {project}")
    if ROOT in project.parents:
        fail("consumer project must not be nested inside the Spec Kit Flow source checkout")
    release = verified_release()
    if release["status"] != "released":
        fail("catalog is a development snapshot; install and refresh require tagged extension releases")
    expected_specify = tomllib.loads((ROOT / "mise.toml").read_text(encoding="utf-8"))["tools"]["pipx:specify-cli"]
    specify = shutil.which("specify")
    if specify is None and shutil.which("mise"):
        resolved = subprocess.run(["mise", "which", "specify"], text=True, capture_output=True, check=False)
        if resolved.returncode == 0:
            specify = resolved.stdout.strip()
    if specify is None:
        fail("specify is unavailable; run mise trust and mise install in this checkout")
    version = subprocess.run([specify, "--version"], text=True, capture_output=True, check=True).stdout.strip()
    if version != f"specify {expected_specify}":
        fail(f"expected specify {expected_specify}, found {version}")
    with tempfile.TemporaryDirectory(prefix="spec-kit-flow-catalog-") as temporary:
        directory = Path(temporary)
        assets = directory / "assets"
        assets.mkdir()
        for entry in release["extensions"].values():
            shutil.copy2(CATALOG / "packages" / entry["artifact"], assets / entry["artifact"])
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
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


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
    arguments = parser.parse_args()
    try:
        if arguments.command == "build":
            build(arguments.roadmap, arguments.wiki, arguments.snapshot)
        else:
            install(arguments.project, arguments.command == "refresh")
    except (ValueError, OSError, subprocess.CalledProcessError, KeyError, zipfile.BadZipFile) as error:
        print(f"catalog: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Validate the development bundle snapshot with pinned component artifacts.

The test uses the exact roadmap and wiki packages recorded in this repository's
release manifest, so it does not require other project checkouts. Its evidence
covers the current local bundle source with those declared compatible inputs;
it does not establish compatibility with newer component source revisions or a
published Spec Kit Flow release.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

from test_bundle_lifecycle import (
    FEEDBACK_ID,
    ROADMAP_ID,
    WIKI_ID,
    LocalCatalog,
    ROOT,
    WORKFLOW_IDS,
    archive_extension,
    extension_manifest,
    released_feedback_source,
    sha256,
)


SPECIFY_BIN = os.environ.get("SPECIFY_BIN", "specify")
RELEASE_PATH = ROOT / "catalog/release.json"
BUNDLE_PATH = ROOT / "bundles/spec-kit-flow/bundle.yml"
INDEPENDENT_WORKFLOW = ROOT / "tests/consumer-fixtures/independent-workflow.yml"


def extract_pinned_extension(extension_id: str, destination: Path) -> tuple[Path, dict[str, str]]:
    """Extract one checksum-verified release package into a temporary tree."""
    release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    entry = release["extensions"][extension_id]
    archive_path = ROOT / "catalog/packages" / entry["artifact"]
    if sha256(archive_path) != entry["sha256"]:
        raise AssertionError(f"release archive checksum differs for {extension_id}")
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            parts = Path(member.filename).parts
            if not parts or parts[0] != extension_id or ".." in parts:
                raise AssertionError(f"unsafe path in {extension_id} release archive")
            archive.extract(member, destination)
    source = destination / extension_id
    manifest = extension_manifest(source)
    if manifest.get("id") != extension_id or manifest.get("version") != entry["version"]:
        raise AssertionError(f"release metadata and manifest disagree for {extension_id}")
    return source, entry


class SnapshotValidationTests(unittest.TestCase):
    """Install, refresh, and remove a snapshot without damaging consumer data."""

    def test_snapshotLifecycle_preservesConsumerFilesAndRecordsProvenance(self) -> None:
        specify_path = shutil.which(SPECIFY_BIN)
        if specify_path is None:
            self.skipTest(f"Specify CLI not found: {SPECIFY_BIN}")

        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-snapshot-") as temporary:
            fixture = Path(temporary)
            consumer = fixture / "consumer"
            consumer.mkdir()
            home = fixture / "home"
            home.mkdir()

            roadmap_source, roadmap_release = extract_pinned_extension(ROADMAP_ID, fixture / "roadmap")
            wiki_source, wiki_release = extract_pinned_extension(WIKI_ID, fixture / "wiki")
            feedback_source = released_feedback_source(fixture / "feedback")
            sources = {ROADMAP_ID: roadmap_source, WIKI_ID: wiki_source, FEEDBACK_ID: feedback_source}
            with LocalCatalog(fixture / "catalog", sources) as local_catalog:
                environment = os.environ.copy()
                environment.update({
                    "HOME": str(home),
                    "SPECKIT_CATALOG_URL": local_catalog.extension_url,
                    "SPECKIT_WORKFLOW_CATALOG_URL": local_catalog.workflow_url,
                })

                def run_specify(*arguments: str) -> str:
                    completed = subprocess.run(
                        [specify_path, *arguments],
                        cwd=consumer,
                        env=environment,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        check=False,
                    )
                    self.assertEqual(0, completed.returncode, completed.stdout)
                    return completed.stdout

                cli_version = subprocess.run(
                    [specify_path, "--version"], text=True, capture_output=True, check=True
                ).stdout.strip()
                run_specify(
                    "init", "--here", "--force", "--non-interactive", "--integration", "codex",
                    "--integration-options=--skills",
                )

                consumer_files = {
                    consumer / "AGENTS.md": "# Consumer guidance\nKeep this file.\n",
                    consumer / ".codex/agents/coder.toml": 'name = "Coder"\ndescription = "Consumer-owned"\n',
                    consumer / "specs/local/README.md": "Consumer-owned feature data.\n",
                    consumer / "unrelated/keep.txt": "Unrelated project file.\n",
                }
                for path, contents in consumer_files.items():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(contents, encoding="utf-8")
                consumer_hashes = {path: sha256(path) for path in consumer_files}
                run_specify("workflow", "add", "--dev", str(INDEPENDENT_WORKFLOW))
                unrelated_workflow = consumer / ".specify/workflows/independent-consumer-check/workflow.yml"
                self.assertTrue(unrelated_workflow.is_file())
                unrelated_hash = sha256(unrelated_workflow)

                run_specify("bundle", "install", str(BUNDLE_PATH))
                installed_record = json.loads((consumer / ".specify/bundle-records.json").read_text(encoding="utf-8"))
                installed = installed_record["bundles"][0]
                self.assertEqual("spec-kit-flow", installed["bundle_id"])
                contributions = installed["contributed_components"]
                expected_components = {
                    ("extensions", ROADMAP_ID), ("extensions", WIKI_ID), ("extensions", FEEDBACK_ID),
                    *(('workflows', workflow_id) for workflow_id in WORKFLOW_IDS),
                }
                self.assertEqual(expected_components, {(item["kind"], item["id"]) for item in contributions})
                self.assertTrue(all(item.get("version") for item in contributions))
                self.assertEqual(consumer_hashes, {path: sha256(path) for path in consumer_files})

                run_specify("bundle", "install", str(BUNDLE_PATH), "--refresh")
                refreshed = json.loads((consumer / ".specify/bundle-records.json").read_text(encoding="utf-8"))
                refreshed_contributions = refreshed["bundles"][0]["contributed_components"]
                self.assertEqual(
                    {(item["kind"], item["id"], item["version"]) for item in contributions},
                    {(item["kind"], item["id"], item["version"]) for item in refreshed_contributions},
                )
                self.assertEqual(consumer_hashes, {path: sha256(path) for path in consumer_files})
                self.assertEqual(unrelated_hash, sha256(unrelated_workflow))

                run_specify("bundle", "remove", "spec-kit-flow")
                self.assertEqual(consumer_hashes, {path: sha256(path) for path in consumer_files})
                self.assertEqual(unrelated_hash, sha256(unrelated_workflow))
                self.assertFalse((consumer / ".specify/workflows/speckit-flow-implement/workflow.yml").exists())
                self.assertFalse((consumer / ".specify/extensions/flow-roadmap").exists())
                self.assertFalse((consumer / ".specify/extensions/flow-wiki").exists())

            release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
            bundle = yaml.safe_load(BUNDLE_PATH.read_text(encoding="utf-8"))["bundle"]
            git_head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
            ).stdout.strip()
            provenance = {
                "specify_cli": cli_version,
                "snapshot": {
                    "bundle_id": bundle["id"],
                    "bundle_version": bundle["version"],
                    "source": str(BUNDLE_PATH.relative_to(ROOT)),
                    "source_revision": git_head,
                },
                "components": {
                    extension_id: {
                        "version": release["extensions"][extension_id]["version"],
                        "sha256": release["extensions"][extension_id]["sha256"],
                        "source_repository": release["extensions"][extension_id]["source_repository"],
                        "source_commit": release["extensions"][extension_id]["source_commit"],
                        "source_tag": release["extensions"][extension_id]["source_tag"],
                    }
                    for extension_id in (ROADMAP_ID, WIKI_ID, FEEDBACK_ID)
                },
                "result": "install-refresh-remove-passed; consumer files and unrelated workflow preserved",
                "limits": [
                    "Roadmap and wiki inputs are checksum-pinned release packages, not current working trees.",
                    "This validates the local bundle snapshot against its declared component versions; it does not establish publication or consumer adoption.",
                ],
            }
            self.assertEqual("spec-kit-flow", provenance["snapshot"]["bundle_id"])
            self.assertTrue(all(provenance["components"][key]["source_commit"] for key in (ROADMAP_ID, WIKI_ID, FEEDBACK_ID)))
            report_output = os.environ.get("SPEC_KIT_FLOW_SNAPSHOT_REPORT")
            if report_output:
                report_path = Path(report_output)
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()

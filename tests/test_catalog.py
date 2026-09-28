"""Focused integrity checks for the checked-in consumer catalog release."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from tools import catalog


class CatalogReleaseTests(unittest.TestCase):
    def test_selectedSpecify_prefersProjectMiseSelection(self) -> None:
        with patch.object(catalog.shutil, "which", side_effect=lambda name: "/usr/bin/mise" if name == "mise" else "/path/specify"), patch.object(
            catalog.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "/mise/specify\n", "")
        ) as run:
            with patch.object(catalog.Path, "is_file", return_value=True), patch.object(catalog.os, "access", return_value=True):
                self.assertEqual("/mise/specify", catalog.selected_specify(Path("/consumer")))
        self.assertEqual(["/usr/bin/mise", "which", "specify"], run.call_args.args[0])

    def test_catalogRemove_dispatchesCompleteLifecycle(self) -> None:
        with patch.object(catalog.sys, "argv", ["catalog.py", "remove", "/consumer"]), patch.object(catalog, "remove") as remove:
            self.assertEqual(0, catalog.main())
        remove.assert_called_once_with(Path("/consumer"))

    def test_controllerManifest_hasEightStableBindingsAndDisplayNames(self) -> None:
        manifest = catalog.controller_manifest()
        self.assertEqual("flow-kit-controllers", manifest["package_id"])
        self.assertEqual("1.0.10.dev0+pegagio.2", manifest["specify_cli_version"])
        self.assertEqual(8, len(manifest["controllers"]))
        self.assertEqual(
            [
                ("flow-kit-start-feature", "FlowKit Start Feature", "speckit-flow-start-feature"),
                ("flow-kit-clarify", "FlowKit Clarify", "speckit-flow-clarify"),
                ("flow-kit-plan", "FlowKit Plan", "speckit-flow-plan"),
                ("flow-kit-tasks", "FlowKit Tasks", "speckit-flow-tasks"),
                ("flow-kit-analyze-remediate", "FlowKit Analyze", "speckit-flow-analyze-remediate"),
                ("flow-kit-implement", "FlowKit Implement", "speckit-flow-implement"),
                ("flow-kit-converge", "FlowKit Converge", "speckit-flow-converge"),
                ("flow-kit-closeout", "FlowKit Close Out", "speckit-flow-closeout"),
            ],
            [(item["skill_id"], item["display_name"], item["workflow_id"]) for item in manifest["controllers"]],
        )

    def test_controllerPackage_containsSharedRuntimeAndEightCodexSkills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "controller-package.zip"
            catalog.package_controller(archive)
            with zipfile.ZipFile(archive) as package:
                names = set(package.namelist())
                members = {name: package.read(name).decode("utf-8") for name in names}
                self.assertIn(".specify/flow-kit/manifest.yml", names)
                self.assertIn(".specify/flow-kit/controller-protocol.md", names)
                self.assertIn(".specify/flow-kit/scripts/python/controller.py", names)
                self.assertEqual(8, sum(name.endswith("/SKILL.md") and name.startswith(".agents/skills/flow-kit-") for name in names))
                self.assertEqual(8, sum(name.endswith("/agents/openai.yaml") and name.startswith(".agents/skills/flow-kit-") for name in names))
                for skill_id, display_name, _ in catalog.CONTROLLER_BINDINGS:
                    metadata = members[f".agents/skills/{skill_id}/agents/openai.yaml"]
                    self.assertIn(f'display_name: "{display_name}"', metadata)
                    self.assertRegex(metadata, r"(?m)^  short_description: \"[^\"]+\"$")

    def test_assignmentMatrix_matchesReviewedWorkflowPackage(self) -> None:
        expectations = {
            "speckit-flow-start-feature": {"assess-eligibility": ("gpt-6-sol", None), "draft-specification": ("gpt-6-sol", None), "brief-against-roadmap": ("gpt-6-sol", None)},
            "speckit-flow-clarify": {"clarify-specification": ("gpt-6-sol", None)},
            "speckit-flow-plan": {"create-plan": ("gpt-6-astra", None), "return-to-clarification": ("gpt-6-sol", None)},
            "speckit-flow-tasks": {"generate-tasks": ("gpt-6-luna", "high"), "return-to-plan": ("gpt-6-sol", None)},
            "speckit-flow-analyze-remediate": {
                "analyze-artifacts": ("gpt-6-astra", None), "remediate-specification": ("gpt-6-sol", None),
                "replan-after-specification": ("gpt-6-astra", None), "retask-after-specification": ("gpt-6-sol", None),
                "reanalyze-after-specification": ("gpt-6-astra", None), "remediate-plan": ("gpt-6-sol", None),
                "retask-after-plan": ("gpt-6-sol", None), "reanalyze-after-plan": ("gpt-6-astra", None),
                "remediate-tasks": ("gpt-6-sol", None), "reanalyze-after-tasks": ("gpt-6-astra", None),
            },
            "speckit-flow-implement": {
                "implement-eligible-work": ("gpt-6-luna", "high"), "return-to-analysis": ("gpt-6-sol", None),
                "return-to-specification": ("gpt-6-sol", None), "return-to-plan": ("gpt-6-sol", None),
                "return-to-tasks": ("gpt-6-sol", None),
            },
            "speckit-flow-converge": {"assess-convergence": ("gpt-6-astra", None), "return-remediation-to-analysis": ("gpt-6-sol", None)},
            "speckit-flow-closeout": {"debrief-roadmap": ("gpt-6-sol", None), "ingest-curated-context": ("gpt-6-sol", None), "lint-wiki": ("gpt-6-sol", None)},
        }
        for workflow_id, steps in expectations.items():
            text = (catalog.ROOT / "workflows" / workflow_id / "workflow.yml").read_text(encoding="utf-8")
            actual = {}
            lines = text.splitlines()
            for index, line in enumerate(lines):
                match = __import__("re").match(r'^(\s*)- id: ([A-Za-z0-9_-]+)$', line)
                if not match:
                    continue
                indent, step_id = match.groups()
                model = effort = None
                for following in lines[index + 1:]:
                    if following.startswith(indent + "- id:") or (following.strip() and len(following) - len(following.lstrip()) < len(indent)):
                        break
                    model_match = __import__("re").match(r'^' + __import__("re").escape(indent) + r'  model: "([^\"]+)"$', following)
                    effort_match = __import__("re").match(r"^" + __import__("re").escape(indent) + r"  reasoning_effort: (\S+)$", following)
                    if model_match:
                        model = model_match.group(1)
                    if effort_match:
                        effort = effort_match.group(1)
                if model:
                    actual[step_id] = (model, effort)
            self.assertEqual(steps, actual, workflow_id)
            self.assertNotRegex(text, r"(?m)^  (?:model|reasoning_effort):")

    def test_controllerInstallAndRemoval_preservesConsumerOwnedContentAndRecovery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / ".specify/flow-controllers/runs/existing").mkdir(parents=True)
            (project / ".specify/workflow-feedback").mkdir(parents=True)
            recovery = project / ".specify/flow-controllers/runs/existing/summary.json"
            recovery.write_text('{"status":"stopped"}\n', encoding="utf-8")
            feedback = project / ".specify/workflow-feedback/observations.jsonl"
            feedback.write_text('{"observation_id":"local"}\n', encoding="utf-8")
            local_skill = project / ".agents/skills/local-review/SKILL.md"
            local_skill.parent.mkdir(parents=True)
            local_skill.write_text("consumer-owned", encoding="utf-8")
            archive = project / "controller-package.zip"
            catalog.package_controller(archive)
            catalog.install_controller_package(project, archive, refresh=False, source_digest=catalog.digest(archive), catalog_status="snapshot")
            record = json.loads((project / ".specify/flow-kit/skills-install.json").read_text(encoding="utf-8"))
            self.assertEqual("installed", record["status"])
            self.assertEqual(8, len(record["controllers"]))
            catalog.remove_controller_package(project)
            self.assertTrue(recovery.is_file())
            self.assertTrue(feedback.is_file())
            self.assertEqual("consumer-owned", local_skill.read_text(encoding="utf-8"))
            self.assertFalse((project / ".specify/flow-kit/skills-install.json").exists())
            self.assertFalse((project / ".agents/skills/flow-kit-tasks").exists())

    def test_controllerInstall_preflightsNameCollisionBeforeWriting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            conflict = project / ".agents/skills/flow-kit-clarify/SKILL.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("consumer-owned", encoding="utf-8")
            archive = project / "controller-package.zip"
            catalog.package_controller(archive)
            with self.assertRaisesRegex(ValueError, "consumer-owned path conflicts"):
                catalog.install_controller_package(project, archive, refresh=False, source_digest=catalog.digest(archive), catalog_status="snapshot")
            self.assertEqual("consumer-owned", conflict.read_text(encoding="utf-8"))
            self.assertFalse((project / ".specify/flow-kit/skills-install.json").exists())

    def test_controllerRefreshAndRemoval_preserveLocallyEditedOwnedFile(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            archive = project / "controller-package.zip"
            catalog.package_controller(archive)
            catalog.install_controller_package(project, archive, refresh=False, source_digest=catalog.digest(archive), catalog_status="snapshot")
            edited = project / ".agents/skills/flow-kit-tasks/SKILL.md"
            edited.write_text(edited.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "locally changed FlowKit-owned"):
                catalog.install_controller_package(project, archive, refresh=True, source_digest=catalog.digest(archive), catalog_status="snapshot")
            with self.assertRaisesRegex(ValueError, "locally changed FlowKit-owned"):
                catalog.remove_controller_package(project)
            self.assertIn("local edit", edited.read_text(encoding="utf-8"))

    def test_controllerRemoval_rejectsOwnershipPathEscape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "consumer"
            record_path = project / ".specify/flow-kit/skills-install.json"
            record_path.parent.mkdir(parents=True)
            outside = root / "outside.txt"
            outside.write_text("consumer-owned", encoding="utf-8")
            record_path.write_text(json.dumps({
                "package": "flow-kit-controllers", "status": "installed",
                "files": {"../outside.txt": catalog.digest(outside)},
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ownership path"):
                catalog.remove_controller_package(project, preflight_only=True)
            self.assertEqual("consumer-owned", outside.read_text(encoding="utf-8"))

    def test_controllerInstall_rejectsSymlinkedSkillParent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "consumer"
            other = root / "other-skills"
            other.mkdir()
            (project / ".agents").mkdir(parents=True)
            (project / ".agents/skills").symlink_to(other, target_is_directory=True)
            archive = root / "controller-package.zip"
            catalog.package_controller(archive)
            with self.assertRaisesRegex(ValueError, "ownership path crosses a symlink"):
                catalog.install_controller_package(project, archive, refresh=False, source_digest=catalog.digest(archive), catalog_status="snapshot")
            self.assertEqual([], list(other.iterdir()))

    def test_controllerInstall_rollsBackAfterPartialFileWrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            archive = project / "controller-package.zip"
            catalog.package_controller(archive)
            atomic_write = catalog._atomic_bytes
            calls = 0

            def fail_once(path: Path, content: bytes) -> None:
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise OSError("simulated partial install failure")
                atomic_write(path, content)

            with patch.object(catalog, "_atomic_bytes", side_effect=fail_once):
                with self.assertRaisesRegex(OSError, "partial install failure"):
                    catalog.install_controller_package(project, archive, refresh=False, source_digest=catalog.digest(archive), catalog_status="snapshot")
            self.assertFalse((project / ".specify/flow-kit/skills-install.json").exists())
            self.assertFalse(any((project / ".agents/skills").glob("flow-kit-*/**/*")))

    def test_install_allowsSourceCheckout_butRejectsNestedTarget(self) -> None:
        with patch.object(catalog, "verified_release", side_effect=ValueError("release checked")):
            with self.assertRaisesRegex(ValueError, "release checked"):
                catalog.install(catalog.ROOT, False)
            with self.assertRaisesRegex(ValueError, "must not be nested"):
                catalog.install(catalog.ROOT / "workflows", False)

    def test_verifiedRelease_rejectsSnapshotRelabeledAsReleased(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-catalog-status-") as temporary:
            temporary_catalog = Path(temporary)
            temporary_release = temporary_catalog / "release.json"
            release = catalog.build_development_snapshot(temporary_catalog)
            release["status"] = "released"
            release["extensions"]["flow-roadmap"]["source_tag"] = None
            temporary_release.write_text(json.dumps(release), encoding="utf-8")
            with patch.object(catalog, "CATALOG", temporary_catalog), patch.object(catalog, "RELEASE", temporary_release):
                with self.assertRaisesRegex(ValueError, "source tag differs"):
                    catalog.verified_release(temporary_catalog, temporary_release)

    def test_verifiedRelease_rejectsControllerInventoryMismatch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-controller-inventory-") as temporary:
            temporary_catalog = Path(temporary)
            release_path = temporary_catalog / "release.json"
            release = catalog.build_development_snapshot(temporary_catalog)
            release["controller_package"]["controllers"] = []
            release_path.write_text(json.dumps(release), encoding="utf-8")
            with patch.object(catalog, "CATALOG", temporary_catalog), patch.object(catalog, "RELEASE", release_path):
                with self.assertRaisesRegex(ValueError, "controller inventory differs"):
                    catalog.verified_release(temporary_catalog, release_path)

    def test_install_rejectsSnapshot_beforeStartingCatalog(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-consumer-") as project:
            Path(project, ".specify").mkdir()
            snapshot = {"status": "snapshot"}
            with patch.object(catalog, "verified_release", return_value=snapshot):
                with self.assertRaisesRegex(ValueError, "development snapshot"):
                    catalog.install(Path(project), False)
            with patch.object(catalog, "build_development_snapshot", side_effect=ValueError("snapshot built")):
                with self.assertRaisesRegex(ValueError, "snapshot built"):
                    catalog.install(Path(project), True, True)

    def test_releaseTag_requiresAnnotatedTagAtCheckedOutCommit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-release-tag-") as temporary:
            source = Path(temporary)
            for arguments in (
                ("init", "-q"),
                ("config", "user.name", "Example Maintainer"),
                ("config", "user.email", "maintainer@example.invalid"),
            ):
                subprocess.run(["git", *arguments], cwd=source, check=True, capture_output=True)
            (source / "extension.yml").write_text("version: 1.0.0\n", encoding="utf-8")
            subprocess.run(["git", "add", "extension.yml"], cwd=source, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "Initial release"], cwd=source, check=True, capture_output=True)
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=source, check=True, capture_output=True, text=True).stdout.strip()
            with self.assertRaisesRegex(ValueError, "annotated v1.0.0"):
                catalog.release_tag(source, "1.0.0", commit)
            subprocess.run(["git", "tag", "-a", "v1.0.0", "-m", "Release 1.0.0"], cwd=source, check=True, capture_output=True)
            self.assertEqual("v1.0.0", catalog.release_tag(source, "1.0.0", commit))
            with self.assertRaisesRegex(ValueError, "HEAD differs"):
                catalog.release_tag(source, "1.0.0", "0" * 40)

    def test_localReleaseSources_rejectDirtyWorkflowAndBundle(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-release-source-") as temporary:
            root = Path(temporary)
            for arguments in (("init", "-q"), ("config", "user.name", "Example Maintainer"), ("config", "user.email", "maintainer@example.invalid")):
                subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)
            workflow = root / "workflows/example/workflow.yml"
            bundle = root / "bundles/spec-kit-flow/bundle.yml"
            workflow.parent.mkdir(parents=True)
            bundle.parent.mkdir(parents=True)
            workflow.write_text("version: 1\n", encoding="utf-8")
            bundle.write_text("version: 1\n", encoding="utf-8")
            subprocess.run(["git", "add", "workflows", "bundles"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "Initial release"], cwd=root, check=True, capture_output=True)
            catalog.require_local_release_sources_clean(root)
            for path in (workflow, bundle):
                path.write_text("version: 2\n", encoding="utf-8")
                with self.subTest(path=path), self.assertRaisesRegex(ValueError, "uncommitted"):
                    catalog.require_local_release_sources_clean(root)
                path.write_text("version: 1\n", encoding="utf-8")

    def test_verifiedRelease_rejectsChangedPackage_whenChecksumNoLongerMatches(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-catalog-integrity-") as temporary:
            temporary_catalog = Path(temporary)
            temporary_release = temporary_catalog / "release.json"
            release = catalog.build_development_snapshot(temporary_catalog)
            package = temporary_catalog / "packages" / release["extensions"]["flow-feedback"]["artifact"]
            package.write_bytes(package.read_bytes() + b"changed")
            with patch.object(catalog, "CATALOG", temporary_catalog), patch.object(catalog, "RELEASE", temporary_release):
                with self.assertRaisesRegex(ValueError, "missing or mismatched: flow-feedback"):
                    catalog.verified_release(temporary_catalog, temporary_release)


if __name__ == "__main__":
    unittest.main()

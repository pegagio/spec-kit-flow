"""Focused integrity checks for the checked-in consumer catalog release."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import catalog


class CatalogReleaseTests(unittest.TestCase):
    def test_verifiedRelease_rejectsSnapshotRelabeledAsReleased(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-catalog-status-") as temporary:
            temporary_catalog = Path(temporary)
            shutil.copytree(catalog.CATALOG / "packages", temporary_catalog / "packages")
            temporary_release = temporary_catalog / "release.json"
            release = json.loads(catalog.RELEASE.read_text(encoding="utf-8"))
            release["status"] = "released"
            release["extensions"]["flow-roadmap"]["source_tag"] = None
            temporary_release.write_text(json.dumps(release), encoding="utf-8")
            with patch.object(catalog, "CATALOG", temporary_catalog), patch.object(catalog, "RELEASE", temporary_release):
                with self.assertRaisesRegex(ValueError, "source tag differs"):
                    catalog.verified_release()

    def test_install_rejectsSnapshot_beforeStartingCatalog(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-consumer-") as project:
            with tempfile.TemporaryDirectory(prefix="spec-kit-flow-catalog-snapshot-") as temporary:
                temporary_catalog = Path(temporary)
                shutil.copytree(catalog.CATALOG / "packages", temporary_catalog / "packages")
                temporary_release = temporary_catalog / "release.json"
                release = json.loads(catalog.RELEASE.read_text(encoding="utf-8"))
                release["status"] = "snapshot"
                temporary_release.write_text(json.dumps(release), encoding="utf-8")
                with patch.object(catalog, "CATALOG", temporary_catalog), patch.object(catalog, "RELEASE", temporary_release):
                    with self.assertRaisesRegex(ValueError, "development snapshot"):
                        catalog.install(Path(project), False)
                    with self.assertRaisesRegex(ValueError, "development snapshot"):
                        catalog.install(Path(project), True)

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

    def test_verifiedRelease_rejectsChangedPackage_whenChecksumNoLongerMatches(self) -> None:
        catalog.verified_release()
        with tempfile.TemporaryDirectory(prefix="spec-kit-flow-catalog-integrity-") as temporary:
            temporary_catalog = Path(temporary)
            shutil.copytree(catalog.CATALOG / "packages", temporary_catalog / "packages")
            temporary_release = temporary_catalog / "release.json"
            shutil.copy2(catalog.RELEASE, temporary_release)
            release = json.loads(temporary_release.read_text(encoding="utf-8"))
            package = temporary_catalog / "packages" / release["extensions"]["flow-feedback"]["artifact"]
            package.write_bytes(package.read_bytes() + b"changed")
            with patch.object(catalog, "CATALOG", temporary_catalog), patch.object(catalog, "RELEASE", temporary_release):
                with self.assertRaisesRegex(ValueError, "missing or mismatched: flow-feedback"):
                    catalog.verified_release()


if __name__ == "__main__":
    unittest.main()

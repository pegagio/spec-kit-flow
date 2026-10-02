"""One-path argument and dash-prefixed path tests."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
SCRIPT = Path(__file__).resolve().parents[1] / "normalize_text.py"
class UsageTests(unittest.TestCase):
    def test_zero_two_and_stdin_sentinel_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            for arguments in ([], ["first", "second"], ["-"]):
                with self.subTest(arguments=arguments):
                    result = subprocess.run([sys.executable, str(SCRIPT), *arguments], cwd=directory, input=b"stdin must not be used", capture_output=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, b"")
                    self.assertTrue(result.stderr)
    def test_dash_path_with_separator(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "-input"
            path.write_bytes(b" a ")
            result = subprocess.run([sys.executable, str(SCRIPT), "--", "-input"], cwd=directory, capture_output=True)
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, b"a\n", b""))
            self.assertEqual(path.read_bytes(), b" a ")

"""Rejection status, channels, and input immutability tests."""
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from normalize_text import main
SCRIPT = Path(__file__).resolve().parents[1] / "normalize_text.py"
class RejectionTests(unittest.TestCase):
    def test_missing_directory_and_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = root / "invalid"
            late = root / "late"
            invalid.write_bytes(b"\xff")
            late.write_bytes(b"valid prefix\n" * 10000 + b"\xff")
            cases = [(root / "missing", b"missing"), (root, b"directory"), (invalid, b"UTF-8"), (late, b"UTF-8")]
            for path, category in cases:
                with self.subTest(path=path.name):
                    original = path.read_bytes() if path.is_file() else None
                    result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, b"")
                    self.assertIn(category, result.stderr)
                    if original is not None:
                        self.assertEqual(path.read_bytes(), original)
    def test_os_read_failure_before_stdout(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("normalize_text.Path.read_bytes", side_effect=PermissionError("denied")), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(main(["input.txt"]), 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("read", stderr.getvalue())

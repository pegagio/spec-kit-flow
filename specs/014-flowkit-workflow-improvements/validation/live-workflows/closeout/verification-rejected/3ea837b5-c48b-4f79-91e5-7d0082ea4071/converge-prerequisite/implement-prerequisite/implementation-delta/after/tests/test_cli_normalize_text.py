"""Subprocess success-contract tests."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_normalize_text import EXAMPLES
SCRIPT = Path(__file__).resolve().parents[1] / "normalize_text.py"
class CliSuccessTests(unittest.TestCase):
    def test_exact_bytes_repeat_and_no_file_writes(self):
        for source, expected in EXAMPLES + [(" a \r\n" * 200000, "a\n" * 200000)]:
            with self.subTest(length=len(source)), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "input.txt"
                original = source.encode("utf-8")
                path.write_bytes(original)
                results = [subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True) for _ in range(2)]
                for result in results:
                    self.assertEqual((result.returncode, result.stdout, result.stderr), (0, expected.encode("utf-8"), b""))
                self.assertEqual(path.read_bytes(), original)
                self.assertEqual(list(Path(directory).iterdir()), [path])

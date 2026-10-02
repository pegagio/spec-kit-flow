"""Unit tests for the pure normalization contract."""
import unittest
from normalize_text import normalize

EXAMPLES = [(" a  b \r\n\r\n", "a  b\n\n"), ("a\rb", "a\nb\n"), ("", ""), (" \t", "\n"), ("a\n\n", "a\n\n"), ("\u00a0e\u0301\u00a0", "\u00a0e\u0301\u00a0\n"), ("\t a \t b \t\r\n\t\r", "a \t b\n\n"), ("x\u2028y", "x\u2028y\n")]
class NormalizeTests(unittest.TestCase):
    def test_exact_examples_and_idempotence(self):
        for source, expected in EXAMPLES:
            with self.subTest(source=source):
                self.assertEqual(normalize(source), expected)
                self.assertEqual(normalize(normalize(source)), expected)

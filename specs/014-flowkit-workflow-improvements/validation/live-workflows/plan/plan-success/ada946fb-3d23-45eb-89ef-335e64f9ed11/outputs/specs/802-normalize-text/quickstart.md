# Quickstart Validation: Normalize Text

This guide describes validation after implementation. The planned module and tests do not exist yet; the commands are future verification instructions, not claims of current execution.

## Prerequisites and Setup

Use Python 3.11 or later with its standard library. Work from the consumer root. No installation, network access or external package is required. Create temporary UTF-8 fixtures outside protected source documents and clean them up after validation.

## Unit and CLI Checks

Run the future suite with `python -m unittest discover -s tests -v`. Unit tests must compare the pure transform against every [exact CLI example](contracts/cli.md#exact-examples), preserve all blank lines and Unicode, and check idempotence. CLI tests should invoke `[sys.executable, "normalize_text.py", fixture_path]` with subprocess capture in binary mode, using tempfile-managed paths.

For each accepted fixture assert exit 0, exact expected stdout bytes, empty stderr and unchanged input digest. Repeat the invocation to prove SC-003 determinism. For missing paths, directories and invalid UTF-8 (including invalid bytes after a valid prefix), assert exit 2, nonempty category diagnostics on stderr and empty stdout. Reject zero and two positional paths; do not introduce stdin support. Exercise a large finite input and inspect that no explicit product size guard exists; this does not promise unlimited system memory.

## Manual Smoke Check

After implementation, from the consumer root run:

```sh
printf ' a  b \r\n\r\n' > /tmp/normalize-text-smoke.txt
python normalize_text.py /tmp/normalize-text-smoke.txt > /tmp/normalize-text-smoke.out
python -c 'from pathlib import Path; assert Path("/tmp/normalize-text-smoke.out").read_bytes() == b"a  b\n\n"; assert Path("/tmp/normalize-text-smoke.txt").read_bytes() == b" a  b \r\n\r\n"'
```

Temporary filenames are illustrative; select unoccupied paths for a manual run. Validate the full error matrix through the suite rather than relying on this one smoke example. Passing these checks supplies implementation evidence, while product and roadmap acceptance remain explicit human gates.

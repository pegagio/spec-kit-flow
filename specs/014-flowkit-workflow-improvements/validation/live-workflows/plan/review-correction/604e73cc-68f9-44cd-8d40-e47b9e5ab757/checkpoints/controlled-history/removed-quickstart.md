# Quickstart Validation: Normalize Text

These commands validate the future implementation; planning does not create the script or tests. Run from the consumer root with Python 3.11 or newer. No external packages, services, network access, or installation are required. See the [CLI contract](contracts/cli.md) and [data model](data-model.md) for detailed behavior.

## Setup and Unit Tests

Once `normalize_text.py` and `tests/test_normalize_text.py` are implemented, confirm the runtime and run the standard-library suite:

```sh
python3 --version
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The suite must compare exact bytes for every contract example, preserve non-ASCII whitespace and decomposed Unicode, exercise empty/whitespace-only input, retain trailing blanks, and repeat identical invocations. Tests must assert that input bytes do not change and no output files are created. Use temporary directories for fixtures and clean them through the test harness.

## End-to-End Success

Create a temporary UTF-8 file containing the actual bytes represented by `" a  b \r\n\r\n"`. Invoke `python3 normalize_text.py PATH` with PATH replaced by its shell-quoted temporary path. Capture stdout and stderr separately. Expect stdout bytes `"a  b\n\n"`, empty stderr, and status 0; compare the file before and after. Repeat with `"a\rb"` expecting `"a\nb\n"`, empty input expecting zero bytes, `" \t"` expecting exactly `"\n"`, and `"a\n\n"` expecting unchanged trailing LFs. Repeat each case twice to establish deterministic behavior.

## End-to-End Rejection and Boundaries

Run the CLI against a nonexistent path, a temporary directory, and a file containing invalid UTF-8 bytes such as hex FF. Each must yield status 2, nonempty stderr, and empty stdout. Invoke with zero and two path arguments and check the same channels/status. Test a path containing spaces as one quoted argument; supply stdin while a valid file is selected and confirm only the file affects the result. Validate a representative large file without adding a product length guard; this confirms ordinary large-input behavior, not an unlimited-memory guarantee.

## Completion Criteria

All exact examples and rejection cases pass, files remain unchanged, repeated results match, and the unit suite succeeds. These checks demonstrate behavior after implementation; they do not constitute human feature acceptance or authorize another workflow.

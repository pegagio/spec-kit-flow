# Quickstart Validation: Normalize Text

This guide applies after the proposed `normalize_text.py` and standard-library unit tests are implemented. Planning creates documentation only; the commands below have not yet validated an implementation.

## Prerequisites and Setup

Use the consumer's Python 3 interpreter and a local writable temporary directory for test fixtures. No package installation, network access or service is needed. Run commands from the consumer root. See [CLI contract](contracts/cli.md) for channels and [data model](data-model.md) for transformation rules.

## Unit Validation

Run `python3 -m unittest discover -s tests -v`. Require tests for every FR-001–FR-009 policy: one path/no stdin, strict UTF-8 and Unicode preservation, ASCII-only edge trimming, interior/trailing blank preservation, newline conversion, original-empty final-LF distinction, output-only channels, specified input failures and no explicit size cap. Include repeatability and input-byte preservation.

## Exact End-to-End Examples

Create small input files using shell `printf`, invoke the proposed script and compare bytes:

```sh
mkdir -p .validation/normalize-text
printf ' a  b \r\n\r\n' > .validation/normalize-text/input.txt
python3 normalize_text.py .validation/normalize-text/input.txt > .validation/normalize-text/actual.txt
printf 'a  b\n\n' > .validation/normalize-text/expected.txt
cmp .validation/normalize-text/expected.txt .validation/normalize-text/actual.txt
```

Require status 0, exact output `"a  b\n\n"`, and byte-identical input before/after invocation. Repeat with `"a\rb"` expecting `"a\nb\n"`, an empty file expecting zero output bytes, and `" \t"` expecting exactly one LF. Existing trailing LFs must remain. Also compare non-ASCII whitespace, decomposed Unicode and interior tabs exactly, without normalization. Repeat each invocation and compare byte-identical outputs.

## Error Validation

Invoke separately with a missing path, a directory and a fixture containing invalid UTF-8 bytes. Capture stdout and stderr separately and preserve the process status before running another command. Each must yield status 2, empty stdout and a category diagnostic on stderr. Verify the directory and all existing files remain unchanged. Zero/multiple positional arguments must also reject with status 2.

## Size and Completion

Exercise a reasonably large local UTF-8 fixture and compare exact expected bytes; this is a test size, not a product maximum or performance guarantee. Completion requires passing unit tests and the observable scenarios above. Failures remain implementation work; this planning guide does not authorize another workflow or claim acceptance.

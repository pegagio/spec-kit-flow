# Quickstart: Normalize Text Validation

This guide describes proposed implementation-time validation. No implementation or behavioral tests were executed during planning. The accepted [CLI contract](contracts/cli.md) and [data model](data-model.md) define the authoritative channels and transformation rules.

## Prerequisites and Setup

Use Python 3 with its standard library. After implementation supplies the proposed root `normalize_text.py` and `tests/test_normalize_text.py`, run commands from the consumer root. No installation, network service or external dependency is needed. Create disposable input fixtures, preserving original files for comparison:

```sh
python3 --version
mkdir -p .validation/normalize-text
python3 -m unittest discover -s tests -p 'test_normalize_text.py'
```

The test command must pass the transformation and CLI adapter cases below. The fixture directory is for future validation only; these setup commands have not run in this planning session.

## Exact Successful Scenarios

Create each fixture with bytes matching the input column, invoke `python3 normalize_text.py FILE`, and compare captured stdout as bytes rather than rendered terminal text. Every case returns status 0. Successful output must not modify the input or create an additional product output file. Test capture files are harness artifacts.

| Fixture input bytes | Expected stdout bytes | Coverage |
| --- | --- | --- |
| `b" a  b \r\n\r\n"` | `b"a  b\n\n"` | ASCII edge trim, interior spaces, CRLF, trailing blank lines |
| `b"a\rb"` | `b"a\nb\n"` | Bare CR conversion and missing final LF |
| `b""` | `b""` | Empty original input stays empty |
| `b" \t"` | `b"\n"` | Nonempty ASCII-space/tab-only input gains exactly one LF |
| `b"a\n\n"` | `b"a\n\n"` | Existing trailing LF characters remain |
| `b" \talpha\t  beta\t "` | `b"alpha\t  beta\n"` | Interior tabs/spaces remain |
| UTF-8 encoding of `" \u00a0e\u0301\u00a0 "` | UTF-8 encoding of `"\u00a0e\u0301\u00a0\n"` | Non-ASCII whitespace and decomposed Unicode remain unchanged |

A concrete proposed fixture/run/compare sequence for the first case is:

```sh
printf ' a  b \r\n\r\n' > .validation/normalize-text/input.txt
cp .validation/normalize-text/input.txt .validation/normalize-text/original.txt
python3 normalize_text.py .validation/normalize-text/input.txt > .validation/normalize-text/output.bin
printf 'a  b\n\n' > .validation/normalize-text/expected.bin
cmp .validation/normalize-text/expected.bin .validation/normalize-text/output.bin
cmp .validation/normalize-text/original.txt .validation/normalize-text/input.txt
python3 normalize_text.py .validation/normalize-text/input.txt > .validation/normalize-text/repeated.bin
cmp .validation/normalize-text/output.bin .validation/normalize-text/repeated.bin
```

Require status 0 from each invocation and successful `cmp` results. Repeat the same capture and original-file comparison for every table row. The unit tests should exercise mixed CRLF, CR and LF in one input and verify no broader Unicode separator normalization. Exercise a reasonably large valid fixture with identical semantics; its chosen size is a test sample, not a product limit.

## Rejected Inputs and Argument Boundaries

Run each specified rejection independently with captured stdout and stderr: a nonexistent path, a directory, and a file containing invalid UTF-8 bytes. Each must return exactly status 2, nonempty diagnostic stderr identifying the failure category, and empty stdout. Literal diagnostic wording is not prescribed. For example, after ensuring `missing.txt` does not exist:

```sh
python3 normalize_text.py .validation/normalize-text/missing.txt > .validation/normalize-text/rejected.out 2> .validation/normalize-text/rejected.err
status=$?
test "$status" -eq 2
test ! -s .validation/normalize-text/rejected.out
test -s .validation/normalize-text/rejected.err
```

Repeat with `.validation/normalize-text` as a directory argument. Create invalid UTF-8 with `printf '\377' > .validation/normalize-text/invalid.bin` and repeat the checks with that path, also comparing its original bytes after rejection. Diagnostic text must not disclose file contents. The adapter completes read and decode before writing successful stdout.

Invoke with zero paths and with two paths to verify argument rejection through status 2 and stderr. Invoke with one quoted path containing spaces to verify it remains one argument. Supplying stdin must not replace the required path; no batch input, in-place mutation or separate output destination is supported.

## Completion Criteria

The future unit tests and CLI captures must prove all nine FR policies and SC-001–SC-003: exact normalization bytes, specified rejections, unchanged input and repeatable output. Preserve original emptiness separately from normalized emptiness. Require strict UTF-8 and no Unicode normalization, ASCII-only edge trimming, all blank lines, CRLF/CR conversion and the conditional final LF. There is no explicit product size cap. Record actual implementation-time results separately; this planning guide does not claim implementation readiness, test execution or feature acceptance.

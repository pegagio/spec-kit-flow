# Quickstart: Validate Normalize Text

This guide validates the planned CLI against [spec.md](spec.md), [CLI contract](contracts/cli.md), and [data model](data-model.md). Implementation is pending: `normalize_text.py` and `tests/test_normalize_text.py` do not yet exist. Run the commands below only after implementation supplies those files; this planning session has not executed behavior tests.

## Prerequisites and Setup

Use Python 3.11 or newer with its standard library from the consumer root. No package installation, network service, or database is required. Create temporary UTF-8 input files for the cases below; represent escaped strings as actual bytes, not literal backslash sequences. For example, a POSIX shell can prepare the first case with `printf ' a  b \r\n\r\n' > input.txt`. Store fixtures and captured outputs in a disposable validation directory, keeping the input separate from output captures.

## Planned Commands

After implementation, run `python3 -m unittest discover -s tests -v` from the consumer root. Then invoke `python3 normalize_text.py PATH > actual.out 2> actual.err` for each fixture and capture its exit status immediately. Compare `actual.out` byte-for-byte with the expected UTF-8 bytes, inspect stderr, and compare the input against a saved byte-for-byte copy. Shell redirection creates validation captures; the utility itself must never write or modify a file.

## Exact Success Scenarios

All successful cases require status 0, empty stderr, unchanged input bytes, and exactly the stdout bytes below. Repeat each invocation on unchanged input and compare status and both output channels to establish SC-003 repeatability.

| Actual input bytes expressed as escaped text | Expected stdout expressed as escaped text | Coverage |
|---|---|---|
| `" a  b \r\n\r\n"` | `"a  b\n\n"` | FR-003 edge trim, FR-004 interior spaces and trailing blank line, FR-005 CRLF |
| `"a\rb"` | `"a\nb\n"` | FR-005 bare CR, FR-006 final LF |
| `""` | `""` | FR-006 original empty input |
| `" \t"` | `"\n"` | FR-003 ASCII edge trim, FR-006 nonempty original input |
| `"a\n\n"` | `"a\n\n"` | FR-004 and FR-006 preserve trailing LFs |
| `"\u00a0e\u0301\u00a0"` encoded as UTF-8 | `"\u00a0e\u0301\u00a0\n"` encoded as UTF-8 | FR-002 no Unicode normalization, FR-003 preserve non-ASCII whitespace |
| `"a\tb\n\n c \n"` | `"a\tb\n\nc\n"` | FR-003 and FR-004 interior tab and blank line |

FR-001 requires a single file-path argument, including a shell-quoted path containing spaces; no stdin mode is available. FR-007 requires stdout-only results and byte-identical inputs after every run. FR-009 requires a representative large readable file to succeed without a product size cutoff: repeat a simple known line enough times for a meaningful local test and compare the complete output to repeated expected bytes. No fixed maximum or throughput promise is implied; whole-file buffering remains subject to host memory limits.

## Rejection and Channel Checks

Invoke the planned command with a missing path, a directory path, and a file containing invalid UTF-8 (for example a single byte `0xff`). Each FR-008 case must return status 2, nonempty diagnostic stderr, and exactly zero stdout bytes. Verify the malformed file remains byte-identical. Also run the command with zero and two positional paths: the FR-001 parser contract requires the same status and channel behavior. Exact diagnostic wording is not prescribed. These checks must detect partial stdout from a decode failure, not merely check the exit status.

## Validation Interpretation

The unit-test suite should cover the pure transformation and subprocess interface described in [plan.md](plan.md). Exact successes cover SC-001, rejection status/channel assertions cover SC-002, and repeated runs cover SC-003. Passing future tests does not constitute operator feature acceptance or authorize a later workflow. This guide preserves the nine accepted product decisions and adds no tasks, implementation code, dependencies, or product choices.

# Implementation Validation: Normalize Text

T002–T012 were implemented and validated on 2026-10-01. T001 remains completed design history. These checks supply implementation evidence; human product and roadmap acceptance remain separate gates.

## Invocation and Runtime

Run `python normalize_text.py PATH` using Python 3.11 or later. Exactly one path is required; use `--` before dash-prefixed relative paths. Only the standard library is required. The CLI reads the full file and decodes strictly as UTF-8 before emitting any bytes. Buffering consumes memory proportional to input size; there is no product size threshold, and environmental memory exhaustion is not guaranteed to succeed.

## Validation Results

`python -m unittest discover -s tests -v` passed all six test methods, with subcases covering eight exact transformation examples, idempotence, repeated binary subprocess results, a 1,000,000-byte finite input, input immutability and absence of output files. T004/T005 were observed failing against the skeleton before US1 implementation. T008/T009 were observed failing on unhandled rejection before US2 correction; the diagnostics and subsequent green suite are retained in the run evidence.

The quickstart smoke case was executed using unoccupied tempfile-managed paths: input hex `2061202062200d0a0d0a`; stdout hex `612020620a0a`; status 0; empty stderr. The input stayed unchanged, no output file appeared, repeated invocations matched, and applying normalization again preserved the result.

Missing paths, directories, invalid UTF-8 at the beginning and after a valid prefix, deterministic OS read failure, and zero/two arguments yield status 2, category/usage diagnostics on stderr, and zero stdout. A missing `-` path is rejected rather than reading stdin. A dash-prefixed real path works with `--`. Invalid input bytes remain unchanged.

## Inspection and Hooks

Source inspection confirms ASCII-only edge stripping, explicit CRLF-before-CR conversion, literal LF splitting, preservation of Unicode and all trailing blank lines, original-input emptiness handling, and whole-file decode before output. There is no Unicode normalization, explicit size guard, stdin mode, file-write interface, network use or external dependency. Importing the module does not execute the CLI.

All 16 specification checklist items were checked before implementation edits. The required prerequisite command succeeded. Existing design/specification, contract, pointer, roadmap and baseline Git HEAD were preserved. Optional pre-implementation roadmap brief and optional post-implementation roadmap debrief/wiki ingest were offered and left unexecuted because this bounded invocation authorizes no later workflow. No mandatory hooks were registered. No unresolved implementation failure remains.

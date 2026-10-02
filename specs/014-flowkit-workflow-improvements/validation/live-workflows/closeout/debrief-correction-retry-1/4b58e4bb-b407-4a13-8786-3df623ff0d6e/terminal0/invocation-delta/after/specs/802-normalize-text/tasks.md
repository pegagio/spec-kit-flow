# Tasks: Normalize Text

Tasks derive from the reviewed specification, plan, research, data model, CLI contract and quickstart. Tests are required by the constitution. At generation, new tasks were unchecked; the checklist now records completed work, with completed design history preserved independently of implementation status.

## Table of Contents

[History](#completed-design-history) · [Setup](#phase-1-setup) · [Foundation](#phase-2-foundational) · [US1](#phase-3-user-story-1-normalize-local-text-p1-mvp) · [US2](#phase-4-user-story-2-understand-rejected-input-p2) · [Polish](#phase-5-polish-and-cross-cutting-validation) · [Dependencies](#dependencies-and-execution-order) · [Parallel examples](#parallel-examples) · [Strategy](#implementation-strategy)

## Completed Design History

This completed documentation task is backed by the reviewed contract; it does not claim implemented behavior or acceptance.

- [x] T001 [US1] Document reviewed CLI contract in specs/802-normalize-text/contracts/cli.md

## Phase 1: Setup

Establish only the reviewed Python 3.11+ standard-library module and test directory; no packaging, service, external dependency or build tool is needed.

- [X] T002 Create module skeleton normalize_text.py and tests/ directory for unittest discovery, preserving existing files and adding no external dependencies.

## Phase 2: Foundational

Define shared transient boundaries before story work. These are function boundaries rather than persistent domain classes.

- [X] T003 Define pure normalize(text) and main(argv) boundaries in normalize_text.py with no execution on import; preserve data-model constraints: Input request `path`: one local path string, "Exactly one argument; no stdin sentinel or output destination"; Input bytes `content`: byte sequence, "Read from request path without modification; missing/directory/read failures become rejection"; Input text `text`: Unicode string and `was_empty`: original emptiness, "Strict UTF-8 decoding; preserves Unicode code points and canonical form"; Normalized result `text`: Unicode string and `encoded`: UTF-8 bytes, "Produced from input text by FR-003–FR-006; emitted only after complete success"; Input rejection `category`: read or encoding failure, `diagnostic`: concise text, `status`: 2, "stderr diagnostic, zero stdout; no stored record".

Foundation checkpoint: importable boundaries exist without filesystem writes or network behavior. T003 depends on T002.

## Phase 3: User Story 1 — Normalize local text (P1, MVP)

Deliver deterministic successful normalization through one local file path. Independent validation uses exact stdout bytes, status 0, empty stderr, and unchanged input digest; US2 rejection work is not needed to demonstrate accepted input.

- [X] T004 [P] [US1] Write pure-transform unittest cases in tests/test_normalize_text.py for FR-002, FR-003, FR-004, FR-005 and FR-006: strict character preservation, ASCII-only edge trimming, interior whitespace, all trailing blank lines, CRLF then bare CR conversion, original-input emptiness, conditional final LF and idempotence; assert exact examples `" a  b \r\n\r\n"` → `"a  b\n\n"`, `"a\rb"` → `"a\nb\n"`, `""` → `""`, `" \t"` → `"\n"`, `"a\n\n"` → `"a\n\n"`, and `"\u00a0e\u0301\u00a0"` → `"\u00a0e\u0301\u00a0\n"`.
- [X] T005 [P] [US1] Write subprocess success-contract unittests in tests/test_cli_normalize_text.py using sys.executable and tempfile: one path, exact UTF-8 stdout, exit 0, empty stderr, unchanged input bytes and no additional output file; repeat accepted fixtures for SC-003 and exercise a large finite input without a product size threshold (FR-001, FR-007, FR-009).
- [X] T006 [US1] Implement normalize(text) in normalize_text.py after T004/T005 expose failures: replace CRLF before remaining CR, split/join literal LF preserving empty segments, strip only ASCII space/tab from each edge, preserve Unicode and interior whitespace, and append LF only for originally nonempty input whose result lacks LF; run tests/test_normalize_text.py.
- [X] T007 [US1] Implement successful main(argv) flow in normalize_text.py after T006: argparse exactly one positional path with no stdin/output-file mode, read raw bytes without modification, strict UTF-8 decode of complete input before emission, pure normalization, UTF-8 binary stdout and exit 0; impose no explicit size guard, support `--` for dash-prefixed paths, and run tests/test_cli_normalize_text.py plus tests/test_normalize_text.py.

US1 checkpoint: both success suites pass independently, including whitespace-only nonempty input producing exactly one LF. Buffering remains proportional to file size; do not promise unlimited memory.

## Phase 4: User Story 2 — Understand rejected input (P2)

Deliver deterministic input rejection after the successful CLI foundation. Independent tests exercise rejection status and channels without depending on the normalization output of a successful input.

- [X] T008 [P] [US2] Write rejection-contract unittests in tests/test_rejected_input.py for missing paths, directories, invalid UTF-8 and invalid bytes after a valid prefix; assert exit 2, nonempty concise category diagnostics on stderr, zero stdout and no input mutation (FR-008), including ordinary OS read failures using a deterministic standard-library test double where necessary.
- [X] T009 [P] [US2] Write argument-contract unittests in tests/test_cli_usage.py for zero and two positional paths producing status 2/stderr with no result output, no stdin mode, and successful dash-prefixed paths using `--`; use subprocess binary capture and temporary files (FR-001).
- [X] T010 [US2] Implement argument/read/decode rejection flow in normalize_text.py after T008/T009 expose failures: argparse arity validation, category diagnostics for missing/directory/other OS read errors and strict UTF-8 failure, status 2 and no stdout prefix; preserve all US1 behavior and run all four unittest files.

US2 checkpoint: each required rejection category independently satisfies status/channel assertions; the full success suite remains green.

## Phase 5: Polish and Cross-Cutting Validation

Validate the finished increments against the reviewed quickstart without changing product decisions or claiming acceptance.

- [X] T011 Run `python -m unittest discover -s tests -v` for tests/ and the smoke scenario in specs/802-normalize-text/quickstart.md using unoccupied temporary paths; record exact byte/status/channel, input immutability, repeated determinism and idempotence results in specs/802-normalize-text/validation/implementation.md; inspect normalize_text.py for no product size guard, Unicode normalization, stdin mode, output-file writes, external dependencies or network use.
- [X] T012 Document verified invocation, Python 3.11+ runtime, error categories and full-buffering environmental memory limitation in specs/802-normalize-text/validation/implementation.md after T011; distinguish test evidence from human product/roadmap acceptance and report any unresolved failures without marking their implementation tasks complete.

## Dependencies and Execution Order

The execution graph is T002 → T003 → (T004 ∥ T005) → T006 → T007 → (T008 ∥ T009) → T010 → T011 → T012. T001 is already-completed design history, not a blocking implementation task. Setup and foundation block both story phases. US2 integrates with the shared CLI completed in US1; its rejection criteria remain independently testable. Tests are authored and observed failing before the associated implementation. All normalize_text.py edits are sequential, as are the final validation document edits.

## Parallel Examples

Parallel eligibility applies only after each listed prerequisite completes. No same-file writers run concurrently.

### User Story 1

After T003, run T004 (tests/test_normalize_text.py) alongside T005 (tests/test_cli_normalize_text.py). Join both before T006; then execute T006 and T007 sequentially in normalize_text.py.

### User Story 2

After T007, run T008 (tests/test_rejected_input.py) alongside T009 (tests/test_cli_usage.py). Join both before T010. Do not run US1 and US2 implementation edits concurrently because they share normalize_text.py.

## Implementation Strategy

Deliver MVP through T002–T007 and validate US1 exact accepted examples before proceeding. Add T008–T010 as the rejection increment, then run T011–T012 to establish the complete contract evidence. Preserve T001 throughout and mark a new task complete only after its actual work and validation. No Git integration, publication, additional workflow or human acceptance follows automatically from these tasks.

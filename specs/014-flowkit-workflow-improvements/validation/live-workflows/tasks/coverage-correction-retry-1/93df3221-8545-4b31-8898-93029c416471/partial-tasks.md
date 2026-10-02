# Tasks: Normalize Text

This implementation task list derives from the reviewed spec, plan, research, data model, CLI contract and quickstart in `specs/802-normalize-text/`. Tests are required by the constitution. All new work is unchecked; completed design documentation does not establish implementation or acceptance.

## Table of Contents

- [Completed Design History](#completed-design-history)
- [Phase 1: Setup](#phase-1-setup)
- [Phase 2: Foundation](#phase-2-foundation)
- [Phase 3: US1 — Normalize Local Text (P1)](#phase-3-us1--normalize-local-text-p1)
- [Phase 4: US2 — Understand Rejected Input (P2)](#phase-4-us2--understand-rejected-input-p2)
- [Phase 5: Polish](#phase-5-polish)
- [Dependencies and Parallel Examples](#dependencies-and-parallel-examples)
- [Implementation Strategy](#implementation-strategy)

## Completed Design History

Preserve this independently reviewed design row exactly. It predates implementation ordering and is not an implementation prerequisite still needing work.

- [x] T001 [US1] Document reviewed CLI contract in specs/802-normalize-text/contracts/cli.md

## Phase 1: Setup

Establish the two planned source files without adding dependencies or packaging.

- [ ] T002 Create the standard-library unittest harness in tests/test_normalize_text.py using tempfile-managed fixtures and binary subprocess capture; provide helpers for exact stdout/stderr/status and unchanged input digest assertions.

## Phase 2: Foundation

Provide shared CLI structure before either story, keeping transformation pure and output deferred until success.

- [ ] T003 Create normalize(text) and main(argv) entry points in normalize_text.py with argparse, pathlib and sys only; implement the Input request constraint "Exactly one argument; no stdin sentinel or output destination" and support -- before dash-prefixed paths, with standard help and status-2 invalid arity handling.

## Phase 3: US1 — Normalize Local Text (P1)

Deliver normalized UTF-8 stdout with unchanged input. Independently validate exact output for all contract examples, mixed newline forms, ASCII edge trimming, preserved interior/blank-line content, non-ASCII whitespace, decomposed Unicode, empty and whitespace-only inputs; success must exit 0 with empty stderr and unchanged input bytes.

- [ ] T004 [US1] Write pure-transform unittest cases in tests/test_normalize_text.py for every contracts/cli.md exact example, mixed CRLF/CR/LF, interior spaces/tabs, trailing blank lines, non-ASCII whitespace, decomposed Unicode, Unicode separators, original empty input and nonempty whitespace-only input; verify idempotence and observe failures before implementing the transform (FR-002–FR-006, SC-001).
- [ ] T005 [US1] Implement pure normalization in normalize_text.py: CRLF then bare CR to LF, literal-LF splitting, ASCII space/tab edge trimming and preserved separators; enforce Input text constraint "Strict UTF-8 decoding; preserves Unicode code points and canonical form"; distinguish original emptiness so empty stays empty and nonempty gains LF only when needed (FR-002–FR-006).
- [ ] T006 [US1] Write accepted-input subprocess cases in tests/test_normalize_text.py for exact UTF-8 stdout, status 0, empty stderr, unchanged input digest, no output-file creation, dash-prefixed paths via -- and repeated deterministic results; add a large finite fixture with no product-size threshold (FR-001, FR-007, FR-009, SC-001, SC-003).
- [ ] T007 [US1] Implement successful read/decode/normalize/encode/emission flow in normalize_text.py with binary stdout and full buffering, no explicit product input-size limit or file writes; enforce Normalized result constraint "Produced from input text by FR-003–FR-006; emitted only after complete success" and run the US1 cases.

## Phase 4: US2 — Understand Rejected Input (P2)

Deliver category diagnostics with status 2 and zero stdout. Independently run the rejection matrix without depending on accepted-output examples: missing path, directory, invalid UTF-8 at the beginning and after valid text, argument-count failures and simulated OS read errors; existing input files remain unchanged.

- [ ] T008 [US2] Write rejection unittest/subprocess cases in tests/test_normalize_text.py for missing path, directory, invalid UTF-8 at beginning and after valid prefix, zero/two paths and mocked OS read failure; assert status 2, category diagnostic on stderr and zero stdout, with unchanged existing inputs (FR-008/SC-002).
- [ ] T009 [US2] Implement rejection handling in normalize_text.py for argument, read and strict decoding failures before any stdout emission; enforce Input bytes constraint "Read from request path without modification; missing/directory/read failures become rejection" and Input rejection constraint "stderr diagnostic, zero stdout; no stored record"; diagnostics identify the category without requiring fixed wording, and all specified failures exit 2.
- [ ] T010 [US2] Run the rejection matrix in tests/test_normalize_text.py, including late invalid UTF-8 and mocked read failures, then rerun accepted-input cases to prove error handling preserves success behavior and no input mutation.

## Phase 5: Polish

Finish cross-story verification and document the reviewed buffering tradeoff without changing product choices.

- [ ] T011 [P] Update specs/802-normalize-text/quickstart.md with implemented invocation and actual validation results after both stories; retain full-buffer O(n) memory tradeoff, no explicit product size limit and explicit human acceptance boundary.
- [ ] T012 [P] Validate normalize_text.py and tests/test_normalize_text.py with python -m unittest discover -s tests -v and the quickstart smoke scenario using unoccupied temporary paths; inspect standard-library-only imports, absence of network/packaging/stdin/output-file modes and product size guards, and record exact outcomes in the implementation report.

## Dependencies and Parallel Examples

The execution graph is T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010 → {T011, T012}. T001 is preserved completed design history. Setup and foundation block both story increments. US2 reuses the shared CLI/read pipeline from US1, so implement stories sequentially in priority order; their acceptance checks are independently selectable.

For US1, run T004 then T005, followed by T006 then T007. Tests and implementation touch shared files or depend on failing tests; there is no safe within-story parallel task pair. For US2, run T008 then T009 then T010 for the same reason. Do not concurrently edit either shared source file across stories. After T010, T011 documentation and T012 read-only validation can run in parallel on different files; keep temporary test data outside protected documents.

## Implementation Strategy

Deliver the US1 MVP after T002–T007 and validate its exact-output suite independently. Add US2 through T008–T010 and rerun both story suites; then finish T011–T012. Write and observe failing behavioral tests before each implementation change. Completion of tests or task checkboxes supplies evidence only; publication, Git integration, roadmap disposition and feature acceptance require separately authorized human decisions.

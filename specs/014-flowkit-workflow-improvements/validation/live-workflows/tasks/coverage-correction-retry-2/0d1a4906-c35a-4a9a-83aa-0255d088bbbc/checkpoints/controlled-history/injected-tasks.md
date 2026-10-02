# Tasks: Normalize Text

This task list derives from the approved spec, plan, research, data model, CLI contract and quickstart in `specs/802-normalize-text/`. Tests are required by the specification and constitution. Only the historical design row is completed; implementation and acceptance remain separate.

## Table of Contents

- [Completed Design History](#completed-design-history)
- [Phase 1: Setup](#phase-1-setup)
- [Phase 2: Foundation](#phase-2-foundation)
- [Phase 3: US1 — Normalize Local Text](#phase-3-us1--normalize-local-text)
- [Phase 4: US2 — Understand Rejected Input](#phase-4-us2--understand-rejected-input)
- [Phase 5: Polish](#phase-5-polish)
- [Dependencies and Execution Order](#dependencies-and-execution-order)
- [Parallel Examples](#parallel-examples)
- [Implementation Strategy](#implementation-strategy)

## Completed Design History

T001 records independently reviewed CLI design, not built behavior. Its exact completed history is preserved.

- [x] T001 [US1] Document reviewed CLI contract in specs/802-normalize-text/contracts/cli.md

## Phase 1: Setup

Prepare only the planned Python standard-library source and tests, without packaging, dependencies or services.

- [ ] T002 Establish the planned module and unittest file structure at normalize_text.py and tests/test_normalize_text.py; use Python 3.11 or later and standard library only, with no packaging or external dependencies.

## Phase 2: Foundation

The shared interface and test harness block both stories; define these before story behavior.

- [ ] T003 Define pure normalize(text) and thin main(argv) interfaces in normalize_text.py with Input request constraint "Exactly one argument; no stdin sentinel or output destination"; keep argument, file, transform and output responsibilities separate, without adding stdin or output-file support.
- [ ] T004 Build the standard-library unittest/subprocess/tempfile harness in tests/test_normalize_text.py; capture binary stdout/stderr and input digests so both stories can verify exact channels and unchanged files.

## Phase 3: US1 — Normalize Local Text

Priority P1, MVP. Produce deterministic normalized UTF-8 stdout while preserving the input. Independent criterion: every exact contract example, edge whitespace, Unicode, empty/unterminated input and trailing blank lines yields exact bytes, status 0, empty stderr and unchanged input digest.

- [ ] T005 [US1] Write failing transform tests in tests/test_normalize_text.py for all exact examples in specs/802-normalize-text/contracts/cli.md, including whitespace-only input yielding one LF, mixed CRLF/CR, retained trailing blank lines, interior spaces/tabs, NBSP and decomposed Unicode; check idempotence and repeatability (FR-002–FR-006, SC-001, SC-003).
- [ ] T006 [US1] Implement normalize(text) in normalize_text.py: convert CRLF then bare CR to LF, split on literal LF, trim only ASCII space/tab at each line edge, preserve interior whitespace and all blank lines, and append LF only for originally nonempty input whose result lacks LF; enforce Input text constraint "Strict UTF-8 decoding; preserves Unicode code points and canonical form" without Unicode normalization.
- [ ] T007 [US1] Add accepted-path CLI tests in tests/test_normalize_text.py, then wire full byte read, strict UTF-8 decode, transform, UTF-8 encode and binary stdout in normalize_text.py; enforce Normalized result constraint "Produced from input text by FR-003–FR-006; emitted only after complete success"; assert status 0, empty stderr, unchanged input, no output file, '--' dash-prefixed path handling and standard help behavior (FR-001, FR-002, FR-007).

## Phase 4: US2 — Understand Rejected Input

Priority P2. Reject invalid requests without partial output. Independent criterion: missing path, directory and invalid UTF-8, including after a valid prefix, each produces status 2, category diagnostics on stderr and zero stdout. Check invalid arity and OS read failures as the reviewed CLI contract requires.


## Phase 5: Polish

Validate the combined behavior and document the already approved resource tradeoff.

- [ ] T010 [P] Extend tests/test_normalize_text.py with a large finite UTF-8 fixture, repeated subprocess comparisons for SC-003 and file-digest checks; inspect normalize_text.py for absence of explicit product size guards (FR-009), then run python -m unittest discover -s tests -v and record actual results.
- [ ] T011 [P] Update specs/802-normalize-text/quickstart.md only when implementation exists to record the actual invocation and verified validation results, documenting full-buffer O(n) memory and environmental resource limits without introducing a product size cap.
- [ ] T012 Validate all exact examples and rejection categories against normalize_text.py and tests/test_normalize_text.py using specs/802-normalize-text/quickstart.md; record any failed checks before reporting implementation evidence, leaving product and roadmap acceptance to explicit human gates.

## Dependencies and Execution Order

The execution graph is T001 (completed design) → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → {T010, T011} → T012. T003/T004 are shared prerequisites. US1 is independently valid after T007; US2 tests and rejection implementation then extend the same CLI, and its rejection matrix is independently verifiable after T009. This explicit sequential story order prevents competing edits to the shared module and test file. Tests precede the related implementation; T007 first adds accepted-path tests before wiring emission. T010 and T011 may proceed concurrently only after T009, because they edit different files and have no mutual unfinished dependency. T012 depends on both.

## Parallel Examples

There is no safe simultaneous authoring within either story because tasks modify the same two small files in dependency order. This is intentional for the reviewed single-module design.

### US1 Example

Run T005, then T006, then T007; do not launch these together. After implementation, independent read-only checks for Unicode preservation and trailing blank-line preservation can run concurrently against separate temporary fixtures, without editing shared files.

### US2 Example

Run T008, then T009; do not launch these together. After implementation, missing-path and invalid-UTF-8 subprocess checks can run concurrently using separate temporary fixtures. Cross-cutting T010 and T011 are the only marked authoring parallel opportunity, after both stories are implemented.

## Implementation Strategy

Complete setup and foundation, then deliver the US1 MVP through T007 and verify its exact successful-output matrix. Add US2 through T009 and verify the independent rejection matrix without regressing US1. Complete T010/T011 and the final T012 validation. Task generation authorizes no implementation, Git integration, publication, roadmap mutation or feature acceptance; unchecked tasks are future work.

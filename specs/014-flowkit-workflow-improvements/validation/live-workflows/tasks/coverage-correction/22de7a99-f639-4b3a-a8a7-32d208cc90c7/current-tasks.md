# Tasks: Normalize Text

These tasks derive from the reviewed spec, plan, research, data model, CLI contract and quickstart in `specs/802-normalize-text/`. Python 3.11+ and the standard library are sufficient. Only the historical design row is completed; all implementation and validation remain future work.

## Table of Contents

[History](#completed-design-history) · [Setup](#phase-1-setup) · [Foundation](#phase-2-foundational-prerequisites) · [US1](#phase-3-user-story-1-normalize-local-text-p1-mvp) · [US2](#phase-4-user-story-2-understand-rejected-input-p2) · [Polish](#phase-5-polish-and-cross-cutting-validation) · [Dependencies](#dependencies-and-execution-order) · [Parallel examples](#parallel-examples) · [Strategy](#implementation-strategy)

## Completed Design History

This completed row documents independently reviewed design, not implementation or acceptance.

- [x] T001 [US1] Document reviewed CLI contract in specs/802-normalize-text/contracts/cli.md

## Phase 1: Setup

Establish the proposed source and test paths without introducing dependencies or packaging.

- [ ] T002 Create the planned module and unittest discovery skeleton in normalize_text.py and tests/test_normalize_text.py, using Python 3.11+ standard library only; leave product behavior for story tasks.

## Phase 2: Foundational Prerequisites

Provide shared interfaces for both stories without adding persistent models or storage.

- [ ] T003 Define pure normalize(text) and thin main(argv) boundaries in normalize_text.py; retain original emptiness for Input text (`text`: Unicode string; `was_empty`: original emptiness), and document transient Input bytes (`content`: byte sequence), Normalized result (`text`: Unicode string; `encoded`: UTF-8 bytes) and Input rejection (`category`: read or encoding failure; `diagnostic`: concise text; `status`: 2); no persistence schema or migration.

## Phase 3: User Story 1 — Normalize Local Text (P1, MVP)

Deliver deterministic normalization on valid local files. Independently verify exit 0, exact UTF-8 stdout, empty stderr and unchanged input bytes for every contract example, repeated invocation, a large finite fixture and dash-prefixed paths supplied after `--`.

- [ ] T004 [US1] Write pure-transform unittest cases in tests/test_normalize_text.py before implementation for all six exact examples in specs/802-normalize-text/contracts/cli.md, mixed CRLF/CR/LF, interior whitespace, trailing blank lines, non-ASCII edges, decomposed Unicode, empty and whitespace-only input; assert idempotence and FR-002–FR-006/SC-001/SC-003.
- [ ] T005 [US1] Implement normalize(text) in normalize_text.py: replace CRLF before bare CR, split on literal LF preserving empty segments, trim only ASCII space/tab at each edge, preserve interior whitespace/Unicode/trailing LFs, return empty for original empty input and conditionally append LF for original nonempty input; in particular `" \t"` produces exactly `"\n"`.
- [ ] T006 [US1] Write successful subprocess CLI unittest cases in tests/test_normalize_text.py using sys.executable, tempfile and binary capture; assert exactly one path succeeds, all contract bytes, exit 0/empty stderr, unchanged input digest, repeated determinism, dash-prefixed path after `--`, and large finite input without a product size cap.
- [ ] T007 [US1] Implement successful CLI flow in normalize_text.py using argparse, pathlib and binary stdout: enforce Input request constraint "Exactly one argument; no stdin sentinel or output destination"; read bytes without modification, enforce Input text constraint "Strict UTF-8 decoding; preserves Unicode code points and canonical form", and Normalized result constraint "Produced from input text by FR-003–FR-006; emitted only after complete success"; encode UTF-8 and emit only after full read/decode/normalization, with no output file, stdin mode, network or explicit input length guard (FR-001/FR-002/FR-007/FR-009).

## Phase 4: User Story 2 — Understand Rejected Input (P2)

Provide deterministic errors without partial stdout. Independently test missing paths, directories, invalid UTF-8 including a valid prefix followed by invalid bytes, zero/two positional arguments and a mocked ordinary OS read failure; check exit 2, nonempty category stderr and empty stdout. US2 builds on the shared CLI, but its rejection matrix can be exercised independently of normalization examples.


## Phase 5: Polish and Cross-Cutting Validation

Confirm both stories together and document observed validation without asserting human acceptance.

- [ ] T010 Extend cross-cutting unittest cases in tests/test_normalize_text.py to confirm determinism/idempotence and no mutation across the full acceptance/error matrix; run python -m unittest discover -s tests -v, resolving failures within the approved contract.
- [ ] T011 Inspect normalize_text.py for standard-library-only imports, no network/file writes/Unicode normalization/product size guard, and full decoding before output; record findings against FR-001–FR-009 in specs/802-normalize-text/validation.md.
- [ ] T012 Execute the temporary-file smoke example and full validation procedure from specs/802-normalize-text/quickstart.md after implementation; record exact commands, results and any environmental limits in specs/802-normalize-text/validation.md, preserving reviewed design documents and leaving acceptance to the operator.

## Dependencies and Execution Order

T001 is historical design evidence. Execute T002 → T003 before either story. US1: T004 → T005; T006 → T007, with T007 also depending on T005. Tests should demonstrate missing behavior before corresponding implementation and pass afterward. US2: T008 → T009; T009 depends on the CLI built by T007. T008 can be authored once the foundation exists, but US2 completion requires T007 and T009. T010 depends on both stories; T011 follows T010; T012 follows T011. Shared module/test files require serial editing: no task is marked [P].

Requirement coverage is FR-001: T006/T007/T008; FR-002: T004/T007/T008/T009; FR-003–FR-006: T004/T005; FR-007: T006/T007; FR-008: T008/T009; FR-009: T006/T007/T011. SC-001 is exact transformation/CLI bytes, SC-002 the rejection matrix, and SC-003 repeated behavior. Data-model invariants are checked by T004/T006/T008/T010.

## Parallel Examples

The small shared-file design offers no safe parallel authoring tasks. For US1, after T007, separate read-only invocations can validate the pure-transform examples and successful subprocess fixtures concurrently in separate temporary directories; do not concurrently edit tests/test_normalize_text.py. For US2, after T009, missing/directory cases and invalid-encoding cases may be run independently with isolated fixtures. These are validation examples, not parallel implementation labels; serial task execution remains the default.

## Implementation Strategy

Deliver T002–T007 first as the valid-input US1 MVP, then stop to run its independent tests. Complete T008–T009 for US2 before considering the feature's full rejection contract satisfied. Finish T010–T012 for combined evidence. Keep tests and implementation in the planned two files, avoid new frameworks, and preserve the nine human-approved policies. Successful automated checks provide implementation evidence; roadmap verification, Git integration and feature acceptance remain separate human decisions.

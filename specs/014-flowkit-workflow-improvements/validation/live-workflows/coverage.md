# Live Workflow Coverage

This matrix records the required T080–T089 live scenarios against their actual evidence. Pending and failed success scenarios remain required work. [The ledger](ledger.json) retains run IDs, findings, and retry chains; [the runbook](runbook.md) defines completion assertions.

## Contents

Use the matrix for scenario evidence and the later sections for retained trials and coverage limits.

- [Scenario matrix](#scenario-matrix)
- [Current limitations](#current-limitations)
- [Verified Closeout cases](#verified-closeout-cases)
- [Coverage boundaries](#coverage-boundaries)

## Scenario matrix

Each row identifies the actual required outcome and its independent coordinator audit.

| Task | Required scenario | Current result | Evidence |
|---|---|---|---|
| T082 | selection-success | passed after approved fixture metadata correction | [independent audit](select-feature/selection-success-retry-1/coordinator-audit.json) |
| T082 | selection-rejected | passed | [independent audit](select-feature/selection-rejected/coordinator-audit.json) |
| T082 | mapping-conflict | passed | [independent audit](select-feature/mapping-conflict/coordinator-audit.json) |
| T083 | authoring-success | passed after scoped author correction | [independent audit](specify/authoring-success-retry-2/coordinator-audit.json) |
| T083 | linkage-repair | passed | [independent audit](specify/linkage-repair/coordinator-audit.json) |
| T083 | linkage-conflict | passed | [independent audit](specify/linkage-conflict/coordinator-audit.json) |
| T084 | ambiguity-continuation | passed | [independent audit](clarify/ambiguity-continuation/coordinator-audit.json) |
| T084 | already-clean | passed | [independent audit](clarify/already-clean/coordinator-audit.json) |
| T084 | unresolved-answer-stop | passed | [independent audit](clarify/unresolved-answer-stop/coordinator-audit.json) |
| T085 | plan-success | passed | [independent audit](plan/plan-success/coordinator-audit.json) |
| T085 | review-correction | passed after checked sequencing retry | [independent audit](plan/review-correction-retry-1/coordinator-audit.json) |
| T085 | product-decision-stop | passed after explicit question-contract retry | [independent audit](plan/product-decision-stop-retry-1/coordinator-audit.json) |
| T086 | tasks-success | passed | [independent audit](tasks/tasks-success/coordinator-audit.json) |
| T086 | coverage-correction | passed after helper/driver correction | [independent audit](tasks/coverage-correction-retry-2/coordinator-audit.json) |
| T086 | design-gap-stop | passed | [independent audit](tasks/design-gap-stop/coordinator-audit.json) |
| T087 | closeout-success | passed | [Independent audit](closeout/closeout-success-retry-1/coordinator-audit.json) |
| T087 | debrief-correction | passed after exact finding handoff | [independent audit](closeout/debrief-correction-retry-1/coordinator-audit.json) |
| T087 | wiki-reconciliation | passed after strict initial retry | [independent audit](closeout/wiki-reconciliation-retry-1/coordinator-audit.json) |
| T087 | verification-rejected | passed | [independent audit](closeout/verification-rejected/coordinator-audit.json) |
| T088 | multiple-source-refresh | passed on final package | [independent final-package audit](wiki-lint-update/multiple-source-refresh-final/coordinator-audit.json) |
| T088 | already-clean | passed | [independent audit](wiki-lint-update/already-clean/coordinator-audit.json) |
| T088 | inconsistency-stop | passed | [independent audit](wiki-lint-update/inconsistency-stop/coordinator-audit.json) |
| T088 | age-only-no-progress | passed | [independent audit](wiki-lint-update/age-only-no-progress/coordinator-audit.json) |

## Current limitations

All 23 required live scenarios pass against current own workflow packages and controller 0.5.2. T080–T089 are delivered, with separate actual Analyze, Implement and Converge prerequisite evidence completing the ten-active-workflow inventory. [The final audit](completion-audit.json) binds scenario summaries, independent assertions, current source digests, 127-test success, eleven valid definitions and checksum-pinned install/refresh/remove. Twelve failed required attempts remain recorded, alongside an older passing Wiki run superseded by the final-protocol retry. These results establish the defined synthetic scenarios and coordinated recovery, not exhaustive branches, all standalone commands, native model/effort identity, unattended long-chat reliability, publication or real-feature acceptance.

The successful corrected selection retry independently verified exact approval, roadmap/pointer activation and no specification authoring. The first selection attempt stopped on incomplete synthetic roadmap metadata. Corrected baselines and dry-run-validated revised patches are prepared; those changed exact patch bytes now have direct supplemental human approval and the full selection retry passed independent live verification. The independent Select Feature mapping-conflict scenario passed with no mutation. Candidate inventory and approval handling observed in the failed selection run do not establish successful activation.

Historical Wiki failures remain recorded: missing fixture crosslinks, an inaccurate index report, and a forbidden route field on a complete outcome. Corrected fixtures and final source guidance have passed fresh real ingestions, independent reassessment, and terminal validation. The older successful 0.5.1-protocol retry remains historical evidence; the final 0.5.2 run supplies current-package coverage.

An earlier disposable-chat compaction reverted to a historical Analyze prompt. Coordinator steering stopped that early accidental preflight before any workflow step or feature correction. The current procedure uses one scenario per message, a durable coordination checkpoint, and scope inspection after compaction. Agent-capacity cleanup uses supported reversible archival of verified completed test children.

These results do not establish all FlowKit commands or all workflow branches as live-tested. Native model/effort identity introspection remains unverified. No release, Git integration, real roadmap verification, or feature acceptance follows from this phase.

The first Specify success attempt authored the exact target and verified linkage but failed the mandatory core quality checklist because the Specifier role prohibited its self-check. An extra quality review was retained as excluded evidence. Source Specifier, Planner, and Tasker instructions now distinguish required author checks from independent review, without changing workflow nodes or assignments. The fresh retry completed all 16 real author self-checks. Its independent brief found a nonempty-input newline rule error; a separately invoked, scoped Specify correction fixed both passages and added a distinguishing acceptance example. A fresh actual brief returned PROCEED with zero findings. The coordinator independently verified current packages, roles, core checklist, semantic correction, and protected bytes. Historical failures remain recorded.

The first Plan product-decision stop failed because the actual child omitted option descriptions. Strict validation rejected the request before downstream mutation. A fresh isolated trial explicitly relayed the existing question contract, produced a real valid unanswered question, and stopped with `human-input-missing`. Independent audit confirmed the preserved child, partial template, validation ordering, and protected bytes; no validator or package changed.

Tasks coverage correction passed after two failed trials were retained: an exact-restoration helper assertion and a task-row counter that included TOC links. The driver now allows safe command-local self-check correction before returning an author result while preserving strict controller gates. A fresh full trial executed two actual authors and independent reviews, handed off the exact finding, restored the original task coverage, and validated completion. The material upstream conflict case stopped on a valid real reconciliation question with no workflow artifact changes.

The separately coordinated T087 Analyze prerequisite completed cleanly on the synthetic task plan without artifact changes; its [independent audit](closeout/prerequisites/analyze/coordinator-audit.json) and baseline manifest are retained. At the baseline milestone, the approved initial local Git baseline recorded 21 allowlisted fixture files and an immutable OID while separately invoked implementation was still pending. Actual subsequent Implement and Converge completion is recorded below. Closeout lint-scope compatibility was corrected statically in package 0.6.5, pinned by bundle 0.13.7, with red/green path evidence, full127-test success and supported installation refresh. [The correction record](closeout-lint-scope-correction.json) left all four live Closeout cases pending at its static-only milestone. Earlier passing workflows retain identical workflow/protocol bytes.

## Verified Closeout cases

Actual Analyze, Implement and Converge prerequisites passed independent audits. The first Closeout success attempt correctly stopped on a synthetic specification status label before debrief or mutation; `F014-LIVE-SETUP-016` retains the failed run. A new fixture replaces only that test-input label with Draft and records the exact delta. Fresh Converge passed with 31 assertions and independently reviewed current evidence in run `6de0565b-96cf-4984-b673-18194a14cdd5`; its [coordinator audit](closeout/prerequisites/converge-draft-retry-1/coordinator-audit.json) confirms current Draft bytes, zero gaps and preserved implementation/task/Git state. Closeout retry completed successfully, including the exact lifecycle update, trusted debrief, independent review, approved patch, actual ingestion and clean full lint. Its [audit](closeout/closeout-success-retry-1/coordinator-audit.json) rechecks 40 native assertions, checkpoint digests and eleven transition-order assertions. Read-only compaction scope drift was recovered in the same running controller invocation. The remaining Closeout cases and final reconciliation are now independently audited below.

The [verification rejection audit](closeout/verification-rejected/coordinator-audit.json) confirms 51 native assertions, strict assessment envelopes and validation-before-transition ordering. The real gate chose `return-to-workflow`; specification lifecycle remains Complete, roadmap remains implemented, and writer/wiki/Git mutations did not occur. This intended stop passes the negative scenario. A coordinator audit helper was adjusted to distinguish the eight agent profiles from the larger protected digest map; native behavior and source packages were unchanged.

The first controlled debrief-correction case completed the real specification → plan → tasks waterfall and restored the exact pre-injection specification. Fresh analysis then found `I-802-TASK-INTRO`, an ambiguous generation-era statement about unchecked tasks. Strict eligibility correctly stopped before the confirming debrief, verification or wiki work. The [independent failure audit](closeout/debrief-correction/coordinator-audit.json) preserves 64 native assertions without counting this required success as passed. A pristine full retry supplies the exact prior finding to the actual Tasker reconciliation node for a narrow wording correction; task IDs, completed markers, implementation and source rules remain protected.

The [source continuity audit](source-continuity-audit.json) matches each passing run’s workflow and shared protocol to current source, and distinguishes executed from skipped roles using actual recovery steps. Four Wiki runs lack per-run raw role snapshots; their Reviewer/Wiki Curator definitions match the unchanged initial source baseline, while their native execution evidence remains separate. This limitation is not model/effort identity verification.

The [full correction retry audit](closeout/debrief-correction-retry-1/coordinator-audit.json) validates 84 native assertions and 31 independent checks. The first independent assessment retained both actual findings, entered the shared specification → plan → tasks waterfall, restored the exact specification and historicized only the task introduction. All twelve task entries and five planning artifacts were preserved. Fresh analysis and eligibility resolved both findings; a second debrief and distinct Code Reviewer confirmed readiness before the exact approved roadmap write. Real feature ingestion, full clean lint and fresh maintenance/readiness review reached the terminal report without Git integration or acceptance. The first failed attempt remains historical.

The first stale-source Closeout attempt stopped before mutation because its initial Reviewer returned `continue` with empty `remaining_ids`. The [failure audit](closeout/wiki-reconciliation/coordinator-audit.json) reproduces strict rejection and confirms all 180 starting files, installed packages and Git state stayed intact. A separate pristine retry relays the full existing assessment contract; the rejected output remains unchanged.

The final wiki retry required another coordinator scope recovery after compaction. This time the extra Analyze dispatch launched four probes and one analyzer execution child before interruption, and its main-task preparation/routes ran. Its [scope recovery record](closeout/wiki-reconciliation-retry-1-scope-recovery.json) distinguishes that incomplete, excluded dispatch from the selected Closeout run and verifies all 1,220 recorded parent files stayed unchanged. The interrupted analyzer is preserved; the same Closeout controller resumed at wiki pass two. These observations establish coordinated recovery, not unattended reliability of a long native chat or authorization for an extra phase.

The [final wiki reconciliation audit](closeout/wiki-reconciliation-retry-1/coordinator-audit.json) records 54 local checks, 33 independent coordinator checks and 15 distinct actual execution children. The authorized source overlay changed exactly two files and preserved 179 others at that boundary. Three modeled single-source ingestions refreshed S001, S002 and S003, with fresh full lint and independent assessments resolving actual stale-policy IDs and missing feature coverage before final readiness. Code, tests, completed task entries, design artifacts, source packages and Git state were preserved.

## Coverage boundaries

Defined synthetic success/correction/negative cases only; no exhaustive runtime branch or product-domain claim.

Named-role invocations and source continuity observed; native loaded-model/effort identity and optional visual desktop checks remain unavailable or unrun.

Four Wiki Lint Update runs omit per-run raw role snapshots; unchanged initial Reviewer/Wiki Curator baseline hashes and actual native execution are explicitly distinguished.

Long-chat compaction required coordinator scope recovery. The extra interrupted Analyze child in the final wiki case is excluded; all 1220 recorded historical parent files were unchanged. These results do not prove unattended native-chat reliability.

External-working-tree lifecycle suite was skipped because its optional source settings were unset; checksum-pinned initialized-consumer install/refresh/remove passed.

Deprecated Start Feature was not installed or invoked. Manual prompt paths and every workflow branch were not independently executed.

Standalone constitution, custom checklist, tasks-to-issues, roadmap-sync, wiki-init/query/status, feedback capture/report, and Mermaid rendering commands were not demonstrated as live skill invocations in T080–T089. No claim about earlier unrelated invocations follows.

Feature014 remains Draft and its roadmap remains in-progress; no main commit, push, release, real roadmap verification or acceptance occurred.

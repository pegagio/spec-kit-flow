# Data Model: Consumer Adoption Review

This feature uses Markdown documents rather than a database or runtime registry. Stable labels support review and future automation without treating a semantic conclusion as mechanically proven.

## Contents

The sections below provide the planning decisions and review details.

- [Consumer Context](#consumer-context)
- [Model Rule Matrix](#model-rule-matrix)
- [Adoption Proposal](#adoption-proposal)
- [Operator Decision](#operator-decision)
- [Adoption Review](#adoption-review)
- [Validation Record](#validation-record)
- [State Transitions](#state-transitions)

## Consumer Context

A review identifies one initialized consumer and one inspected project scope. Record a portable project identifier, designated integration branch, governance paths, active agent guidance paths, and why those guidance files apply to the selected feature work. Paths are project-relative. Include nested guidance or override rules that apply; an unexplained or conflicting authority chain prevents confirmation.

## Model Rule Matrix

Each rule has separate governance and active-guidance evidence cells. Each cell records `compatible`, `missing`, `conflicting`, or `uncertain`, a path and heading or line locator, and a brief semantic rationale. Equivalent or stricter wording counts only when it still satisfies the entire rule. Splitting a rule across several passages is allowed with citations to each.

| ID | Required meaning |
| --- | --- |
| M1 | Before integration, spec, plan, tasks, and implementation form one mutable change set. |
| M2 | Accepted behavior, technical approach, and work changes flow back to the corresponding artifacts and are reconciled across the set before proceeding. |
| M3 | Agents flag missing checks and unresolved divergence, recommend appropriate operator-invoked analysis/remediation, convergence, and pre-merge review, and do not invoke workflows or underlying commands independently. Known divergence blocks implementation/merge pending reconciliation or operator resolution. |
| M4 | Acceptance into the project's designated integration branch freezes feature meaning; editorial corrections cannot change semantics. |
| M5 | Later behavioral changes use a new feature directory and reference earlier materially amended, replaced, or depended-on features. |

README evidence may supplement context but cannot replace either required evidence column. The matrix must retain missing and conflicting cells; a list of only successful matches is insufficient.

## Adoption Proposal

The proposal holds the inspected baseline digests, each target path, exact before/after patch, affected rule IDs, rationale, and any required project amendment procedure. It identifies proposed additions separately from existing compatible text. A proposal never authorizes its own application.

## Operator Decision

Record `accept`, `decline`, or `defer`, the proposal identity/digest or exact reviewed scope, and any approved subset. Acceptance applies only to that proposal against its inspected baseline. Partial acceptance leaves unaccepted changes unapplied. Revisions to patch content or a changed baseline require review again. Decline/deferral does not mutate governance or agent guidance; writing a review record is separate evidence recording.

## Adoption Review

The worksheet contains consumer context, model/source revision or digest, rule matrix, proposed changes, operator decision, applied changes, final inspected file digests, outcome, remaining work, and evidence limits. Existing compliant projects may be assessed without an amendment: record that no change was needed and retain the inspection evidence. A result is scoped to its observed snapshot and does not persist as a permanent adoption flag.

| Outcome | Derivation |
| --- | --- |
| `confirmed` | Both columns are compatible for every rule, applicable guidance and integration boundary are established, and all required amendment/conflict decisions for any applied edits are recorded. |
| `partial` | Some required evidence is absent or incomplete, with no unresolved material conflict or uncertainty. Also covers a deferred missing-rule proposal. |
| `declined` | Operator explicitly declines the adoption proposal; report the decision and observed evidence without claiming adoption. |
| `unresolved` | A material conflict, uncertain compatibility, ambiguous boundary/authority, or changed proposal baseline remains unsettled. |

For deterministic reporting, an explicit decline takes precedence and retains conflicts in the matrix; otherwise unresolved evidence takes precedence over partial evidence, and only complete evidence permits confirmed. `defer` is a decision value, not an additional adoption outcome. State which missing or conflicting evidence makes a deferred review partial or unresolved.

## Validation Record

For each scenario, record its synthetic consumer ID, tested CLI version, installed component IDs/versions/digests, guide and template source coordinates/digests, setup state, exact decisions, observed result, applicable file hashes before and after, validation mode, and limitations. Expected results remain separate from observed results. Portable evidence excludes secrets, raw transcripts, and absolute host paths.

## State Transitions

The procedure moves through inspect → propose if needed → decide → apply accepted changes → reinspect → report. Already compatible state can move from inspect directly to report. Decline or deferral skips application. A baseline change returns to inspection. Refresh begins a new inspection; it never inherits confirmed state from an older worksheet. Package removal does not delete project-owned review records or adopted guidance.

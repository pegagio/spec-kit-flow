# Consumer Adoption Interface Contract

The interface is a reviewed runbook used by an operator or explicitly instructed agent. There is no adoption command, installed marker, or new workflow in this design. The runbook and worksheet are source documents supplied through the catalog source checkout.

## Contents

The sections below provide the planning decisions and review details.

- [Entry Points and Inputs](#entry-points-and-inputs)
- [Review and Mutation Contract](#review-and-mutation-contract)
- [Output Contract](#output-contract)
- [Refresh and Removal Contract](#refresh-and-removal-contract)
- [Acceptance Boundary](#acceptance-boundary)

## Entry Points and Inputs

Installation and refresh documentation link to `docs/consumer-adoption.md` after the component operation, explaining that adoption is a separate project decision. The runbook links to `docs/merge-bounded-flow-back.md` for reusable proposal wording and `docs/templates/adoption-review.md` for evidence output.

The invocation identifies the selected consumer, whether this is first adoption or reassessment, relevant guidance/governance paths, and a project-relative review output location. Unknown integration branch, applicable guidance, or governance authority is resolved from inspectable project evidence or a substantive operator answer. No default such as `main` or `develop` may silently establish the merge boundary.

An implementation-ready manual prompt must convey the following intent:

> Review this project's adoption of the Merge-Bounded Flow-Back model using the reviewed consumer-adoption runbook and worksheet. Inspect active agent guidance and governance, map every model rule to evidence, and preserve compatible project wording. Present exact proposed changes and obtain the required operator decisions before applying constitutional amendments or resolving material conflicts. Reinspect resulting state and report a bounded outcome. Flag and recommend missing FlowKit checks for separate operator invocation.

## Review and Mutation Contract

The agent may inspect and draft the proposal under the invocation. It must show all proposed changes before acceptance, cite existing compatible or conflicting text, and explain every required rule gap. An amendment follows the consumer's own governance procedure, including any required version/date handling. A missing constitution requires a proposed creation and explicit adoption decision, not silent generation during installation.

The decision records the exact patch or approved subset. Apply only accepted changes after confirming unchanged baselines. Preserve unrelated rules, local edits, components, and merged feature history. If applicability or semantics cannot be established, report the question with citations; do not reinterpret governance to fit the model. The runbook may recommend a separately invoked constitution or FlowKit workflow but cannot run it without operator instruction.

## Output Contract

The report uses the [data model](../data-model.md), including both evidence columns for M1–M5 and the separate decision/outcome fields. The implementation worksheet must provide empty fields and instructions, never prefilled claims of successful adoption. A compact illustrative result is:

```yaml
consumer: example-project
review_scope: repository-wide feature work
integration_branch: integration
operator_decision: defer
outcome: partial
remaining:
  - M5 is missing from active agent guidance
rule_evidence:
  M5:
    governance:
      status: compatible
      reference: .specify/memory/constitution.md#spec-evolution
      rationale: Later behavior changes require a new feature with historical links.
    active_guidance:
      status: missing
      reference: AGENTS.md#feature-work
      rationale: The inspected section does not address later behavioral changes.
```

This example is an excerpt, not a complete confirmed report. Actual reports include every rule, applicability evidence, baseline/final digests, proposal and decision details, provenance, and limitations. The final report explains remaining work and the smallest next operator action. It never treats installing the bundle, writing the report, or completing the procedure as proof of adoption.

## Refresh and Removal Contract

Refresh updates installed components through the normal catalog route and directs the operator to reassess project state. It does not overwrite project-owned guidance with newer proposal text. A prior report cannot silently carry forward its outcome. Removal preserves adopted project guidance, constitution, history, and adoption evidence because those files are outside package ownership.

## Acceptance Boundary

Automated checks may validate structure, citation presence, and preservation. They cannot decide semantic equivalence or prove live-agent compliance. Validation must separately demonstrate manual execution and the agent's pre-merge, post-merge, and missing-check behavior in a disposable consumer. Publication, general CLI compatibility, and adoption in other projects remain outside those observations.

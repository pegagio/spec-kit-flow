# Approved Roadmap Amendment for Feature 015

This records the operator-approved replacement applied to the Feature 015 entry in `.specify/memory/roadmap.md` version 1.14.0. The prior ledger called for a FlowKit role map and step → workflow → parent precedence. The approved direction names a native Codex agent on every delegated step. The operator subsequently approved corrections to the roadmap vision and cross-cutting C-02 summary; both are applied in the roadmap.

The later operator-approved version 1.14.1 amendment supersedes this document's separate per-launch announcement language. The current roadmap uses Codex native subagent activity and child-pane identity for launch visibility; the original replacement below remains as the review record for version 1.14.0.

## Replace the Feature 015 heading and bullets

Replace the existing `### 015 — Agent Roles and Assignment Inheritance  [status: planned]` heading and its bullets with:

> ### 015 — Named Agents for Delegated Steps  [status: planned]
>
> - **Description**: Let each explicitly delegated FlowKit workflow step name a consumer-configured Codex custom agent.
> - **Outcome**: Every delegated step names a reviewed agent; different steps may name different agents. Main-task steps and human gates stay in the driving task. Immediately before each child launch, the controller announces its step and agent name, adding model and reasoning effort when Codex exposes them.
> - **Scope (in)**: A fixed reviewed set of agent names; Specify-compatible per-step agent declarations; explicit delegation; native Codex custom-agent configuration; all-branch named-agent preflight; per-launch announcements; main-task and human-gate boundaries; disposable-consumer and native-runner validation.
> - **Scope (out)**: Feature 014 workflow changes and retrospective edits to verified Feature 013 artifacts.
> - **Depends on**: 013; no dependency on 014.
> - **Governed by**: C-02, C-03, C-04, C-05.
> - **Notes**: Architect, Builder, Coder, and Verifier are the reviewed names. Codex owns each agent's optional model and reasoning settings; Feature 015 must prove exact named dispatch in the supported client.

## Replace the Feature 015 open questions

Replace the four bullets under `Feature 015 must resolve these questions before its source changes are selected:` with:

> - Can the supported Codex client select a custom agent by exact name for each delegated child and confirm its instructions load?
> - How should a delegated step's agent name and explicit child marker be represented in Specify-compatible YAML while main-task steps remain in the driving task?
> - Can the controller validate every possible named child before workflow work and announce each actual child launch with model and effort when available?
> - Which named-agent behavior can native `specify workflow run` support, and how should any difference from the direct Codex controller be documented?

## Replace the roadmap sync impact report

Replace the current `SYNC IMPACT REPORT` comment with:

```text
<!--
SYNC IMPACT REPORT
==================
Version change: 1.13.0 → 1.14.0
Bump rationale: MINOR — revise planned Feature 015 to use per-step native Codex agents instead of a FlowKit role map.

Changes this revision:
  - Replaced the planned role map and three-level precedence with reviewed agent names on every delegated step.
  - Kept main-task steps and human gates outside child dispatch.
  - Added named-dispatch validation and per-launch agent announcements.

Specs affected: 015
Open questions added/resolved: four Feature 015 questions revised; Feature 014 questions remain open.

Notes: This prospective design change does not implement named-agent dispatch or amend Constitution II.
-->
```

Keep Feature 014 and all verified history untouched.

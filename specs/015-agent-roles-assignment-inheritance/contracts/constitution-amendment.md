# Proposed Constitution Amendment for Feature 015

The operator approved this amendment, and it was applied to `.specify/memory/constitution.md` on 2026-09-29. It changes only the assignment authority in Principle II; workflow and controller source remain unchanged.

## Assignment rule

In Principle II's first paragraph, replace the passage beginning “A reviewed workflow MAY declare a concrete model” and ending “MUST follow the declared or operator-overridden assignments” with:

> Every explicitly delegated workflow step MUST declare a reviewed Codex agent name. Naming an agent MUST NOT itself delegate a main-task step. Invocation authorizes those named assignments without a per-run agent, model, or effort override. A Codex controller MAY launch bounded step subagents and MUST follow the named assignments.

In the next sentence, replace “fallback model” with “fallback assignment.” Leave the rest of Principle II unchanged.

## Rationale

Replace Principle II's rationale with:

> **Rationale:** Reviewed agent names keep selection explicit while consumers configure those agents through Codex.

## Version and impact

The constitution changed from `4.0.0` to `5.0.0` with `Last Amended: 2026-09-29`. This major change replaces concrete workflow step models and per-run overrides with reviewed agent names. The sync impact report records Principle II, Feature 015, pending workflow/controller source, and aligned `AGENTS.md`; the ratification date and all other principles remain unchanged.

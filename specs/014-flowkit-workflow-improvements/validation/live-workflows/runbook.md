# Live Workflow Verification Runbook

This procedure implements T080–T089 under the operator-issued Codex goal. It coordinates separately invoked installed workflows in an isolated consumer; it does not extend any workflow's authority or bypass a human gate.

## Contents

- [Scope and prerequisites](#scope-and-prerequisites)
- [Scenario execution](#scenario-execution)
- [Correction and retry](#correction-and-retry)
- [Human decisions](#human-decisions)
- [Completion audit](#completion-audit)

## Scope and prerequisites

The source baseline is commit `4e442bd` plus attributable changes made under this goal. The source checkout is the correction authority. The disposable Codex chat is the live controller host. Keep its historical Feature 014 artifacts and runs intact; create distinct synthetic fixture directories and checkpoints for this phase.

Before each scenario, verify the installed workflow ID/version/digest, controller and command skill ownership manifests, compatible extensions, exact native assignments, active feature pointer, and scenario baseline. Use the supported development-snapshot installer for unreleased source. Do not rewrite installed definitions, substitute global skills, or treat an availability probe as execution evidence. Refresh only between terminal invocations, since an installation change during execution invalidates a run's boundary.

## Scenario execution

The coordinator sends one exact installed-skill invocation to the authorized disposable chat and waits on that chat's specific active turn. Observation timeouts are not workflow failures; inspect the same turn or run before considering a retry. Resume an interactive step's existing child with the attributable answer rather than launching a replacement child. Keep each scenario isolated and retain its failed runs as well as eventual successful reruns.

Dispatch one scenario per message. After any context compaction, verify the latest explicit coordinator request, current coordination checkpoint, selected workflow ID and fixture root before execution; a historical task title or initial prompt cannot silently substitute the old workflow. If scope drifts, stop before semantic work, preserve the accidental preflight, and relay a fresh exact scenario request. [The recovery record](coordination-recovery.json) documents an observed preflight-only correction.

Record portable evidence under this directory, grouped by workflow. Each scenario record contains a stable scenario ID, task ID, expected outcome, fixture identity, invocation prompt, source and installed versions/digests, run and step IDs, observed validated outcome, ordered loop passes, artifact before/after digests, exact independent assertions, finding IDs, correction coordinates, and retry links. Summaries exclude raw transcripts, secrets, and personal host paths. Local execution locations stay in temporary coordinator state; durable paths are relative to the source or fixture root.

Release completed test children between scenario invocations to prevent cumulative agent-capacity exhaustion. In this client, the disposable runtime exposes no close/retire tool and interrupting an idle child does not release capacity. The coordinator can obtain child thread IDs from typed app `subAgentActivity` records, verify each child's latest turn is completed and its state is idle/notLoaded with `read_thread`, then reversibly archive completed test children with `set_thread_archived`. One archived completed readiness child demonstrably permitted a fresh exact Wiki Curator launch; [the recovery record](capacity-recovery.json) preserves that evidence. Retain outputs and run summaries first. Do not archive an active child, a child awaiting substantive answers, or any child still needed for same-step continuation. If capacity fails, preserve the preflight stop, clean up only verified completed children, then separately retry; never substitute a role or count a failed probe as workflow work.

An expected success requires the declared workflow terminal result plus independent inspection of its durable outputs. A validated blocked assessment is a failed success scenario. An expected negative scenario passes only when the intended cause and bounded stop are observed and prohibited changes are absent. Checking YAML or constructing an outcome envelope without a live skill run cannot satisfy either case.

When delegating a potentially interactive command, relay the installed protocol’s structured question contract alongside the exact rendered command arguments. The child must return its actual question with the active step ID, custom-answer flag, and short-string options or objects containing nonempty `id` and `description`; a `label` alone is insufficient. Persist the exact returned request before validation. An invalid request stops the invocation; never invent options or answers, relax validation, or claim the expected human-input stop from a schema rejection. Correct the delegation context and separately retry the affected scenario.

Controlled defects must be introduced into synthetic input or authored artifacts at a documented boundary, with before/after digests and the real command output preserved. Do not change installed prompts, provide a fabricated assessment, suppress a prerequisite, or tell the reviewer to assert a finding irrespective of the evidence. The test observes whether the real author/reviewer correction path resolves the seeded defect.

Assessment routing follows the controller schema exactly. A `complete` envelope omits `next_step_id`, `gate_step_id`, and `resume_action`; a `continue` envelope includes only `next_step_id` targeting the declared loop body and identifies actual unresolved in-scope work in `remaining_ids`; pending lifecycle or maintenance work is not itself a product defect. An empty list cannot support continuation. Relay this requirement to the initial assessor as well as loop assessors. A `blocked` envelope includes only a stable `resume_action`. Clean findings do not excuse an invalid terminal envelope. Live verification must record the rejected run, correct ambiguous source guidance, and retry against refreshed source before claiming workflow success.

## Correction and retry

On routine failure, retain the run evidence, identify the smallest source defect, and add a meaningful regression assertion before correcting behavior. Reconcile the affected specification, plan, and tasks; change reviewed source, related version pins, manual guidance, and diagrams as needed. Run focused checks, refresh the consumer through the supported installer, verify installed/source digest equality, restore the affected fixture checkpoint without deleting historical evidence, then issue a separate invocation for the retry. Reuse existing finding IDs and remediation obligations rather than multiplying duplicate tasks.

Execute dependent helper operations sequentially with checked exit status. A failed checkpoint save or validation must prevent every following branch and terminal-status mutation. Preserve a premature terminal mutation as a failed required success attempt; repairing metadata afterward does not prove the original ordering. Separately retry the affected full scenario and retain an ordered validation/mutation trace.

Within an unfinished core command, the actual author may repair a routine helper or self-check mistake and rerun the corrected check before returning a valid command result. Preserve the failed diagnostic and successful recheck. A mechanical row-count or formatting assertion is not itself a substantive product blocker. This does not authorize downstream routing after a failed controller checkpoint or envelope validation, nor relabel a terminal failed run; those attempts require separate recovery or retry. Task-row checks must match checklist markers followed by stable task IDs, rather than counting table-of-contents links.

A changed shared controller requires retesting every affected live scenario, not merely the scenario that exposed it. A changed workflow package requires rerunning that workflow's required scenarios. Current-source coverage must identify the final installed digest for each passing run. Preserve exact implementation delta boundaries needed by Converge and debrief; install refresh is not itself proof of an attributable source delta.

Keep the outer goal active through recoverable failures and continue independent scenarios when another scenario waits on a decision. Record no-progress stops with the evidence, attempted corrections, and smallest supported recovery. Do not retry unchanged failures indefinitely or redefine the task to exclude a difficult scenario.

## Human decisions

Fixture construction, small typos, ambiguous test instructions, evidence collection, and routine source corrections are authorized by the operator's goal. Synthetic product defaults may be proposed during setup. Product answers and exact roadmap approvals used as live gate evidence require an attributable operator decision for the actual question or exact patch bytes. Present a concrete initial packet so those decisions can be recorded together and relayed when their gates occur. Approval remains valid only while its scoped inputs and patch bytes match. A changed consequential decision or major structural change returns to the operator; independent test work continues meanwhile.

No test grants authority to commit, push, release, verify the real project's roadmap, or accept Feature 014. A deliberately rejected or unanswered gate may prove its negative scenario but cannot satisfy a required success scenario.

## Completion audit

Before completing the goal, independently audit all T080–T089 deliverables and required scenarios against final source and installed digests. Require live success and negative-case evidence, artifact assertions, resolved defect/retest chains, current affected regression suites, the full available suite, source validation, relevant installation checks, and whitespace checks. Record genuinely skipped optional checks and untested branches separately; no required failed, skipped, or unverified scenario can be marked complete. Reconcile the coverage matrix, feature artifacts, and report while retaining historical records and their original limits.

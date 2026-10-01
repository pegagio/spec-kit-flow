# Feature 014 Workflow Review Baseline

This is the historical pre-change read-only first pass over the original eight source `workflow.yml` files. It records where the current graph reaches a conclusion, stops after one corrective step, or asks the operator to classify an outcome. It is evidence for the Feature 014 review, not an approved replacement design.

## Review lens

For each workflow, verify the success condition, every branch, the evidence used to route routine outcomes, the exact human decision gates, the continuation path after changed evidence, and a bounded stop for repeated findings or lack of progress. Test both the manual path and the direct Codex controller path. A workflow may finish without starting the next separately invoked phase.

## Baseline graph observations

| Workflow | Current route | Review target |
|---|---|---|
| Start Feature | `assess-eligibility` leads to an exact-patch gate, then roadmap write, wiki query, specification, brief, and final gate. The graph does not insert an explicit linkage repair between specification creation and brief. | Establish or safely stop on missing, stale, or conflicting `Spec dir` after the directory is known; preserve exact-patch approval and a reliable brief result. |
| Clarify | One `speckit.clarify` child leads to a human result gate; `continue-clarification` stops for another invocation. | Assess residual ambiguity from the current spec. Decide whether an operator's explicit choice to continue can repeat a bounded session inside the invoked workflow without launching Plan. |
| Plan | An unconditional readiness gate precedes planning. `return-to-clarification` runs one clarification child and has no route back to a refreshed readiness assessment or plan. | Replace the routine gate with evidence-based readiness; define a safe continuation after an in-scope correction and a specific stop for product decisions. |
| Tasks | Generation leads to a human coverage gate. `return-to-plan` runs one planning child and has no route back to regenerated or reassessed tasks. | Assess coverage automatically from reviewed design, continue routine in-scope correction from current evidence, and keep separate Analyze invocation. |
| Analyze and Remediate | A human gate classifies analysis. Each routine branch performs one artifact correction and one reanalysis, then ends regardless of the new result. | Classify inspectable routine findings, follow dependent artifact order, reassess until clean or a bounded stop, and keep consequential decisions with the operator. |
| Implement | A human gate classifies execution evidence. Return branches run one analysis, specification, planning, or task command and then end without completing dependent reconciliation or resuming eligible work. | Route from current evidence through dependent artifacts and analysis before eligible implementation resumes; stop on a real blocker or changed authority. |
| Converge | A human gate classifies convergence. Remediation runs one analysis child, then stops for separate Implement and later Converge. | Resolve the Constitution II / Feature 007 authority conflict, then define the approved bounded remediation loop and its progress measure. |
| Close Out | A human availability gate precedes completion. One debrief leads to an exact-roadmap-patch gate; a return choice stops instead of correcting routine findings and repeating debrief. | Recognize clear authorized completion evidence, reconcile routine debrief findings within scope, refresh evidence, repeat safely, and retain exact roadmap and Git gates. |

## Named-agent baseline

Every delegated step in current workflow source uses Architect, Builder, or Verifier; no workflow step currently uses Coder. The tracked `.codex/agents/coder.toml` is labeled a temporary named-agent launch probe, while this checkout has no Architect, Builder, or Verifier configuration file. Feature 015 reviewed Architect, Builder, Coder, and Verifier as the starting set. Feature 014 will review each step's assignment, establish usable consumer-owned configurations here for selected names, and propose any additional name only for a distinct reviewed responsibility. Native preflight must continue to stop when a required name is unavailable; bundle lifecycle must not take ownership of consumer agent files.

## Decisions needed before source changes

- Approve the exact F014 roadmap scope amendment that makes all eight workflow reviews and agent integration explicit.
- Resolve the prospective authority boundary for a Converge invocation that contains analysis, implementation, and reassessment without rewriting verified Feature 007 history.
- Set evidence, progress, repetition, and safe-stop rules for each proposed continuation loop.
- Review step-to-agent assignments and any additional name before it appears in workflow source or a production configuration.

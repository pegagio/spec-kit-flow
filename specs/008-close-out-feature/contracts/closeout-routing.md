# Closeout Routing Contract

`feature_context` identifies the converged feature. `completion_operation_status`, `roadmap_transition_decision`, and `commit_readiness_decision` are separate human gate inputs.

`operation-missing` and invalid completion choices stop. `operation-available` prompts for the separately approved completion operation, then runs `speckit.flow-roadmap.debrief`. Only `approve-patch` runs `speckit.flow-roadmap.write`, followed by curated `speckit.flow-wiki.ingest`, `speckit.flow-wiki.lint`, and a commit-readiness gate. `return-to-workflow`, `defer`, and invalid roadmap choices stop without a roadmap write.

No branch itself commits, integrates Git, or accepts project work. A ready disposition is a proposal for a separate explicit commit.

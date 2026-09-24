# Research: Start Eligible Feature

## Decision: Specify the existing reviewed package

The source workflow is `workflows/speckit-flow-start-feature/workflow.yml` version `0.2.0`. It assesses eligibility, obtains a human patch decision, applies only an approved patch, retrieves cited context, drafts a specification, runs a roadmap brief, and asks the operator for the next state. A retrospective specification should describe and verify this contract before proposing a source change.

**Rationale**: The project owns generic workflow source and keeps installed consumer copies operational only. This avoids inventing an alternative start process.

**Alternative considered**: Replace the workflow with a new implementation. Rejected because no concrete deficiency has been established.

## Decision: Validate authority and dispatch separately

Contract inspection can verify step ordering and gate options. The disposable lifecycle test can verify installation, provenance, and native resolution. Its no-op Codex route proves dispatch behavior only; a live consumer review remains a separate acceptance decision.

**Rationale**: The constitution requires evidence-bounded claims and explicit human authority.

**Alternative considered**: Treat a no-op agent result as acceptance. Rejected because it cannot show the quality of an actual agent's roadmap or specification decisions.

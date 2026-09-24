# Data Model: Start Eligible Feature

The workflow coordinates existing project artifacts; it introduces no new persistent entity.

| Concept | Required information | Ownership |
| --- | --- | --- |
| Feature candidate | Operator request, roadmap identity, eligibility, dependencies | Roadmap extension and operator |
| Proposed roadmap patch | Exact status change and evidence for approval | Roadmap extension; human approves |
| Governing context | Cited decisions, constraints, dependencies, coverage classification | Wiki extension |
| Feature draft | Specification and roadmap brief tied to the approved outcome | Spec Kit and roadmap extension |
| Operator decision | Patch verdict and final next-state choice | Human operator |

The roadmap patch transitions from proposed to applied only after approval. Amendment, context resolution, deferral, and invalid decisions stop the route without applying the proposed patch. The final next-state choice does not itself start another workflow.

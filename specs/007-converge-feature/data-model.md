# Data Model: Converge Feature

The workflow coordinates existing feature artifacts and implementation; it introduces no new persistent entity.

| Concept | Relevant information | Ownership |
| --- | --- | --- |
| Feature artifact set | Current specification, plan, and tasks | Consumer feature |
| Convergence assessment | Evidence of alignment or remaining gaps | Core `speckit.converge` |
| Remediation tasks | Bounded remaining work appended when gaps exist | Core command and consumer feature |
| Result disposition | Clean, remediation, or blocked | Human operator |

A clean result stops for separate closeout review. Remediation tasks must be analyzed before implementation and later reassessed. Blockers preserve evidence without claiming convergence.

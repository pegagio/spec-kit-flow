# Data Model: Implement Eligible Work

The workflow coordinates existing feature and code artifacts; it introduces no new persistent entity.

| Concept | Relevant information | Ownership |
| --- | --- | --- |
| Eligible task set | Remaining tasks and prerequisite state | Consumer feature |
| Execution evidence | Completed work, tests, discoveries, blockers | Current selected agent |
| Result disposition | Converge, return path, or blocked | Human operator |
| Flow-back target | Analysis, specification, plan, or tasks | Corresponding core command |

Execution evidence is reviewed before a route is chosen. A return route stops implementation and leaves dependent reconciliation to the normal feature flow. A convergence choice does not itself run convergence.

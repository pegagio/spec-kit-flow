# Data Model: Plan Implementation

The workflow coordinates existing consumer artifacts and introduces no new persistent entity.

| Concept | Relevant information | Ownership |
| --- | --- | --- |
| Clarified specification | Reviewed product intent and open decisions | Consumer feature |
| Readiness decision | Plan, return to clarification, or defer | Human operator |
| Planning artifacts | Plan, research, data model, contracts, quickstart | Core `speckit.plan` and consumer feature |

Planning artifacts may be created only on the `plan` route. The return route resumes clarification for the same feature; deferral and invalid decisions leave planning unstarted.

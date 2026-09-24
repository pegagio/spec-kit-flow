# Data Model: Generate Implementation Tasks

This workflow coordinates an existing feature artifact set and introduces no new persistent entity.

| Concept | Relevant information | Ownership |
| --- | --- | --- |
| Planned feature | Reviewed specification and design artifacts | Consumer feature |
| Task proposal | Dependency-ordered work and surprising human actions | Core `speckit.tasks` output |
| Review decision | Analyze, return to plan, amend tasks, or defer | Human operator |

Task generation creates a proposal before the review choice. The proposal becomes analysis-ready only when the operator chooses that route. Deferral does not erase the generated artifact or authorize implementation.

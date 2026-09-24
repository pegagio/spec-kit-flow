# Data Model: Analyze and Remediate Artifacts

The workflow coordinates an existing feature artifact set; it introduces no new persistent entity.

| Concept | Relevant information | Ownership |
| --- | --- | --- |
| Artifact set | Active spec, plan, and tasks | Consumer feature |
| Analysis report | Read-only findings and evidence | Core `speckit.analyze` |
| Disposition | Clean, routine artifact path, or consequential stop | Operator review gate |
| Flow-back chain | Ordered artifact updates followed by reanalysis | Workflow and core commands |

A routine specification change propagates through plan and tasks; a plan change propagates through tasks; a task change remains task-scoped. Each ends in a fresh analysis. Stop outcomes do not change the artifacts.

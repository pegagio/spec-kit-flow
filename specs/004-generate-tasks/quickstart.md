# Validation Guide: Generate Implementation Tasks

Use a disposable initialized Codex consumer with the pinned bundle and compatible Specify CLI. Record the CLI version, workflow source version and digest, and observed result.

1. Inspect `specify workflow info speckit-flow-tasks` and compare inputs and gate choices with [the contract](contracts/task-generation.md).
2. Run a no-op route with `task_review_decision=defer`. Confirm native completion and no implementation dispatch. The no-op executable does not generate a meaningful task proposal.
3. Inspect `analyze`, `return-to-plan`, amendment, and invalid routes in the YAML. Confirm analysis and implementation are separate operator actions.
4. In a separate human-reviewed consumer session, inspect real generated tasks for coverage, dependencies, and unexpected operator work before acceptance.

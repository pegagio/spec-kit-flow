# Optional Codex Desktop Checks

These checks are optional user-experience observations, separate from automated validation. Neither has been run in this session. Record operator observations below only after performing the check; do not treat expected results as observed evidence.

## Visible continuation

1. In a disposable initialized consumer with the development snapshot installed, invoke the Implement workflow for a feature with at least two eligible tasks.
2. Allow the controller to complete one implementation pass and reach its assessment.
3. Observe whether the controller continues when progress is evidenced and eligible work remains, then stops when the work is complete or precisely blocked.

**Expected result**: Existing eligible tasks continue through the declared bounded loop; no new workflow, planning, task generation, or goal wrapper is started. The final report identifies completion or the blocker and resume action.

**Operator observation**: Not run.

## Named-agent assignment and gate presentation

1. In the same disposable consumer, inspect a workflow with delegated steps and a main-task gate, such as Select Feature.
2. Confirm the delegated work presents its declared role name and that the selection gate remains a main-task interaction.
3. If the Codex client exposes actual subagent identity, compare it with the declared name; otherwise record the client limitation.

**Expected result**: The requested role is used without a silent fallback. The main-task gate remains visible and the child does not decide the operator's choice. Native live selection is not established by the repository's static validator.

**Operator observation**: Not run.

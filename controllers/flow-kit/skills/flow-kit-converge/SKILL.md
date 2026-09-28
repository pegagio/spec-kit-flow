---
name: flow-kit-converge
description: Assess implementation convergence and remaining gaps. Run the installed speckit-flow-converge workflow in this Codex task.
---

# FlowKit Converge

Run only the installed `speckit-flow-converge` workflow in the selected consumer project and current Codex task. Follow `.specify/flow-kit/controller-protocol.md` exactly. The installed workflow owns its prompts, commands, branch logic, and gates; do not duplicate them here or call `specify workflow run`. Start by validating the installed controller inventory and invoking `bash .specify/flow-kit/scripts/bootstrap.sh "$PWD" speckit-flow-converge flow-kit-converge` from the consumer project. Translate supplied workflow inputs to repeated `--input name=value` arguments and the optional single named-step model/effort override to repeated `--override name=value` arguments on the bootstrap command. Show the effective assignment table and stop before workflow execution if any input or model-effort pair is invalid or unavailable. Do not launch another workflow phase.

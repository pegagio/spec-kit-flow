---
name: flow-kit-select-feature
description: Choose and activate a roadmap feature without writing a spec. Run the installed speckit-flow-select-feature workflow in this Codex task.
---

# FlowKit Select Feature

Run only the installed `speckit-flow-select-feature` workflow in the selected consumer project and current Codex task. Follow `.specify/flow-kit/controller-protocol.md` exactly. The installed workflow owns its prompts, commands, branch logic, and gates; do not duplicate them here or call `specify workflow run`. Start by validating the installed controller inventory and invoking `bash .specify/flow-kit/scripts/bootstrap.sh "$PWD" speckit-flow-select-feature flow-kit-select-feature` from the consumer project. Translate supplied workflow inputs to repeated `--input name=value` arguments. Review the returned `agent_assignments`, follow the named-agent dispatch procedure in the shared protocol, and stop before workflow work if a required agent cannot be confirmed. Do not launch another workflow phase.

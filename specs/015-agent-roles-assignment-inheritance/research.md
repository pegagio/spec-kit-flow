# Feature 015 Research: Native Codex Agents

These findings use the installed Specify CLI `1.0.10.dev0+pegagio.2`, current FlowKit source, Codex CLI 0.157.1, and [Codex's subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents). They establish a design, not live Feature 015 behavior.

## Decision: Name a native Codex agent on every delegated step

Codex loads standalone custom-agent TOML files from `.codex/agents/` or `~/.codex/agents/`. Each requires `name`, `description`, and `developer_instructions`; model and reasoning effort are optional native settings. The `name` field identifies the agent. A configured custom-agent model or effort can take precedence over spawn defaults. Feature 015 therefore places an exact agent name on every delegated step and leaves model and effort resolution to Codex. The reviewed names are Architect, Builder, Coder, and Verifier.

**Rationale**: Consumers can choose agent behavior without a FlowKit role map or duplicated model settings. **Alternatives considered**: A FlowKit role-to-pair map was rejected by the operator as duplication. A workflow-level default and steps without agent names were also rejected; requiring a name on each delegated step makes its selection explicit. The operator declined a temporary per-run substitution.

## Decision: Keep delegation separate from assignment

Feature 013 used a concrete step `model` as both a model selection and a child-dispatch marker. Feature 015 replaces that marker with `flow_kit.delegated: true` on executable child steps, paired with `flow_kit.agent`. An executable step without the marker runs in the main task and has no agent name. Gates and switches always stay in the main task. The migrated packages loaded in a disposable consumer with Specify `1.0.10.dev0+pegagio.2`, and the controller returns per-step named assignment intents. Loader preservation does not establish native runner named-agent semantics.

## Decision: Use native subagent visibility

Codex's native subagent activity shows when a probe or workflow child starts. The controller supplies a task label containing the intended agent name, and the child pane may show model and reasoning effort. The observed pane does not have a separate native-agent-name field; the operator accepted the task label as the launch indication. The exact native `agent_type` request and successful probe establish selection separately from the label. Missing model or effort display does not block launch. All-branch preflight still checks names before workflow work.

## Open validation gate: Native dispatch integration

Operator-provided Codex desktop screenshots show a child titled `Coder` loading distinctive instructions from its project TOML. With model and effort omitted, the UI showed the parent's reported `GPT-6 Sol · Medium`; after the file specified `gpt-6-luna` and `high`, the child returned the changed instruction marker and the UI showed `GPT-6 Luna · High`. The operator accepted these screenshots as sufficient for T004; see [validation.md](validation.md). Current Codex documentation says a direct app request can spawn subagents and identifies custom agents by their TOML `name`. The procedure in [controller-protocol.md](../../controllers/flow-kit/controller-protocol.md) uses that native orchestration path and requires confirmation through the exact native request and readiness probe. The in-session collaboration tool and Codex CLI 0.157.1 probes did not select the custom agent, so those are documented limits, not substitutes. The two-consumer dispatch, malformed and absent definitions, unavailable model, same-child continuation, and edit behavior after preflight are recorded in [validation.md](validation.md). Feature 015 adds no watcher for configuration changes.

## Governance and compatibility

Constitution II requires reviewed agent names on delegated steps and excludes per-run overrides. The [constitution amendment](contracts/constitution-amendment.md), Feature 015 [roadmap amendment](contracts/roadmap-amendment.md), and subsequent approved C-02 correction are applied. Workflow metadata, controller preflight, and the direct Codex dispatch procedure are implemented. A native `specify workflow run` attempt reached a Codex prompt and failed because the temporary consumer was not trusted; it did not establish native named-agent dispatch behavior. The manual-prompt fallback remains available.

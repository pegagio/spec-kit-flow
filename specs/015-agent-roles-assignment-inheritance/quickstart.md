# Quickstart: Validate Feature 015 Named Agents

This is the live Codex runbook for Feature 015. The repository-side setup is already prepared for this session; the operator actions are limited to opening the prepared projects in Codex, starting the named FlowKit skill, answering its human gates, and reporting what the UI shows. Do not use native `specify workflow run` for these scenarios: it did not reach a delegated step in the recorded probe.

T012's two-consumer named-agent and native UI visibility check, T016's mixed-boundary continuation check, and T022's negative cases are complete. Their steps below are retained for reproduction, not a request to rerun them.

## What is prepared

Two disposable Specify consumers were initialized, installed from the current development snapshot, and given different project agent files. Both have the same `speckit-flow-analyze-remediate` workflow bytes (`dc04d2e27b314420bc81f55cab6226292f68478d62361647b5e9d3775cc3f6ab`), Specify CLI `1.0.10.dev0+pegagio.2`, and FlowKit bundle `0.4.1`. Each has project agents named Architect, Coder, and Verifier. Each consumer now also has a root `.mise.toml` pin for `pipx:specify-cli` at `1.0.10.dev0+pegagio.2`; this lets FlowKit bootstrap resolve the Specify executable from the selected project runtime.

| Consumer | Architect | Verifier | Coder |
|---|---|---|---|
| A | No model or effort set; distinctive `CONSUMER_A_ARCHITECT` instruction | No model or effort set; distinctive `CONSUMER_A_VERIFIER` instruction | No model or effort set; distinctive `CONSUMER_A_CODER` instruction |
| B | `gpt-6-luna`, `high`; distinctive `CONSUMER_B_ARCHITECT_LUNA_HIGH` instruction | `gpt-6-sol`, `high`; distinctive `CONSUMER_B_VERIFIER` instruction | No model or effort set; distinctive `CONSUMER_B_CODER` instruction |

I’ll provide the two temporary project paths in chat. Do not install anything or edit the agent files for the first scenario. If reproducing this setup later, use the checked-in fixtures under `tests/consumer-fixtures/named-agents/consumer-a/.codex/agents/` and `consumer-b/.codex/agents/`; initialize each consumer with Specify, then use the development-snapshot install route in [installation.md](../../docs/installation.md#install-in-another-project).

## T012: Run the same workflow in both consumers

Run the steps once in consumer A and then in consumer B. Use a fresh Codex task for each consumer so it loads the current project-scoped `.codex/agents/` configuration. Consumer A's test instructions were revised after the first two attempts; do not continue inside either earlier task.

1. In Codex, open the consumer path I provide as a project and start a new task in that project.
2. Invoke the installed skill exactly as follows:

   ```text
   $flow-kit-analyze-remediate feature_context=015-validation-smoke-test
   ```

3. Let FlowKit complete preflight. For every no-work probe, inspect Codex's native subagent activity for a task label containing the intended agent name and the child reply for the fixed readiness token. The label is a launch cue; the exact native agent request and successful probe establish selection. The test agents return their consumer-specific markers only for delegated workflow steps.
4. If the workflow proceeds to `analyze-artifacts`, inspect the native Verifier child. This is a delegated workflow step, not a readiness probe. In consumer A, inspect the child pane for the exact reply `CONSUMER_A_VERIFIER`; in consumer B, inspect it for `CONSUMER_B_VERIFIER` and, when Codex exposes them, `GPT-6 Sol · High`. The parent’s summary may call this reply a fixture token without printing it, so record the child’s exact text.
5. The fixture agents intentionally return markers instead of running the analysis command. The marker is evidence of the project agent configuration, but it is not an analysis report. FlowKit should stop at `analyze-artifacts`, record `step-failed` with no changed files, and launch no remediation. This run does not reach the analysis gate; the separate T016 scenario tests main-task gates.
6. Repeat in the other consumer using a fresh Codex task. For consumer B, note Architect's preflight agent name and whether Codex displays its configured `GPT-6 Luna · High` settings. Consumer A's missing model/effort values should follow Codex's normal inheritance behavior.

For each consumer, report whether both probes appeared and returned their requested readiness tokens, the agent names and any model/effort shown by Codex, the work child’s exact marker, and the resulting `step-failed` stop with no file changes. A screenshot of the subagent pane is useful, but include the consumer name in your note so the two runs cannot be confused. If a named child or marker is missing, stop that run and report the UI state; do not retry with a different agent or an override.

## T016: Verify the main-task boundary and same-child continuation

The completed live test used a third disposable consumer with a test-only Specify overlay on the installed Clarify workflow. The overlay composes a main-task prompt, the delegated `clarify-specification` Architect command, a delegated Verifier prompt, and the original human gate and switch. The composed workflow digest is `85c8f3d53867a0325a9a1baa14b008b412c22f97e07d27abef51391ce15752b7`; the reviewed source workflow is unchanged. The Architect returned a structured question, then `CONTINUATION_RESUMED_A` after the answer reached the same child. The Verifier returned `T016_VERIFIER_COMPLETE`. The operator chose defer at the main-task gate, and the summary recorded `operator-deferred` with no changed files.

Open the prepared project path in a fresh Codex task and invoke:

```text
$flow-kit-clarify feature_context=015-continuation-test
```

Confirm that `record-validation-context` runs in the main task without a child and that Codex shows the delegated `clarify-specification` Architect child in native activity. The child should ask: “For this validation, should the parent record the answer as option A or option B?” **Pause before answering and tell me that the question is visible.** I will replace the disposable Architect TOML at that point to observe Codex's changed-during-run behavior. After I confirm the edit, answer `A` in the main task. Confirm that the answer is sent to the same child task and that its result begins `CONTINUATION_RESUMED_A`. The delegated `verify-relay-result` Verifier child should then return `T016_VERIFIER_COMPLETE`. The workflow presents its clarification-result gate in the main task; choose **defer** to stop safely. Report the visible child names, question and answer relay, gate ownership, and markers. Do not edit the test files yourself.

## T022: Verify preflight failures and configuration changes

The source controller's six static negative cases and three native missing-file, malformed-file, and unavailable-model cases were checked without starting workflow work. A refreshed missing-file rerun confirmed that the final diagnostic includes the exact affected step ID. The test consumers stay isolated from the two completed T012 consumers.

The cases are:
- A delegated step has no agent name.
- A step uses an unsupported name or a case-mismatched name.
- Delegation metadata is malformed or placed on the wrong node.
- A delegated step still has a legacy concrete `model` field.
- A native agent configuration is missing, malformed, or unavailable.
- An invalid agent appears only in an untaken branch.
- The consumer's agent configuration changes after preflight while a run is waiting at a human boundary.

For each preflight failure, confirm that the diagnostic identifies the affected step and reason, no workflow child performs work, no run/recovery record is created, and no fallback agent is selected. For the changed-during-run case, report exactly when the file changed and what the active run did. Feature 015 specifies documenting the observed behavior; it adds no watcher or special stop rule. I’ll perform the file edits and restoration. Your part is to start the prepared run, tell me when it reaches the indicated point, and report the Codex behavior.

## Reproducing the consumer setup

Run these commands from the Spec Kit Flow source checkout only when you need new disposable consumers. Snapshot installation is for temporary test consumers; do not use it for normal release installation.

```sh
specify_bin="$(mise which specify)"
temp_root="$(python3 -c 'import tempfile; print(tempfile.gettempdir())')"
consumer_a="$(mktemp -d "$temp_root/flowkit-015-a.XXXXXX")"
consumer_b="$(mktemp -d "$temp_root/flowkit-015-b.XXXXXX")"

for consumer in "$consumer_a" "$consumer_b"; do
  git -C "$consumer" init -q
  (cd "$consumer" && "$specify_bin" init --here --force --non-interactive --integration codex --integration-options="--skills")
  cat > "$consumer/.mise.toml" <<'EOF'
[tools]
"pipx:specify-cli" = "1.0.10.dev0+pegagio.2"
EOF
  mise install -C "$consumer"
done

cp -R tests/consumer-fixtures/named-agents/consumer-a/.codex "$consumer_a/"
cp -R tests/consumer-fixtures/named-agents/consumer-b/.codex "$consumer_b/"
PATH="$(dirname "$specify_bin"):$PATH" python3 tools/catalog.py install "$consumer_a" --development-snapshot
PATH="$(dirname "$specify_bin"):$PATH" python3 tools/catalog.py install "$consumer_b" --development-snapshot
```

Check that both consumers have the same workflow bytes and that the expected agents are present:

```sh
shasum -a 256 \
  "$consumer_a/.specify/workflows/speckit-flow-analyze-remediate/workflow.yml" \
  "$consumer_b/.specify/workflows/speckit-flow-analyze-remediate/workflow.yml"
find "$consumer_a/.codex/agents" "$consumer_b/.codex/agents" -maxdepth 1 -name '*.toml' -print
```

Record the source revision, Specify CLI version, Codex desktop version if available, workflow digest, consumer name, and observed UI result in [validation.md](validation.md). Do not record absolute temporary paths in the durable validation record; I’ll map the reported consumer labels to the prepared paths in this session.

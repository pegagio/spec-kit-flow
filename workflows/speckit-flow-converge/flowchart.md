# Converge workflow flowchart

This diagram maps every step ID in [workflow.yml](./workflow.yml) to its execution path. Each node shows its exact step ID, assigned agent in parentheses when present, and command when present.

The dark Start circle marks workflow entry. Rectangles are prompt steps, diamonds are switch steps, the hexagon is the do-while loop, and rounded nodes are command steps. Dashed outlines mark delegated steps.

```mermaid
flowchart TD
    start((Start))
    loop{{"convergence-remediation-loop<br/>condition: assess-convergence state == continue<br/>max_iterations: 6"}}
    converge(["append-task-remediation<br/>(Architect)<br/>command: speckit.converge"])
    assess["assess-convergence<br/>(Verifier)"]
    correctionRoute@{ shape: diam, label: "route-convergence-correction" }
    prepare["prepare-convergence-flowback"]
    specRoute@{ shape: diam, label: "route-specification-remediation" }
    spec(["reconcile-convergence-specification<br/>(Architect)<br/>command: speckit.specify"])
    planRoute@{ shape: diam, label: "route-plan-remediation" }
    plan(["reconcile-convergence-plan<br/>(Architect)<br/>command: speckit.plan"])
    tasksRoute@{ shape: diam, label: "route-task-remediation" }
    tasks(["reconcile-convergence-tasks<br/>(Architect)<br/>command: speckit.tasks"])
    analyze(["analyze-remediation-tasks<br/>(Verifier)<br/>command: speckit.analyze"])
    eligibility["assess-remediation-eligibility<br/>(Verifier)"]
    implementRoute@{ shape: diam, label: "route-remediation-implementation" }
    implement(["implement-remediation<br/>(Builder)<br/>command: speckit.implement"])
    report["report-convergence-outcome"]

    start --> loop
    loop -- first or next convergence check --> converge --> assess --> correctionRoute
    assess -- controller stops for no progress or cap --> report
    correctionRoute -- continue --> prepare --> specRoute
    correctionRoute -- complete --> loop
    correctionRoute -- needs-human --> loop
    correctionRoute -- blocked --> loop
    specRoute -- run --> spec --> planRoute
    specRoute -- skip --> planRoute
    planRoute -- run --> plan --> tasksRoute
    planRoute -- skip --> tasksRoute
    tasksRoute -- run --> tasks --> analyze
    tasksRoute -- skip --> analyze
    analyze --> eligibility --> implementRoute
    implementRoute -- continue --> implement --> loop
    implementRoute -- complete --> loop
    implementRoute -- needs-human --> report
    implementRoute -- blocked --> report
    loop -- clean, blocked, or required input --> report

    classDef delegated stroke:#4b5563,stroke-width:2px,stroke-dasharray:6 4
    class converge,assess,spec,plan,tasks,analyze,eligibility,implement delegated
    style correctionRoute stroke-dasharray:0
    style specRoute stroke-dasharray:0
    style planRoute stroke-dasharray:0
    style tasksRoute stroke-dasharray:0
    style implementRoute stroke-dasharray:0
    style start fill:#111827,stroke:#111827,color:#ffffff
```

Every pass starts with `speckit.converge`. It checks current implementation and records remaining work under its append-only contract. The assessment classifies that fresh report and the controller checks progress and the correction limit before entering the waterfall. The first report establishes the gap baseline; subsequent reports must prove resolution of a prior gap.

Corrections enter the shared waterfall at specification, plan, or tasks as needed; implementation-only gaps skip all three stages. Fresh task analysis and eligibility verification precede implementation. Successful implementation returns directly to `speckit.converge`. Eligibility `complete` only means no eligible task work and still returns for fresh convergence; eligibility blockers or required operator decisions stop immediately through the outcome report. Failed commands, unresolved implementation blockers, invalid actions, and stale evidence also stop before further work.

Six total passes allow five corrections and a final convergence check. A clean sixth check succeeds; unresolved findings at that check stop before a sixth correction. Empty top-level branches reach loop exit without another command invocation. The controller stop edges show its declared routing policy in addition to YAML branch joins. One final report handles all outcomes; Close Out remains separately invoked.

# Implement workflow flowchart

This diagram maps every step ID in [workflow.yml](./workflow.yml) to its execution path. Each node shows its step ID, its assigned agent in parentheses when present, and its command when present.

The dark Start circle marks workflow entry. Rectangles are `prompt` steps, diamonds are `switch` steps, the hexagon is the `do-while` step, parallelograms are `gate` steps, and rounded nodes are command steps. A dashed outline marks `flow_kit.delegated: true`. The correction loop permits at most five passes in one invocation.

```mermaid
flowchart TD
    start((Start))
    assess["assess-implementation<br/>(Verifier)"]
    routeInitial@{ shape: diam, label: "route-initial-implementation" }
    completeInitial["implementation-complete-stop"]
    loop{{"implementation-correction-loop<br/>condition: reassess-implementation state == continue<br/>max_iterations: 5"}}
    gateInitial[/"implementation-consequential-gate"/]
    decisionInitial["stop-after-initial-implementation-decision"]
    blockedInitial["implementation-initial-blocked-stop"]
    invalidInitial["implementation-initial-invalid-state-stop"]

    before["reassess-implementation-before-pass<br/>(Verifier)"]
    routePass@{ shape: diam, label: "route-implementation-pass" }
    selectFlowback@{ shape: diam, label: "select-implementation-flowback" }

    specify(["remediate-implementation-specification<br/>(Architect)<br/>command: speckit.specify"])
    replanSpec(["replan-after-implementation-specification<br/>(Architect)<br/>command: speckit.plan"])
    retaskSpec(["retask-after-implementation-specification<br/>(Architect)<br/>command: speckit.tasks"])
    analyzeSpec(["analyze-after-implementation-specification<br/>(Verifier)<br/>command: speckit.analyze"])
    implementSpec(["implement-after-implementation-specification<br/>(Builder)<br/>command: speckit.implement"])

    plan(["remediate-implementation-plan<br/>(Architect)<br/>command: speckit.plan"])
    retaskPlan(["retask-after-implementation-plan<br/>(Architect)<br/>command: speckit.tasks"])
    analyzePlan(["analyze-after-implementation-plan<br/>(Verifier)<br/>command: speckit.analyze"])
    implementPlan(["implement-after-implementation-plan<br/>(Builder)<br/>command: speckit.implement"])

    tasks(["remediate-implementation-tasks<br/>(Architect)<br/>command: speckit.tasks"])
    analyzeTasks(["analyze-after-implementation-tasks<br/>(Verifier)<br/>command: speckit.analyze"])
    implementTasks(["implement-after-implementation-tasks<br/>(Builder)<br/>command: speckit.implement"])

    analyzeFirst(["analyze-before-implementation-resumes<br/>(Verifier)<br/>command: speckit.analyze"])
    implementAfterAnalysis(["implement-after-analysis<br/>(Builder)<br/>command: speckit.implement"])
    implementEligible(["continue-eligible-implementation<br/>(Builder)<br/>command: speckit.implement"])
    unknownFlowback["implementation-unknown-flowback-stop"]

    after["reassess-implementation<br/>(Verifier)"]
    routeFinal@{ shape: diam, label: "route-final-implementation" }
    completeFinal["implementation-executed-stop"]
    gateFinal[/"implementation-final-consequential-gate"/]
    decisionFinal["stop-after-final-implementation-decision"]
    blockedFinal["implementation-final-blocked-stop"]
    boundedFinal["implementation-loop-bounded-stop"]
    invalidFinal["implementation-final-invalid-state-stop"]

    start --> assess
    assess --> routeInitial
    routeInitial -- complete --> completeInitial
    routeInitial -- continue --> loop
    routeInitial -- needs-human --> gateInitial
    gateInitial -- defer, escalate, or abort --> decisionInitial
    routeInitial -- blocked --> blockedInitial
    routeInitial -- default --> invalidInitial

    loop -- first pass or continue within limit --> before
    before --> routePass
    routePass -- complete --> after
    routePass -- needs-human --> after
    routePass -- blocked --> after
    routePass -- default --> after
    routePass -- continue --> selectFlowback

    selectFlowback -- remediate-implementation-specification --> specify
    specify --> replanSpec --> retaskSpec --> analyzeSpec --> implementSpec --> after
    selectFlowback -- remediate-implementation-plan --> plan
    plan --> retaskPlan --> analyzePlan --> implementPlan --> after
    selectFlowback -- remediate-implementation-tasks --> tasks
    tasks --> analyzeTasks --> implementTasks --> after
    selectFlowback -- analyze-before-implementation-resumes --> analyzeFirst
    analyzeFirst --> implementAfterAnalysis --> after
    selectFlowback -- continue-eligible-implementation --> implementEligible
    implementEligible --> after
    selectFlowback -- default --> unknownFlowback

    after --> loop
    loop -- complete, needs-human, blocked, no progress, or limit reached --> routeFinal
    routeFinal -- complete --> completeFinal
    routeFinal -- needs-human --> gateFinal
    gateFinal -- defer, escalate, or abort --> decisionFinal
    routeFinal -- blocked --> blockedFinal
    routeFinal -- continue --> boundedFinal
    routeFinal -- default --> invalidFinal

    classDef delegated stroke:#4b5563,stroke-width:2px,stroke-dasharray:6 4
    class assess,before,specify,replanSpec,retaskSpec,analyzeSpec,implementSpec,plan,retaskPlan,analyzePlan,implementPlan,tasks,analyzeTasks,implementTasks,analyzeFirst,implementAfterAnalysis,implementEligible,after delegated
    style routeInitial stroke-dasharray:0
    style routePass stroke-dasharray:0
    style selectFlowback stroke-dasharray:0
    style routeFinal stroke-dasharray:0
    style start fill:#111827,stroke:#111827,color:#ffffff
```

The initial assessment can stop before correction. Within the loop, a `complete`, `needs-human`, `blocked`, or default result from `route-implementation-pass` skips correction and reaches `reassess-implementation`, as the empty YAML branches specify. A selected correction route reconciles the smallest affected artifact path and runs fresh analysis before implementation where tasks changed. The loop stops on a fresh complete or blocked result, a consequential decision, no progress, or the five-pass cap. Converge remains a separately invoked workflow.

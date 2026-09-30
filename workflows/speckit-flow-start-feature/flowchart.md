# Start Feature workflow flowchart

This diagram maps every step ID in [workflow.yml](./workflow.yml) to its execution path. Each node shows its exact step ID, assigned agent in parentheses when present, and command when present.

The dark Start circle marks workflow entry. Rectangles are prompt steps, diamonds are switch steps, parallelograms are human gates, and rounded nodes are command steps. Dashed outlines mark delegated steps.

```mermaid
flowchart TD
    start((Start))
    n01["list-roadmap-options<br/>(Architect)"]
    n02[/"select-roadmap-feature"/]
    n03@{ shape: diam, label: "route-feature-selection" }
    n04(["retrieve-governing-context<br/>command: speckit.flow-wiki.query"])
    n05["assess-eligibility<br/>(Architect)"]
    n06@{ shape: diam, label: "route-start-readiness" }
    n07[/"approve-roadmap-patch"/]
    n08@{ shape: diam, label: "route-roadmap-decision" }
    n09(["apply-approved-roadmap-patch<br/>command: speckit.flow-roadmap.write"])
    n10(["draft-specification<br/>(Architect)<br/>command: speckit.specify"])
    n11["assess-created-spec-linkage<br/>(Verifier)"]
    n12@{ shape: diam, label: "route-created-spec-linkage" }
    n13[/"review-spec-dir-patch"/]
    n14@{ shape: diam, label: "route-spec-dir-patch-decision" }
    n15(["apply-approved-spec-dir-patch<br/>command: speckit.flow-roadmap.write"])
    n16["verify-repaired-spec-linkage<br/>(Verifier)"]
    n17["prepare-start-outcome"]
    n18@{ shape: diam, label: "route-start-outcome" }
    n19(["brief-against-roadmap<br/>(Verifier)<br/>command: speckit.flow-roadmap.brief"])
    n20["report-start-feature-outcome"]

    start --> n01
    n01 --> n02
    n02 --> n03
    n03 -- default --> n04
    n04 --> n05
    n05 --> n06
    n06 -- ready --> n07
    n07 --> n08
    n08 -- approve --> n09
    n09 --> n10
    n10 --> n11
    n11 --> n12
    n12 -- repairable --> n13
    n13 --> n14
    n14 -- approve-exact-patch --> n15
    n15 --> n16
    n03 -- defer --> n17
    n12 -- linked --> n17
    n16 --> n17
    n14 -- amend --> n17
    n14 -- defer --> n17
    n12 -- conflict --> n17
    n12 -- ambiguous --> n17
    n08 -- amend-roadmap --> n17
    n08 -- resolve-context --> n17
    n08 -- defer --> n17
    n06 -- needs-human --> n17
    n06 -- blocked --> n17
    n17 --> n18
    n18 -- ready-for-brief --> n19
    n19 --> n20
    n18 -- needs-human --> n20
    n18 -- blocked --> n20
    n18 -- deferred --> n20

    classDef delegated stroke:#4b5563,stroke-width:2px,stroke-dasharray:6 4
    class n01,n05,n10,n11,n16,n19 delegated
    style n03 stroke-dasharray:0
    style n06 stroke-dasharray:0
    style n08 stroke-dasharray:0
    style n12 stroke-dasharray:0
    style n14 stroke-dasharray:0
    style n18 stroke-dasharray:0
    style start fill:#111827,stroke:#111827,color:#ffffff
```

The first step displays available roadmap entries, blocked unfinished work, simple dependency chains, immediate unlock counts, and distinct downstream dependents. The selection gate waits for one exact entry or defer; an optional feature request never selects automatically. Dynamic gate choices come from the completed inventory. No safe candidates means only defer is offered.

Only an explicit selection reaches governing context retrieval and eligibility assessment. Only a ready result reaches exact roadmap patch approval. Both already-linked and successfully-repaired paths join at `prepare-start-outcome`; a repair requires exact patch approval and fresh linkage verification. Deferral, missing context, conflicting or ambiguous linkage, or an unsuccessful recheck skips the shared brief. One final report presents successful artifacts or the exact stop reason. No next workflow is invoked. Invalid choices, missing outputs, and command errors stop before further mutation under controller rules.

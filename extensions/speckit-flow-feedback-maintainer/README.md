# Spec Kit Flow Feedback Maintainer Intake

This component is installed only in the Spec Kit Flow maintainer environment. Consumer projects receive `flow-feedback` capture/report only and must transfer reports through a human-approved handoff.

Intake validates a report's schema version, report integrity digest, component ID/version/digest, required redaction boundary, and duplicate relationship. A valid unique report is copied into `feedback/inbox/` and receives a reviewable triage record in `feedback/triage/`. A duplicate keeps the prior record relationship rather than creating a second proposed source change.

Each triage record records the report ID and digest, component coordinates, disposition, rationale, status, and next action. A disposition is never an implementation: the next action for a source refinement is an ordinary Spec Kit Flow specification, planning, task, and implementation proposal.

# Data Model: Maintainer Feedback Intake

The existing JSON records remain the persistence contract.

| Entity | Relevant fields | Ownership |
| --- | --- | --- |
| Transferred report | Schema, report ID, observations, component coordinates, integrity digest | Consumer handoff |
| Inbox copy | Canonical accepted report | Maintainer repository |
| Triage proposal | Intake ID, time, digest, component coordinates, disposition, rationale, next action | Maintainer repository |
| Duplicate relationship | Repeat triage ID and `duplicate_of` original ID | Maintainer repository |

The validator rejects nonportable report and triage text before creating either record. Existing records are not rewritten.

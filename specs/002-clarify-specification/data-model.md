# Data Model: Clarify Specification

The workflow coordinates an existing active specification and introduces no new persistent entity.

| Concept | Relevant information | Ownership |
| --- | --- | --- |
| Active specification | Requirements, open questions, accepted answers | Consumer feature |
| Clarification session | One bounded interaction and incremental edits | Core `speckit.clarify` command |
| Session result | Resolved, outstanding, deferred ambiguity | Core command and workflow review gate |
| Operator decision | Continue, begin planning, or defer | Human operator |

An accepted answer updates the active specification during the session. The result can lead to another session, planning readiness, or deferral only through an explicit operator choice. None of those choices launches another workflow.

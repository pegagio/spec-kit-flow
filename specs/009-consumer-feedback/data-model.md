# Data Model: Consumer Feedback

The existing extension retains its JSON contracts; no migration is needed.

| Entity | Required content | Persistence |
| --- | --- | --- |
| Observation | ID, time, component ID/version/digest, integration, consumer reference, execution profile, expected and observed behavior, safety response, fallback status, evidence references, target, disposition | One canonical JSON line in consumer journal |
| Journal | Ordered observations with unique IDs | Consumer-owned JSONL |
| Report | Producer, report ID, time, observations, integrity digest | Operator-selected JSON file |
| Projection | Readable view of the same report | Operator-selected Markdown file |

Validation rejects nonportable values before capture and again before export. An accepted report remains evidence, not a source change.

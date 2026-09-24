# Data Model: Bundle Catalog and Lifecycle

| Entity | Relevant fields | Ownership |
| --- | --- | --- |
| Bundle manifest | Bundle ID/version, integration, exact extension and workflow versions | Generic composition source |
| Release catalog | Status, component versions, source commits/tags, archive names/checksums, workflow digests | Maintainer catalog |
| Package archive | Deterministic runtime files under one extension root | Maintainer catalog |
| Consumer bundle record | Installed component ownership and versions | Consumer Specify state |
| Consumer feedback journal | Local observations retained across bundle removal | Consumer |

The bundle does not own component behavior or the consumer journal. A local catalog release does not publish to a remote service.

# Maintainer Intake Validation Contract

Intake accepts a transferred JSON report, supported disposition, rationale, and receipt time. It checks the full consumer observation shape, prefixed report integrity digest, component provenance with prefixed or bare SHA-256 digest, duplicate observation IDs, nonempty evidence references, and sensitive content. Absolute host paths after punctuation and `file://` URLs are rejected even if the report digest is valid. Rationale and receipt time pass the same sensitive-content check before persistence.

A first accepted report produces one canonical inbox copy and one triage proposal. Repeated report digests produce a duplicate triage record linked to the original and no new inbox copy. Rejected input writes neither record.

The triage proposal does not approve or edit source. Accepted changes return through specification, planning, tasks, and implementation under ordinary human gates.

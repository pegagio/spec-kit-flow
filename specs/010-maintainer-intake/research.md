# Research: Maintainer Feedback Intake

## Decision: Align the path boundary

The maintainer validator still uses the earlier path pattern and can accept a recomputed report digest with an embedded host path. Use the consumer source's corrected pattern so both transfer ends enforce the same portable-content boundary.

**Rationale**: Intake is an independent trust boundary; a valid digest proves bytes were not altered after export, not that content is safe.

## Decision: Validate written operator text

The current intake checks that `rationale` and `received_at` are nonempty, then stores them in a triage record. Apply the existing sensitive-content validator before any record is written. Keep the current disposition enum and record format.

**Alternative considered**: Sanitize by deleting matched text. Rejected because silent edits would obscure the maintainer's evidence and rationale.

## Decision: Match the consumer report schema

The consumer exporter writes every required observation field and permits a bare or `sha256:`-prefixed component digest. The current intake checks only five observation fields and requires the prefix. Validate the complete exported observation shape and accept both component digest forms while keeping the report integrity digest prefixed.

**Rationale**: A report with a valid recomputed digest can still be incomplete; a valid consumer export should not fail merely because of its supported digest spelling.

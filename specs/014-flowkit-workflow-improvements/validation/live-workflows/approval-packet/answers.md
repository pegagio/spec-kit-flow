# Proposed Fixture Approval Packet

All choices below are proposals. No approval has been recorded or consumed. Approval applies only to synthetic consumers and the exact matching question or patch bytes.

## Product and target choices

Select **802 — Normalize Text**; 801 is the verified prerequisite, 803 remains blocked on 802, and 804 is an eligible alternative. Author a Python standard-library CLI and function for one local text file. Do not add batch processing, packaging, network access, or dependencies.

Proposed answers for separately presented matching clarification questions:

1. Input is exactly one file path; no stdin mode.
2. Decode strict UTF-8; preserve Unicode without Unicode normalization.
3. Strip only ASCII spaces and tabs at each line edge.
4. Preserve interior whitespace and every logical blank line, including trailing blank lines.
5. Convert CRLF and bare CR to LF.
6. Empty input yields empty output. For nonempty input, add a terminating LF only if the normalized output does not already end with LF; preserve all existing trailing LF characters.
7. Output goes to stdout; never modify the input file or write another output file.
8. Missing files, directories, and invalid UTF-8 exit 2, emit concise stderr, and emit no stdout.
9. No size limit is imposed for this tiny local fixture.
10. Tests use Python unittest and cover each rule and errors.

These answers support more than five significant ambiguities, but do not predetermine what the real Clarify skill will ask or prove that a second session occurred. Relay only an approved answer that matches the actual question. The unresolved-answer scenario intentionally supplies no answer and must preserve the pending question.

## Proposed exact roadmap patches

The patch files are proposed, unapplied, and use fixture-relative paths:

- **selection.patch**: Assign the unmapped 802 entry to `specs/802-normalize-text/`; preserve its planned status and every other entry. Activation changes only the active pointer, after approval. Mapping and pointer activation explicitly preserve `planned` status until authoring; selection does not imply authoring or implementation.
- **linkage-repair.patch**: The same exact mapping correction from a separately reset missing-linkage fixture with an active 802 pointer.
- **verification.patch**: Change only 802 from implemented to verified, conditional on the actual debrief proposing precisely that before/after state and independent completion evidence. Approval cannot substitute for evidence.

Reject/defer scenarios deliberately withhold or reject the applicable gate choice; a coordinator must obtain an attributable decision rather than invent it. A conflict fixture adds a competing entry mapped to 802 and has no approved repair. If a live proposed patch differs, this packet does not authorize it.

## Curated source access

Approve only `docs/normalization-contract.md` (S001), `docs/error-contract.md` (S002), and, for Closeout after creation, `specs/802-normalize-text/` as local wiki sources. No remote URLs. Approve copying these fixture choices into the synthetic source contracts after the human decision. The two baseline wiki pages intentionally contradict their registered sources; their construction is test input, not an ingestion result.

## Controlled scenario construction

Approve isolated fixture variants, checkpointed before use: missing/competing roadmap linkage; explicit product ambiguities; deletion of one Plan deliverable after its authoring node and before Reviewer dispatch; removal of one required task after Tasker authoring and before Reviewer dispatch; an unresolved product/design question; one routine synthetic debrief discrepancy; stale registered wiki claims; and an unresolved wiki authority conflict. Inject only fixture artifacts at the declared boundary. Never alter installed workflow packages, outcomes, or approval records. The coordinator must retain before/after digests and independently verify the resulting real correction or bounded stop.

## Explicit fixture lifecycle

The baseline roadmap now defines readiness and status transitions. Planned entries require all prerequisites verified; terminal and already-active entries are excluded. Mapping/pointer activation keeps planned until actual specification authoring. Implemented requires attributable implementation/debrief evidence; verified additionally requires exact operator patch approval. The current patch hashes supersede the retained earlier preparation versions. No proposal is approved.

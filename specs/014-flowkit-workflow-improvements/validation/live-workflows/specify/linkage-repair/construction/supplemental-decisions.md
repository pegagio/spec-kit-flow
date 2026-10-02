# Supplemental Disposable Test Decisions

This packet supplies narrowly scoped decisions required by the remaining live verification scenarios. It is proposed and unapplied; approval affects synthetic fixtures only.

## Corrected roadmap amendments

Approve the exact [selection patch](schema-repair/selection.patch), [linkage repair patch](schema-repair/linkage-repair.patch), and conditional [verification patch](schema-repair/verification.patch). These retain the previously chosen Feature 802 and add required roadmap version and synchronization bookkeeping. Verification still requires actual implementation completion and a trustworthy clean debrief. The previous packet does not approve these changed bytes.

- **selection.patch SHA-256**: `a69df484c7035fba0b7048886c00aa0d497cb244870774b3750b09fe7d38b8d5`.
- **linkage-repair.patch SHA-256**: `a69df484c7035fba0b7048886c00aa0d497cb244870774b3750b09fe7d38b8d5`.
- **verification.patch SHA-256**: `d74991737e3a184e3aee61624112bd296b355373c75096001a9311da4ccc12d3`.

## Initial Git baseline

Authorize one initial local Git baseline commit in the disposable Closeout prerequisite consumer, after real Plan and Tasks creation and before its actual Implement invocation. All Closeout variants will inherit that same baseline. This is needed because the installed roadmap debrief requires an immutable Git baseline; the existing fixtures have no HEAD.

The explicit baseline allowlist is `.gitignore`, `.specify/feature.json`, `.specify/memory/constitution.md`, `.specify/memory/roadmap.md`, `docs/`, `wiki/`, and `specs/801-text-foundation/` plus `specs/802-normalize-text/`. Include only actual existing fixture artifacts at the checkpoint; preserve their hashes and record the resulting OID. Exclude installed skills, agent configurations, installed controller/workflow packages, test evidence, recovery runs, caches, secrets, and any real-project files. Use fixture-local Git identity `pegagio` and `pegagio@users.noreply.github.com`, and commit message `Synthetic Normalize Text baseline`. Record the exact pre-commit manifest and baseline OID in portable verification evidence.

No later implementation commit, main-project commit, push, release, or acceptance is authorized. Actual implementation remains an attributable baseline-to-WORKTREE delta. Do not create an implementation claim in this initial checkpoint.

## Deliberate negative gate choices

For the isolated Select Feature rejection scenario, choose the actual defer/no-selection option (or reject its proposed selection amendment, if that is the applicable modeled gate), retaining the exact presented choice. Do not activate another feature or change the roadmap/pointer. This decision applies only to that named negative scenario.

For the isolated Closeout verification-rejected scenario, reject the exact proposed verification amendment even if its positive-case counterpart is approved. Preserve implementation and any prior authorized artifact changes, keep the roadmap unverified, and stop before wiki maintenance as required by the actual workflow. This decision applies only to that named negative scenario; it does not override the evidence-conditional positive verification approval.

## Scope

Relay these decisions only at matching real modeled gates with recorded human provenance. Changed patch bytes, new product choices, material authority changes, or broader Git actions require a new decision. The real Feature 014 roadmap and Git history remain outside this packet.

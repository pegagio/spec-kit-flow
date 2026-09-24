# Validation Guide: Start Eligible Feature

Use an initialized disposable Codex consumer with the pinned bundle components and a compatible Specify CLI. Record the CLI version, bundle and workflow versions, source digest, and observed result. Do not use a production roadmap for these scenarios.

1. Inspect `specify workflow info speckit-flow-start-feature` and confirm the input and gate options match [the contract](contracts/start-feature.md).
2. In a consumer fixture with one eligible roadmap feature, run the workflow with `feature_request` set. Confirm that assessment proposes an exact patch while the roadmap remains unchanged. Approve the patch and observe context retrieval, specification creation, roadmap brief, and a final human choice without automatic follow-on dispatch.
3. Repeat with ambiguous eligibility, an unmet dependency, incomplete wiki coverage, a non-approval decision, and an invalid decision. Confirm each stop route preserves unapproved state and provides the reason or manual fallback.
4. Run `python3 -m unittest discover -s tests -p test_bundle_lifecycle.py` with the required local roadmap and wiki source inputs. A skipped test is not a pass. This test verifies installation and a no-op deferred start route, not live-agent judgment or the approved route.

Review the created consumer artifacts and source package together before marking the feature accepted.

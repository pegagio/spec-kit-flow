# Validation Guide: Bundle Catalog and Lifecycle

1. Confirm clean tagged Roadmap `v0.2.1` and Wiki `v2.0.1` checkouts, committed feedback `0.2.1` source, and Specify `1.0.10.dev0+pegagio.2`.
2. Run the existing catalog builder with those checkouts. Inspect release metadata, archive contents, checksums, and workflow hashes before treating the local catalog as released.
3. Run `$HOME/.codex/venvs/skill-tools/bin/python -m unittest discover -s tests -p 'test_catalog.py'` and the focused feedback suites.
4. Run the disposable bundle lifecycle suite with `SPEC_KIT_FLOW_TEST_ROADMAP_SOURCE` and `SPEC_KIT_FLOW_TEST_WIKI_SOURCE`. Confirm two non-skipped tests pass.
5. Install and refresh the release into a temporary consumer through `tools/catalog.py`; inspect the bundle record and installed feedback version. Remove the bundle and confirm consumer-owned feedback and unrelated components survive.

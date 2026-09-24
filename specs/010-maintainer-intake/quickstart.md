# Validation Guide: Maintainer Feedback Intake

1. Run `$HOME/.codex/venvs/skill-tools/bin/python -m unittest discover -s extensions/speckit-flow-feedback-maintainer/tests -p 'test_*.py'` from the repository root.
2. Verify valid intake, bare component digest acceptance, incomplete-observation rejection, tampered-report rejection, embedded-path rejection, sensitive-rationale rejection, and duplicate relationship behavior.
3. Run the disposable bundle lifecycle suite with local roadmap and wiki sources. Its maintainer intake uses a temporary root and does not install this component in the consumer.
4. Inspect the existing `feedback/inbox/` and `feedback/triage/` records read-only; do not rewrite historical evidence.

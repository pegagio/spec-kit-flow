# Validation Guide: Consumer Feedback

1. Run `$HOME/.codex/venvs/skill-tools/bin/python -m unittest discover -s extensions/flow-feedback/tests -p 'test_*.py'` from the repository root.
2. Confirm a valid capture and report round trip, duplicate rejection, embedded absolute-path rejection, and allowed relative and HTTPS references.
3. Run the disposable bundle lifecycle suite with local roadmap and wiki sources. Its installed `flow-feedback` archive remains `0.2.0` until the bundle-catalog feature rebuilds it.
4. Compare the source extension version and digest with the pinned catalog coordinates before claiming consumer availability.

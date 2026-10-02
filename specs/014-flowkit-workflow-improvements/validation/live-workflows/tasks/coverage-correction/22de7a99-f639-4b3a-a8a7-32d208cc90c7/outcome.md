# T086 coverage-correction failed trial

Run stopped with `step-failed` at pass 2 `generate-tasks`. The actual Tasker failed `assert repaired==original` before the write because insertion blank-line placement differed. The subsequent read-only inverse-removal assertion passed; tasks remain the exact injected artifact. Missing US2 T008/T009 coverage is unresolved. No pass 2 success checkpoint, Reviewer, assessment or terminal success was produced.

The first recovery stop attempt omitted JSON stdin and exited 1; execution stopped, then the corrected stop call with empty JSON stdin succeeded. The preceding incomplete-step update succeeded before the run stop.

After compaction, a wrong-scope parent Analyze bootstrap inspect was attempted. It executed no workflow steps, dispatched no children, created no run and performed no refresh or correction. The older parent installation is not current scenario source authority. See scope-drift.json for proof and its inventory limitation. No retry is authorized by this evidence collection.

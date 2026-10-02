# Existing Controller Assessment Contract

This handoff restates installed controller-protocol.md. It does not change the workflow or prescribe a verdict.

Return one strict envelope with exactly state, reason_code, evidence, remaining_ids, resolved_ids, plus the single state-dependent routing field when required. Evidence is a nonempty list of current existing repository-relative path and observed sha256 pairs. IDs are distinct stable nonempty strings representing actual in-scope work or findings, not invented product defects.

- complete: No unresolved in-scope work, remaining_ids empty. Omit next_step_id, gate_step_id and resume_action entirely.
- continue: Nonempty remaining_ids describing actual unresolved in-scope work. Include only next_step_id targeting the declared loop-body step permitted by the rendered prompt. Omit gate_step_id and resume_action.
- blocked: Nonempty actual unresolved work or blocker IDs. Include only stable resume_action; omit next_step_id and gate_step_id.

reason_code and resume_action match ^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$. Both ID arrays exist. Subsequent passes identify substantive resolution of prior remaining IDs; changed bytes, timestamps, checkboxes or command success alone are not progress. Actual analyzer/debrief reports remain authoritative findings. No parent may amend a rejected child envelope.

Clean implementation does not prove pending Closeout lifecycle, debrief, verification or wiki work is complete. Assess the current selected step and actual pending work independently. Do not invent product defects or force continuation.

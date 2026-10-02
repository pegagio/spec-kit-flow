# Approved Synthetic Normalization Contract

Strip ASCII spaces and tabs from each line edge; preserve interior whitespace and every logical blank line, including trailing blank lines. Convert CRLF and CR to LF. Empty input produces empty output. For nonempty input, add a terminating LF only if the normalized output does not already end with LF; preserve all existing trailing LF characters. Unicode is preserved without normalization. These synthetic fixture choices were approved by the operator; see `.flowkit-test/operator-decisions.json`.

## Unresolved equal-authority error policy

Invalid UTF-8 exits 1 and emits partial stdout. This conflicts with the equally authoritative error contract; no precedence rule or operator resolution exists.

# Data Model: Normalize Text

All entities are transient values. There is no persistence schema or migration.

## Entities and Relationships

| Entity | Fields | Validation and relationship |
|---|---|---|
| Input request | `path`: one local path string | Exactly one argument; no stdin sentinel or output destination |
| Input bytes | `content`: byte sequence | Read from request path without modification; missing/directory/read failures become rejection |
| Input text | `text`: Unicode string; `was_empty`: original emptiness | Strict UTF-8 decoding; preserves Unicode code points and canonical form |
| Normalized result | `text`: Unicode string; `encoded`: UTF-8 bytes | Produced from input text by FR-003–FR-006; emitted only after complete success |
| Input rejection | `category`: read or encoding failure; `diagnostic`: concise text; `status`: 2 | stderr diagnostic, zero stdout; no stored record |

## State Transitions

A request moves through argument validation → byte read → strict decode → normalization → UTF-8 encode → stdout emission → success status 0. Argument, read or decode failure moves to diagnostic emission → status 2 without result emission. This is control flow, not a durable state machine.

Normalization changes CRLF and CR to LF, trims ASCII spaces/tabs at each line edge and preserves all LF separators, including trailing empty segments. It retains interior whitespace, non-ASCII whitespace and decomposed Unicode. Original empty input produces empty output; original nonempty input gains a final LF only when its normalized result lacks one. No explicit length validation applies.

## Invariants

Input bytes never change. Output bytes are deterministic for the same input bytes. Rejected decoding never emits a prefix. Successive normalization is idempotent, including whitespace-only and terminal blank-line cases. [CLI examples](contracts/cli.md#exact-examples) define the observable values.

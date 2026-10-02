# Data Model: Normalize Text

The feature has only ephemeral processing values; no database or persistence schema is required.

## Values and Relationships

| Value | Fields | Validation and relationship |
| --- | --- | --- |
| Invocation | One path argument | Exactly one path; no stdin source. Produces an input read or rejection. |
| Input text | Original bytes, decoded text, original-empty flag | Strict UTF-8; original-empty derives from the actual input, not trimmed output. |
| Normalized result | Unicode text, UTF-8 bytes | Only CRLF/CR to LF and space/tab line-edge removal; preserve Unicode, interior spacing and all empty segments. |
| Input rejection | Category, diagnostic, status 2 | Specified failures: missing path, directory, invalid UTF-8. Diagnostic goes to stderr and stdout remains empty. |

## Processing States

Invocation → read bytes → strict decode → normalize separators → trim edges → final-LF check → UTF-8 stdout → success status 0. Argument/read/decode rejection terminates through stderr/status 2 before publishing stdout. No state mutates the source file or creates another output file.

The normalization keeps blank segments, including trailing ones. Empty original input exits the transformation as empty. Nonempty original input gains one LF only when the transformed result does not already end in LF. No explicit input-size validation exists.

## Contract Examples

| Input text | Result text |
| --- | --- |
| `" a  b \r\n\r\n"` | `"a  b\n\n"` |
| `"a\rb"` | `"a\nb\n"` |
| `""` | `""` |
| `" \t"` | `"\n"` |
| `"a\n\n"` | `"a\n\n"` |

Non-ASCII whitespace remains, decomposed Unicode remains decomposed, and interior tabs/spaces remain. See [CLI contract](contracts/cli.md) for observable channels.

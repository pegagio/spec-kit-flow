# CLI Contract: Normalize Text

The proposed public command is `python normalize_text.py PATH`. This interface design introduces no packaging, installed executable, stdin mode or additional options.

## Invocation and Channels

Exactly one positional file path is required. Success exits 0 and writes normalized UTF-8 bytes to stdout, with empty stderr. The input remains byte-for-byte unchanged; no output file is created. Use `--` before a path beginning with a dash. Standard argparse help and argument-count validation are CLI mechanics; invalid arity exits 2 on stderr.

Missing paths, directory paths and invalid UTF-8 each exit 2, emit a concise category diagnostic on stderr and emit zero stdout bytes. Diagnostics need not have a fixed literal wording, but must identify the failure category. Other OS read failures follow the same channel/status pattern. There is no fallback decoding or product input-size threshold.

## Normalization Rules

Decode strictly as UTF-8 and preserve Unicode without normalization. Convert CRLF to LF, then remaining CR to LF. Trim only ASCII space and tab at each line edge; preserve interior whitespace, other Unicode characters and every blank line, including trailing blank lines. Empty input stays empty. Nonempty original input receives a final LF only if the normalized result lacks one; existing trailing LFs remain intact.

## Exact Examples

The strings below use escape notation; stdout contains the corresponding actual UTF-8 bytes.

| Input | Stdout |
|---|---|
| `" a  b \r\n\r\n"` | `"a  b\n\n"` |
| `"a\rb"` | `"a\nb\n"` |
| `""` | `""` |
| `" \t"` | `"\n"` |
| `"a\n\n"` | `"a\n\n"` |
| `"\u00a0e\u0301\u00a0"` | `"\u00a0e\u0301\u00a0\n"` |

The final example retains non-ASCII edge whitespace and decomposed Unicode. An invalid UTF-8 sequence anywhere in a file yields the rejection contract, including when preceded by valid text.

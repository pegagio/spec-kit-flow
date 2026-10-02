# CLI Contract: Normalize Text

The planned interface is `python3 normalize_text.py PATH` from the consumer root. It accepts exactly one file path; zero or multiple positional paths fail with status 2, stderr diagnostics, and empty stdout. It never consumes stdin and provides no output-file or mutation option. A shell-quoted path containing spaces is one argument.

## Success

A readable file is decoded strictly as UTF-8. CRLF and bare CR become LF; only ASCII spaces and tabs are removed from each line edge. Interior whitespace, other Unicode whitespace, Unicode composition, and all blank lines including trailing ones remain intact. Empty input yields empty output. Nonempty input receives one terminating LF only when transformed output lacks one. UTF-8 bytes are emitted on stdout, status is 0, stderr is empty, and input bytes remain unchanged. No explicit product size limit is imposed.

## Exact Examples

The quoted strings below express text with escaped control characters; output comparisons must use actual bytes.

| Input | Stdout |
|---|---|
| `" a  b \r\n\r\n"` | `"a  b\n\n"` |
| `"a\rb"` | `"a\nb\n"` |
| `""` | `""` |
| `" \t"` | `"\n"` |
| `"a\n\n"` | `"a\n\n"` |
| `"\u00a0e\u0301\u00a0"` | `"\u00a0e\u0301\u00a0\n"` |

## Rejection

Missing paths, directories, and invalid UTF-8 each produce status 2, diagnostic text on stderr, and zero stdout bytes. Other read errors use the same channel/status policy. Complete decode and transformation precede output so a decoding failure cannot leak partial normalized text. Diagnostic wording is not prescribed; no traceback or input contents are required. Host resource exhaustion is a documented operational limitation rather than a product size restriction.

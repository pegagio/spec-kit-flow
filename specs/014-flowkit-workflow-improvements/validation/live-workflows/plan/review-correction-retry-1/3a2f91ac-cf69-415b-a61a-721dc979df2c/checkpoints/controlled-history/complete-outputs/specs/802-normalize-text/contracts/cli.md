# CLI Contract: Normalize Text

This design exposes a local command through the proposed future script `normalize_text.py`.

## Invocation and Channels

`python3 normalize_text.py FILE`

Exactly one positional file path is accepted; stdin is not an input source. Argument validation rejects missing or extra path arguments with status 2 and stderr diagnostics. Paths containing spaces are passed as one quoted argument. Successful invocation returns status 0 and UTF-8 bytes on stdout, with no input mutation or other output file.

## Normalization

Strictly decode UTF-8 and preserve every Unicode character without Unicode normalization. Convert CRLF and bare CR to LF. Remove only ASCII spaces and tabs at each line edge, preserving interior whitespace and all blank lines, including trailing ones. Empty input yields empty output. For nonempty input, add a terminating LF only when normalized output lacks one; retain existing trailing LF characters. There is no explicit product input-size limit.

Exact text examples: `" a  b \r\n\r\n"` → `"a  b\n\n"`; `"a\rb"` → `"a\nb\n"`; `""` → `""`; `" \t"` → `"\n"`; `"a\n\n"` → `"a\n\n"`. Non-ASCII whitespace and decomposed Unicode are retained. Output uses binary UTF-8 bytes so host newline translation cannot alter the contract.

## Rejections

| Category | Status | stdout | stderr |
| --- | --- | --- | --- |
| Missing path | 2 | Empty | Diagnostic identifying missing input |
| Directory | 2 | Empty | Diagnostic identifying invalid file input |
| Undecodable UTF-8 | 2 | Empty | Diagnostic identifying decoding failure |

Diagnostic wording is not fixed by the specification; tests assert category/channel rather than an invented literal message. Other read failures follow the same status/channel convention as an adapter design decision. Read and decode complete before successful output, preventing partial stdout for these input failures. No input content is copied into diagnostics.

## Repeatability and Authority

Repeated invocation with identical input yields identical output bytes and status. FR-001–FR-009 and accepted operator answers in [specification](../spec.md) govern this contract. This document records a design, not executable implementation or acceptance.

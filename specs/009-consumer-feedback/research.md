# Research: Consumer Feedback

## Decision: Tighten the existing path check

The current `ABSOLUTE_PATH` pattern recognizes a leading slash or one preceded by whitespace or quotes. It misses `Location:/Users/example/...` and `(/private/...)` in free text. Match a slash at the beginning or after a non-path character, while excluding URL separators and relative-path prefixes.

**Rationale**: Keep the current validator structure and close a narrow privacy leak without parsing arbitrary prose as a filesystem path.

**Alternatives considered**: Ban every slash, which would reject valid relative references and URLs; add a broad sanitizer, which could silently alter evidence. Both were rejected.

## Decision: Preserve release separation

Increment the source extension to `0.2.1`. The existing bundle still pins the released `0.2.0` archive. Record this distinction in validation and repackage source through the later bundle-catalog work, rather than silently treating a source test as an installed-package test.

# Synthetic Normalization Contract

These are the operator-approved decisions for the disposable Feature 802 normalization fixture.

Decode strictly as UTF-8 and preserve Unicode code points without Unicode normalization. Trim only ASCII spaces and tabs at each line edge. Preserve interior whitespace, every logical blank line and all trailing blank lines. Convert CRLF and bare CR to LF. Original empty input produces empty output. For originally nonempty input, add one final LF only when the normalized result lacks one; whitespace-only nonempty input therefore produces LF.

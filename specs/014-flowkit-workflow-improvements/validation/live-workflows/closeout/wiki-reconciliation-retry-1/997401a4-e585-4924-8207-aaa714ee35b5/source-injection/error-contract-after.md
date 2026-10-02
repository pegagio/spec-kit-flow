# Synthetic Input and Error Contract

These are the operator-approved decisions for the disposable Feature 802 normalization fixture.

Accept exactly one local file path and emit UTF-8 bytes to stdout. Do not read stdin, mutate the input or create an output file. Missing paths, directories and undecodable input fail with exit status 2, diagnostic text on stderr and no stdout. No explicit product size limit applies; full buffering can encounter ordinary environmental memory limits.

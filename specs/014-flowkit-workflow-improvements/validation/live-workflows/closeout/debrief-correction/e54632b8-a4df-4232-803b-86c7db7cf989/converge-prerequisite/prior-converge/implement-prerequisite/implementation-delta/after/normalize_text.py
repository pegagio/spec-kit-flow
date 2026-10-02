"""Normalize one UTF-8 file to stdout using only the standard library."""
import argparse
from pathlib import Path
import sys


def normalize(text):
    """Preserve Unicode and blank lines while normalizing newline/edge rules."""
    if not text:
        return ""
    result = "\n".join(line.strip(" \t") for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"))
    return result if result.endswith("\n") else result + "\n"


def main(argv=None):
    """Read exactly one path, decode completely, then emit UTF-8 bytes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    arguments = parser.parse_args(argv)
    try:
        text = Path(arguments.path).read_bytes().decode("utf-8", errors="strict")
    except FileNotFoundError:
        print("missing input path", file=sys.stderr)
        return 2
    except IsADirectoryError:
        print("input path is a directory", file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print("input is not valid UTF-8", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"input read failed: {error.strerror or error}", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(normalize(text).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

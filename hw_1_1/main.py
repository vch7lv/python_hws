#!/usr/bin/env python3
import sys
from typing import TextIO


def number_stream(stream: TextIO):
    for i, line in enumerate(stream, start=1):
        sys.stdout.write(f"{i:>6}\t{line}")


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        number_stream(sys.stdin)
    elif len(args) == 1:
        filename = args[0]
        try:
            with open(filename, encoding="utf-8") as f:
                number_stream(f)
        except OSError as e:
            print(f"fail to open the file '{filename}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"usage: {sys.argv[0]} [file]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

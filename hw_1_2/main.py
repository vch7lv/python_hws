#!/usr/bin/env python3
import sys
from collections import deque


def tail_stream(stream, n_lines):
    buf = deque(maxlen=n_lines)
    for line in stream:
        buf.append(line)
    return buf


def main():
    files = sys.argv[1:]

    if not files:
        lines = tail_stream(sys.stdin, 17)
        sys.stdout.writelines(lines)
        return

    first = True

    for name in files:
        try:
            with open(name, 'r', encoding='utf-8') as f:
                if len(files) > 1:
                    if not first:
                        sys.stdout.write('\n')
                    sys.stdout.write(f"==> {name} <==\n")
                    first = False

                lines = tail_stream(f, 10)
                sys.stdout.writelines(lines)
        except OSError as e:
            print(f"{sys.argv[0]}: cannot open '{name}' for reading: {e}",
                  file=sys.stderr)


if __name__ == "__main__":
    main()
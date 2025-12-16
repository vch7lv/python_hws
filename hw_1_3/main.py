#!/usr/bin/env python3
import sys


WHITESPACE = b" \t\n\r\v\f"


def wc_stream(stream):
    lines = words = bytes_cnt = 0
    prev_space = True

    while True:
        chunk = stream.read(8192)
        if not chunk:
            break

        bytes_cnt += len(chunk)
        lines += chunk.count(b"\n")

        for b in chunk:
            if b in WHITESPACE:
                prev_space = True
            else:
                if prev_space:
                    words += 1
                prev_space = False

    return lines, words, bytes_cnt


def print_stats(stats, name=None):
    l, w, b = stats
    if name is None:
        print(f"{l:7d} {w:7d} {b:7d}")
    else:
        print(f"{l:7d} {w:7d} {b:7d} {name}")


def main():
    files = sys.argv[1:]

    if not files:
        stats = wc_stream(sys.stdin.buffer)
        print_stats(stats)
        return

    total = [0, 0, 0]
    many = len(files) > 1

    for name in files:
        try:
            with open(name, "rb") as f:
                stats = wc_stream(f)
        except OSError as e:
            print(f"{sys.argv[0]}: {e}", file=sys.stderr)
            continue

        print_stats(stats, name)
        for i in range(3):
            total[i] += stats[i]

    if many:
        print_stats(tuple(total), "total")


if __name__ == "__main__":
    main()

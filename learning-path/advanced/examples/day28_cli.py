"""Day 28 example: a command-line tool with argparse.

Usage examples:
  python3 day28_cli.py logsummary sample.log
  python3 day28_cli.py logsummary sample.log --level ERROR --top 3
  python3 day28_cli.py weather Chennai          (needs network + requests)
  python3 day28_cli.py --help
  python3 day28_cli.py logsummary --help

Try it without a file first:
  python3 day28_cli.py demo
"""

import argparse
import sys
from collections import Counter
from pathlib import Path


# ---------- LOGIC (kept separate from CLI parsing: easy to test) ----------
def summarise_log(lines, level=None, top=5):
    """Return (total_matching_lines, [(message, count), ...])."""
    messages = []
    for line in lines:
        parts = line.strip().split(" ", 2)         # DATE LEVEL MESSAGE
        if len(parts) < 3:
            continue                                # skip malformed lines
        _, lvl, msg = parts
        if level is None or lvl == level:
            messages.append(msg)
    return len(messages), Counter(messages).most_common(top)


# ---------- COMMAND HANDLERS ----------
def cmd_logsummary(args):
    path = Path(args.file)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1                                    # non-zero = failure
    with open(path) as f:
        total, common = summarise_log(f, args.level, args.top)
    print(f"Matching lines: {total}")
    for msg, count in common:
        print(f"  {count:>3} x {msg}")
    return 0


def cmd_weather(args):
    import requests                                 # imported only when needed
    try:
        r = requests.get(f"https://wttr.in/{args.city}?format=3", timeout=10)
        r.raise_for_status()
        print(r.text.strip())
        return 0
    except requests.exceptions.RequestException as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


def cmd_demo(args):
    sample = [
        "2026-01-01 INFO started",
        "2026-01-01 ERROR disk full",
        "2026-01-02 ERROR disk full",
        "2026-01-02 WARN slow response",
        "2026-01-03 ERROR timeout",
    ]
    total, common = summarise_log(sample, level="ERROR")
    print("Demo (ERROR lines):", total, common)
    return 0


# ---------- THE CLI DEFINITION ----------
def build_parser():
    parser = argparse.ArgumentParser(
        prog="day28_cli",
        description="Small toolbox: summarise logs, check weather.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("logsummary", help="count the most common log messages")
    p_log.add_argument("file", help="path to a log file (format: DATE LEVEL MESSAGE)")
    p_log.add_argument("--level", choices=["INFO", "WARN", "ERROR"], help="only this level")
    p_log.add_argument("--top", type=int, default=5, help="how many to show (default 5)")
    p_log.set_defaults(func=cmd_logsummary)

    p_w = sub.add_parser("weather", help="one-line weather for a city")
    p_w.add_argument("city")
    p_w.set_defaults(func=cmd_weather)

    p_d = sub.add_parser("demo", help="run on built-in sample data")
    p_d.set_defaults(func=cmd_demo)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

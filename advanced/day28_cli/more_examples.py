"""Day 28: Command-line tools with argparse. 10 examples, simple to complex.

Run:  python3 advanced/day28_cli/more_examples.py

Real programs read arguments from the terminal. To make every behaviour easy
to see, each example passes an explicit list of arguments to parse_args()
instead. Normally you would call parser.parse_args() with no argument and
type the options after the command.
"""

import argparse
import contextlib
import io
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


def try_parse(parser, argv):
    """Parse argv; show the error text instead of exiting the whole program."""
    err = io.StringIO()
    try:
        with contextlib.redirect_stderr(err):
            return parser.parse_args(argv)
    except SystemExit as e:
        print(f"  parse failed (exit code {e.code}):", err.getvalue().strip().splitlines()[-1])
        return None


# ---------------------------------------------------------------
show(1, "A required positional argument")
# WHAT: the smallest command-line tool.
# HOW : add_argument("name") makes it required; args.name holds the value.
# WHY : `greet Sam` is more useful than a program that asks questions.
parser = argparse.ArgumentParser(description="Greet someone")
parser.add_argument("name")
args = parser.parse_args(["Sam"])
print(f"Hello, {args.name}!")
try_parse(parser, [])

# ---------------------------------------------------------------
show(2, "Optional arguments with defaults")
# WHAT: --flag value options that may be omitted.
# HOW : names starting with -- are optional; default= fills in when absent.
# WHY : sensible defaults keep common commands short.
parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--greeting", default="Hello")
parser.add_argument("--times", type=int, default=1)
for argv in (["Sam"], ["Sam", "--greeting", "Hi", "--times", "2"]):
    a = parser.parse_args(argv)
    print(argv, "->", [f"{a.greeting}, {a.name}!"] * a.times)

# ---------------------------------------------------------------
show(3, "type= and choices= validate for you")
# WHAT: automatic conversion and checking.
# HOW : type=int converts or errors; choices=[...] restricts the values.
# WHY : you never write validation code for these cases.
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--level", choices=["debug", "info", "error"], default="info")
print(parser.parse_args(["--port", "9000", "--level", "debug"]))
try_parse(parser, ["--port", "abc"])
try_parse(parser, ["--level", "loud"])

# ---------------------------------------------------------------
show(4, "On/off switches: store_true")
# WHAT: flags that need no value.
# HOW : action="store_true" gives False by default, True when present.
# WHY : --verbose, --dry-run, --force.
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--dry-run", action="store_true")
print(parser.parse_args([]))
print(parser.parse_args(["--verbose", "--dry-run"]))

# ---------------------------------------------------------------
show(5, "Several values: nargs")
# WHAT: accept a list of items.
# HOW : nargs="+" means one or more; "*" means zero or more.
# WHY : `tool file1 file2 file3`.
parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")
parser.add_argument("--exclude", nargs="*", default=[])
a = parser.parse_args(["a.txt", "b.txt", "c.txt", "--exclude", "b.txt"])
print([f for f in a.files if f not in a.exclude])

# ---------------------------------------------------------------
show(6, "Short names and counting flags")
# WHAT: -v/--verbose and -vv for more detail.
# HOW : give both names; action="count" counts repeats.
# WHY : familiar Unix style.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("-o", "--output", default="out.txt")
a = parser.parse_args(["-vv", "-o", "result.json"])
print("verbosity", a.verbose, "| output", a.output)

# ---------------------------------------------------------------
show(7, "Mutually exclusive options and required options")
# WHAT: allow only one of several, or insist on one.
# HOW : add_mutually_exclusive_group; required=True.
# WHY : --json versus --csv should never both be given.
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--json", action="store_true")
group.add_argument("--csv", action="store_true")
parser.add_argument("--token", required=True)
print(parser.parse_args(["--token", "abc", "--json"]))
try_parse(parser, ["--token", "abc", "--json", "--csv"])
try_parse(parser, ["--json"])

# ---------------------------------------------------------------
show(8, "Subcommands, like git add / git commit")
# WHAT: one program, several actions.
# HOW : add_subparsers; set_defaults(func=...) attaches a handler to each.
# WHY : keeps big tools organised; main just dispatches.
def cmd_add(args):
    return f"adding {args.item} x{args.qty}"


def cmd_list(args):
    return "listing everything" + (" (long)" if args.long else "")


parser = argparse.ArgumentParser(prog="shop")
sub = parser.add_subparsers(dest="command", required=True)
p_add = sub.add_parser("add", help="add an item")
p_add.add_argument("item")
p_add.add_argument("--qty", type=int, default=1)
p_add.set_defaults(func=cmd_add)
p_list = sub.add_parser("list", help="list items")
p_list.add_argument("--long", action="store_true")
p_list.set_defaults(func=cmd_list)
for argv in (["add", "pen", "--qty", "3"], ["list", "--long"]):
    a = parser.parse_args(argv)
    print(argv, "->", a.func(a))
try_parse(parser, ["remove"])

# ---------------------------------------------------------------
show(9, "Exit codes and standard error")
# WHAT: tell the shell whether you succeeded.
# HOW : return 0 for success, non-zero for failure; print errors to stderr.
# WHY : scripts and CI check the exit code; stderr keeps results clean when
#       output is redirected to a file.
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args(argv)
    if not Path(args.path).exists():
        print(f"error: {args.path} not found", file=sys.stderr)
        return 1
    print("found", args.path)
    return 0


with contextlib.redirect_stderr(io.StringIO()) as captured:
    code = main(["/no/such/file"])
print("exit code:", code, "| stderr said:", captured.getvalue().strip())
print("exit code:", main([__file__]))

# ---------------------------------------------------------------
show(10, "Mini program: a log summary tool")
# WHAT: a complete, testable command-line tool.
# HOW : pure logic in one function, a parser builder, and main(argv) returning
#       an exit code. Tests call main() with argument lists.
# WHY : the structure of every professional script.
def summarise(lines, level=None, top=3):
    messages = []
    for line in lines:
        parts = line.strip().split(" ", 2)
        if len(parts) == 3 and (level is None or parts[1] == level):
            messages.append(parts[2])
    return len(messages), Counter(messages).most_common(top)


def build_parser():
    p = argparse.ArgumentParser(prog="logsum", description="Summarise a log file")
    p.add_argument("file")
    p.add_argument("--level", choices=["INFO", "WARN", "ERROR"])
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--json", action="store_true", help="machine-readable output")
    return p


def cli(argv):
    args = build_parser().parse_args(argv)
    path = Path(args.file)
    if not path.exists():
        print(f"error: {path} not found", file=sys.stderr)
        return 1
    with open(path) as f:
        total, common = summarise(f, args.level, args.top)
    if args.json:
        print(json.dumps({"matching": total, "top": common}))
    else:
        print(f"Matching lines: {total}")
        for msg, count in common:
            print(f"  {count:>3} x {msg}")
    return 0


with tempfile.TemporaryDirectory() as folder:
    log = Path(folder) / "app.log"
    log.write_text("1 INFO start\n2 ERROR disk full\n3 ERROR disk full\n"
                   "4 WARN slow\n5 ERROR timeout\nbad line\n")
    print("$ logsum app.log --level ERROR")
    cli([str(log), "--level", "ERROR"])
    print("$ logsum app.log --json --top 1")
    cli([str(log), "--json", "--top", "1"])
    with contextlib.redirect_stderr(io.StringIO()):
        print("$ logsum missing.log  -> exit code", cli([str(Path(folder) / "missing.log")]))

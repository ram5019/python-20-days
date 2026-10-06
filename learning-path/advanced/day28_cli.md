# Day 28: Command-Line Tools with `argparse`

**Example:** `examples/day28_cli.py` | **Your stub:** `advanced/day28_weather_cli.py`

---

## 1. The big idea

A **command-line interface (CLI)** lets people run your program from the terminal with **options and arguments**:

```bash
python3 day28_cli.py logsummary app.log --level ERROR --top 3
```

Python's built-in `argparse` module reads those words for you, validates them, and writes the `--help` text automatically.

## 2. Why does it exist?

Until now your programs asked questions with `input()`. That works for one person at a keyboard, but **real tools** are used in scripts, cron jobs and pipelines where nobody is there to type. Arguments make a tool:

- **Scriptable** (run it 100 times with different values),
- **Self-documenting** (`--help`),
- **Shareable** (a teammate can use it without reading the code).

For automation and DevOps (Track 3 and Track 5) this is how almost every script is shaped.

## 3. Simple way to understand

A **vending machine panel** versus a **waiter taking an order**.

- `input()` = a waiter who asks you questions one by one. Friendly, but slow and impossible to automate.
- CLI arguments = a vending machine **keypad**: you press everything you want in one go, and the machine either gives your item or says exactly what you got wrong.

## 4. How it works

```python
parser = argparse.ArgumentParser(description="...")
parser.add_argument("file")                       # required positional
parser.add_argument("--top", type=int, default=5) # optional flag with a default
args = parser.parse_args()
print(args.file, args.top)
```

| Kind | Example | Notes |
|------|---------|-------|
| positional | `"file"` | required, order matters |
| optional | `"--level"` | name starts with `--` |
| `type=int` | converts the text | rejects non-numbers automatically |
| `choices=[...]` | restricts values | clear error if wrong |
| `default=` | used when omitted | |
| `action="store_true"` | a yes/no switch | `--verbose` |
| subcommands | `add_subparsers` | like `git commit`, `git push` |

**Exit codes:** a program returns `0` for success and non-zero for failure. Scripts and CI systems check it. `sys.exit(1)` signals an error. Error messages go to `sys.stderr`, not the normal output.

## 5. Code walkthrough, block by block

### Logic: `summarise_log`
Pure logic (Day 14, Day 20 layering): it takes lines in and returns numbers out. It does not know about the command line. It splits each line into 3 parts (`split(" ", 2)` splits at most twice, so the message may contain spaces), skips malformed lines, and counts messages with `collections.Counter` (Day 17). Because it is separate, you can test it with a plain list.

### Command handlers
Each subcommand has a handler taking `args`:
- `cmd_logsummary` checks the file exists (Day 15), prints an error to stderr and **returns 1** on failure, else prints the result and returns 0. It reads the file lazily by passing the file object straight to `summarise_log` (Day 24).
- `cmd_weather` imports `requests` **inside** the function so the rest of the tool works even if `requests` is not installed. It handles failures with Day 26's pattern.
- `cmd_demo` runs on built-in sample data, so you can try the tool with zero setup.

### `build_parser`
Describes the interface:
- `add_subparsers(dest="command", required=True)` creates `logsummary`, `weather`, `demo` as sub-tools.
- `set_defaults(func=...)` attaches the handler function to each subcommand, so `main` can simply call `args.func(args)`. This is **functions as values** (Day 22) used in practice.

### `main` and the entry point
`main(argv=None)` parses and dispatches. `sys.exit(main())` turns the handler's return value into the process exit code. The `if __name__ == "__main__":` guard is Day 17.

### Try it

```bash
cd learning-path/advanced/examples
python3 day28_cli.py demo
python3 day28_cli.py --help
python3 day28_cli.py logsummary --help
python3 day28_cli.py logsummary nofile.log ; echo "exit code: $?"
python3 day28_cli.py weather Chennai
```

Create a `sample.log` with lines like `2026-01-01 ERROR disk full` and run `logsummary sample.log --level ERROR`.

## 6. How the blocks connect

```
build_parser  ── defines what the user may type
     │
main ── parse_args ── args.func(args) ──► handler
                                            │ uses
                                            ▼
                                     logic function (pure)
                                            │ may use
                                            ▼
                                  files / network / output
```

Same layering as Day 20: **interface → handler → logic → storage**.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Everything inside one giant function | hard to test | keep logic separate |
| Forgetting `type=int` | value stays a string | add `type=` |
| Printing errors to normal output | breaks pipelines | `print(..., file=sys.stderr)` |
| Always returning 0 | scripts cannot detect failure | non-zero on error |
| Not providing `help=` text | useless `--help` | describe each argument |
| Using `input()` inside a CLI tool | blocks automation | take an argument instead |

## 8. Practice

1. Update your stub `day28_weather_cli.py` to take `--units` with `choices=["metric","imperial"]` (wttr.in supports `?m` and `?u`).
2. Add `--verbose` (`action="store_true"`) that prints the URL it calls.
3. Add a `wordcount` subcommand: `wordcount file.txt --top 5`.
4. Add `--output out.json` to `logsummary` to save the result with `json.dump`.
5. Make the exit code reflect "no matching lines found" (for example `2`).
6. Add a `csv-to-json` subcommand using your Day 27 helpers.

## 9. Self-check

- Why is `argparse` better than `input()` for automation?
- What does `type=int` do?
- What does a non-zero exit code mean?
- Why separate logic from the argument parsing?

---

**Part A complete.** You now write clean, efficient Python, manage environments, talk to APIs, handle data files and ship command-line tools. Continue with Part B: `track1_data_science.md`.

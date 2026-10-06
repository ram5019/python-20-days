# Day 15: Files

**Time:** ~2 hours | **Example:** `examples/day15_files.py` | **Your practice file:** `week3_structure/day15_files.py`

---

## 1. The big idea

Variables live in memory and **vanish when the program ends**. A **file** lives on disk and **survives**. Python can write data to a file and read it back later.

## 2. Why does this exist?

Think of everything you have built so far: close the program and all the data is gone. Real tools must **remember**: notes, scores, settings, logs. Files are the simplest form of **persistence**. They are also how Python reads data created by *other* programs: log files, exports, configs.

For a support engineer this is daily work: read a log, filter lines, write a summary.

## 3. Simple way to understand

A **notebook in a drawer**.

- Variables = what you hold in your head (lost when you sleep).
- File = writing it in the notebook (still there tomorrow).
- **Opening** the notebook = `open()`. You must say **why**: to *read*, to *write* a fresh page, or to *add* at the end.
- **Closing** it = important, so nothing is half-written. Python's `with` block closes it for you automatically.

## 4. How it works

```python
with open("notes.txt", "w") as f:
    f.write("hello\n")
```

| Mode | Meaning | If file exists | If missing |
|------|---------|----------------|-----------|
| `"r"` (default) | read | reads it | **error** |
| `"w"` | write | **erases it** and starts fresh | creates it |
| `"a"` | append | adds to the end | creates it |

Main operations:

| Call | Does |
|------|------|
| `f.write(text)` | writes text (no automatic newline: add `\n`) |
| `f.read()` | whole file as one string |
| `f.readlines()` | list of lines |
| `for line in f:` | one line at a time (memory-friendly) |

**`with` block:** the file is guaranteed to close when the block ends, even if an error occurs. Always use it.

## 5. Code walkthrough, block by block

### Setup

```python
from pathlib import Path
BASE = Path(__file__).parent
FILE = BASE / "demo_notes.txt"
```

**What it does:** `__file__` is this script's own location. `.parent` is its folder. `BASE / "demo_notes.txt"` joins path pieces using the `/` operator of `pathlib` (works on Mac, Linux and Windows). This stops the classic "file not found because I ran it from another folder" problem.

### Block 1: write

```python
with open(FILE, "w") as f:
    f.write("Line one\n")
    f.write("Line two\n")
```

**What it does:** opens the file for writing (creating it), gives it the nickname `f`, writes two lines, and closes it automatically when the indented block ends. `\n` is the newline character: without it all text would be glued into one line. **Danger:** mode `"w"` wipes any existing content.

### Block 2: append

```python
with open(FILE, "a") as f:
    f.write("Line three\n")
```

**What it does:** adds to the end without erasing. The file now has 3 lines. **Link to Block 1:** Block 2 only works as intended because Block 1 created the file; compare `"w"` and `"a"` by swapping them and observing.

### Block 3: read all

```python
with open(FILE, "r") as f:
    content = f.read()
print(content)
```

**What it does:** reads the whole file into one string. The `print` happens **after** the `with` block, because `content` is already safely in memory. Good for small files.

### Block 4: line by line

```python
with open(FILE) as f:
    for line in f:
        print(line.strip())
```

**What it does:** a file is **iterable**, so a `for` loop (Day 8) gives you one line per round. Each line still ends with `\n`, so `.strip()` (Day 3) removes it. This is the right choice for large files such as logs, because it never loads everything into memory.

### Block 5: readlines

```python
with open(FILE) as f:
    lines = f.readlines()
print(len(lines), "lines")
```

**What it does:** returns a **list** of lines (Day 10). Useful if you need to count, index or loop several times.

### Block 6: check existence

```python
missing = BASE / "does_not_exist.txt"
if missing.exists():
    print("found")
else:
    print("no such file, skipping")
```

**What it does:** `.exists()` returns True/False (Day 6 decision). Opening a missing file in `"r"` mode raises `FileNotFoundError`. Checking first avoids a crash. **Day 16** shows an even more robust method (`try/except`).

### Block 7: a practical use

```python
with open(FILE) as f:
    words = f.read().split()
print("Word count:", len(words))
```

**What it does:** chains Day 15 (read) with Day 3 (`.split()` into words) and Day 10 (`len`). Reading is usually just the *first* step; strings, lists and dicts do the processing. Combine it with Day 13's counting recipe and you have a word-frequency tool.

### Block 8: clean up

```python
FILE.unlink()
```

**What it does:** deletes the demo file so your folder stays tidy. Delete operations are **permanent**, so always be sure of the path first.

## 6. How the blocks connect

```
Block 1  write (create)       ─┐
Block 2  append (extend)       ├── put data ON disk
                              ─┘
Block 3  read all             ─┐
Block 4  read line by line     ├── get data BACK
Block 5  read as list         ─┘
Block 6  check it exists      ── safety before reading
Block 7  process what you read ── use Days 3, 10, 13
Block 8  remove               ── housekeeping
```

Pipeline: **write → read → process**. Blocks 3 to 5 read what Blocks 1 and 2 wrote.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `"w"` when you meant `"a"` | old data erased | use `"a"` to add |
| Missing `\n` in `write` | all text on one line | add `\n` |
| Reading a missing file | `FileNotFoundError` | check `.exists()` or use `try/except` (Day 16) |
| Forgetting `.strip()` on lines | blank lines in output | strip the newline |
| Not using `with` | file may stay open / data lost | always `with open(...)` |
| Relative path depends on where you run | file not found | use `Path(__file__).parent` |
| Writing a number | `TypeError` | `f.write(str(5))` |

## 8. Practice

1. Fill in `day15_files.py`: write three lines of your own, then read them back and print them with line numbers.
2. Ask the user for notes in a `while` loop (Day 9) and append each one to `notes.txt`; stop on `quit`.
3. Read a text file and print the **longest line**.
4. Count how many lines of a file contain the word `error` (any case).
5. Copy one file to another, converting everything to uppercase.
6. Save a list of numbers (one per line), then read them back, convert to `int` and print the sum.

## 9. Self-check

- What is the difference between `"w"` and `"a"`?
- Why use `with` instead of `open` alone?
- When would you loop over the file instead of using `read()`?
- Why does each line need `.strip()`?

**Next:** Day 16: files can be missing, input can be wrong. Learn to **handle errors** instead of crashing.

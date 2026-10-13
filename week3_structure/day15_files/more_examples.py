"""Day 15: Files. 10 examples, simple to complex.

Run:  python3 week3_structure/day15_files/more_examples.py

All files are created inside a temporary folder that is deleted when the
program finishes, so your folders stay clean.
"""

import tempfile
from pathlib import Path

TMP = tempfile.TemporaryDirectory()
BASE = Path(TMP.name)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Write a file")
# WHAT: save text to disk.
# HOW : open(path, "w") creates (or ERASES) the file. `with` closes it for you.
#       Add \n yourself; write() does not.
# WHY : variables vanish when the program ends; files stay.
notes = BASE / "notes.txt"
with open(notes, "w") as f:
    f.write("Line one\n")
    f.write("Line two\n")
print("written:", notes.name, notes.stat().st_size, "bytes")

# ---------------------------------------------------------------
show(2, "Append instead of overwrite")
# WHAT: add to the end without erasing.
# HOW : mode "a". Compare with "w", which would start from scratch.
# WHY : logs and history grow over time.
with open(notes, "a") as f:
    f.write("Line three\n")
print(notes.read_text())

# ---------------------------------------------------------------
show(3, "Read everything at once")
# WHAT: load the whole file as one string.
# HOW : f.read(). Fine for small files.
# WHY : the quickest way to look at a file.
with open(notes) as f:
    content = f.read()
print(repr(content))
print("characters:", len(content))

# ---------------------------------------------------------------
show(4, "Read line by line")
# WHAT: process a large file without loading it all.
# HOW : a file object can be looped over; each line ends with \n, so strip it.
# WHY : memory-friendly; essential for big logs.
with open(notes) as f:
    for number, line in enumerate(f, start=1):
        print(number, line.strip())

# ---------------------------------------------------------------
show(5, "Read into a list of lines")
# WHAT: get lines as list items.
# HOW : f.readlines() keeps the \n; .read().splitlines() removes it.
# WHY : lets you index, count and loop several times.
with open(notes) as f:
    lines = f.read().splitlines()
print(lines)
print("last line:", lines[-1], "| count:", len(lines))

# ---------------------------------------------------------------
show(6, "What `with` really does")
# WHAT: prove the file is closed after the block.
# HOW : f.closed is False inside the block and True after it, even if an
#       error happens inside.
# WHY : unclosed files can lose data or lock the file.
with open(notes) as f:
    print("inside the block, closed?", f.closed)
print("after the block, closed?", f.closed)

# ---------------------------------------------------------------
show(7, "Files that do not exist")
# WHAT: check first, or handle the error.
# HOW : Path.exists() answers True/False; opening a missing file raises
#       FileNotFoundError, which try/except (Day 16) can catch.
# WHY : never assume a file is there.
missing = BASE / "missing.txt"
print("exists?", missing.exists())
try:
    open(missing)
except FileNotFoundError as error:
    print("Caught:", type(error).__name__)

# ---------------------------------------------------------------
show(8, "Numbers go in as text and come back as text")
# WHAT: save a list of numbers and read them back.
# HOW : write str(n); on reading convert with int().
# WHY : files only hold text; you convert at the boundary.
numbers_file = BASE / "numbers.txt"
with open(numbers_file, "w") as f:
    for n in [10, 20, 30, 40]:
        f.write(f"{n}\n")
with open(numbers_file) as f:
    numbers = [int(line) for line in f]
print(numbers, "sum =", sum(numbers))

# ---------------------------------------------------------------
show(9, "Mini tool: search a log file")
# WHAT: count and extract ERROR lines.
# HOW : loop lines, test with `in` (Day 3), collect matches (Day 11).
# WHY : the everyday log-analysis task.
log = BASE / "app.log"
log.write_text(
    "10:00 INFO started\n"
    "10:05 ERROR disk full\n"
    "10:06 INFO retry\n"
    "10:07 ERROR disk full\n"
    "10:09 WARN slow\n"
)
errors = []
with open(log) as f:
    for line in f:
        if "ERROR" in line:
            errors.append(line.strip())
print(len(errors), "errors")
for e in errors:
    print("  ", e)
levels = {}
for line in log.read_text().splitlines():
    level = line.split()[1]
    levels[level] = levels.get(level, 0) + 1
print(levels)

# ---------------------------------------------------------------
show(10, "Mini program: a notes app that remembers")
# WHAT: save and load a list of notes between runs.
# HOW : load_notes returns [] when the file does not exist yet;
#       save_notes rewrites the whole file.
# WHY : "load, change, save" is the shape of every small data app.
NOTES_FILE = BASE / "my_notes.txt"


def load_notes():
    if not NOTES_FILE.exists():
        return []
    return NOTES_FILE.read_text().splitlines()


def save_notes(notes_list):
    NOTES_FILE.write_text("\n".join(notes_list) + "\n")


notes_list = load_notes()
print("first run, notes:", notes_list)
notes_list.append("buy milk")
notes_list.append("call Ana")
save_notes(notes_list)
print("second run, notes:", load_notes())
notes_list = load_notes()
notes_list.remove("buy milk")
save_notes(notes_list)
print("third run, notes:", load_notes())

TMP.cleanup()
print("\n(temporary files deleted)")

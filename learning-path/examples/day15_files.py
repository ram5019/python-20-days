"""Day 15 example: reading and writing files.

Run:  python3 learning-path/examples/day15_files.py
(Creates a small 'demo_notes.txt' file next to this script.)
"""

from pathlib import Path

# Always build paths relative to THIS file so it works from any folder
BASE = Path(__file__).parent
FILE = BASE / "demo_notes.txt"

# BLOCK 1: write a file (creates or overwrites)
with open(FILE, "w") as f:
    f.write("Line one\n")
    f.write("Line two\n")

# BLOCK 2: append to a file
with open(FILE, "a") as f:
    f.write("Line three\n")

# BLOCK 3: read everything at once
with open(FILE, "r") as f:
    content = f.read()
print(content)

# BLOCK 4: read line by line
with open(FILE) as f:                    # "r" is the default mode
    for line in f:
        print(line.strip())              # strip removes the trailing \n

# BLOCK 5: read lines into a list
with open(FILE) as f:
    lines = f.readlines()
print(len(lines), "lines")

# BLOCK 6: check existence before reading
missing = BASE / "does_not_exist.txt"
if missing.exists():
    print("found")
else:
    print("no such file, skipping")

# BLOCK 7: practical: count words in a file
with open(FILE) as f:
    words = f.read().split()
print("Word count:", len(words))

# BLOCK 8: clean up the demo file
FILE.unlink()
print("Demo file removed")

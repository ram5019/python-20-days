"""Day 17: Modules and imports. 10 examples, simple to complex.

Run:  python3 week3_structure/day17_modules/more_examples.py

Example 8 imports mytools.py, which sits in the same folder as this file.
"""

import sys
import tempfile
from pathlib import Path


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "import a whole module")
# WHAT: use ready-made tools from Python's standard library.
# HOW : `import math` then math.something. The dot says which toolbox.
# WHY : never rewrite what already exists and is already tested.
import math

print(math.sqrt(144), math.pi)
print(math.ceil(4.1), math.floor(4.9), math.factorial(5))
print(math.hypot(3, 4))

# ---------------------------------------------------------------
show(2, "from ... import: pick specific names")
# WHAT: bring in just what you need, without the prefix.
# HOW : from module import name1, name2.
# WHY : shorter code; fine for a few names. Avoid `import *`.
from math import gcd, log10

print(gcd(12, 18), log10(1000))

# ---------------------------------------------------------------
show(3, "import ... as: a short nickname")
# WHAT: alias a long module name.
# HOW : import datetime as dt.
# WHY : standard habit (numpy as np, pandas as pd later).
import datetime as dt

d = dt.date(2026, 10, 13)
print(d, d.strftime("%A, %d %B %Y"))
print("in 30 days:", d + dt.timedelta(days=30))

# ---------------------------------------------------------------
show(4, "random: reproducible chance")
# WHAT: random choices that repeat when you fix the seed.
# HOW : random.seed(n) makes the sequence predictable for tests.
# WHY : games, sampling, simulations, test data.
import random

random.seed(42)
print(random.randint(1, 6), random.randint(1, 6))
print(random.choice(["red", "green", "blue"]))
deck = list(range(1, 8))
random.shuffle(deck)
print(deck, random.sample(range(100), 3))

# ---------------------------------------------------------------
show(5, "collections: smarter containers")
# WHAT: Counter and defaultdict save you from hand-written loops.
# HOW : Counter counts items; defaultdict(list) creates missing keys.
# WHY : Day 13's counting and grouping recipes in one line.
from collections import Counter, defaultdict

print(Counter("mississippi"))
print(Counter("the cat and the hat and the bat".split()).most_common(2))
groups = defaultdict(list)
for word in ["apple", "avocado", "banana"]:
    groups[word[0]].append(word)
print(dict(groups))

# ---------------------------------------------------------------
show(6, "statistics and itertools")
# WHAT: mean/median and combinations without writing the maths.
# HOW : import the functions; call them on a list.
# WHY : correct, tested implementations are one import away.
import itertools
import statistics

data = [72, 88, 95, 60, 88]
print(statistics.mean(data), statistics.median(data), statistics.mode(data))
print(list(itertools.combinations(["A", "B", "C"], 2)))
print(list(itertools.permutations([1, 2, 3], 2))[:4])

# ---------------------------------------------------------------
show(7, "sys, os and pathlib: your environment")
# WHAT: ask about Python and the file system.
# HOW : sys.version, sys.argv; os.cpu_count; Path for folders and files.
# WHY : scripts often need to know where they are and what is around them.
import os

print("Python", sys.version.split()[0])
print("Command-line arguments:", len(sys.argv))
here = Path(__file__).parent
print("This file's folder:", here.name)
print("Files here:", sorted(p.name for p in here.iterdir() if p.suffix == ".py"))
print("CPU cores:", os.cpu_count() is not None)

# ---------------------------------------------------------------
show(8, "Import YOUR OWN module")
# WHAT: a module is just a .py file next to your script.
# HOW : import mytools finds mytools.py in this folder.
# WHY : split big programs into files by topic.
import mytools

print(mytools.circle_area(2))
print(mytools.shout("modules work"))
print("mytools.__name__ =", mytools.__name__)
print("this file's __name__ =", __name__)

# ---------------------------------------------------------------
show(9, "Explore any module with dir() and help()")
# WHAT: discover what a module offers.
# HOW : dir(module) lists names; __doc__ holds the documentation.
# WHY : fastest way to learn a new library.
public = [name for name in dir(math) if not name.startswith("_")]
print(len(public), "public names in math, e.g.", public[:6])
print(math.sqrt.__doc__.splitlines()[0])
print((statistics.mean.__doc__ or "").strip().splitlines()[0])

# ---------------------------------------------------------------
show(10, "Mini program: build a module, import it, see __name__ at work")
# WHAT: create a module file at run time, then import and use it.
# HOW : write the file to a temp folder, add the folder to sys.path (where
#       Python looks for imports), import it. The `if __name__ ==
#       "__main__"` block runs only when the file is run directly.
# WHY : shows exactly how imports work and why that guard exists.
with tempfile.TemporaryDirectory() as folder:
    (Path(folder) / "greeter.py").write_text(
        'def hello(name):\n'
        '    return f"Hello, {name}!"\n'
        '\n'
        'if __name__ == "__main__":\n'
        '    print("greeter was run directly")\n'
    )
    sys.path.insert(0, folder)
    import greeter

    print(greeter.hello("Sam"))
    print("greeter.__name__ =", greeter.__name__)
    print("(no 'run directly' message appeared, because we only imported it)")
    sys.path.remove(folder)

# Day 17: Modules and Imports

**Time:** ~2 hours | **Examples:** `examples/day17_modules.py` and `examples/mytools.py` | **Your practice file:** `week3_structure/day17_modules.py`

---

## 1. The big idea

A **module** is a Python file containing code (functions, variables) that **other files can import and reuse**. Python ships with hundreds of ready-made modules (the **standard library**), and you can write your own.

## 2. Why does this exist?

- **Don't reinvent the wheel.** Square roots, dates, random numbers, JSON and file paths are already solved. Importing is faster and less buggy than writing your own.
- **Keep files small.** One 2,000-line file is a nightmare. Split it by topic: `input_tools.py`, `calculations.py`, `storage.py`.
- **Reuse across projects.** Write `ask_int` once (Day 16), import it everywhere.
- **Teamwork.** Different people can own different modules.

## 3. Simple way to understand

A **toolbox shelf in a workshop**.

- Your script is the workbench.
- Each module is a **labelled toolbox**: `math`, `random`, `datetime`.
- `import math` = "bring the maths toolbox to my bench".
- `math.sqrt(16)` = "from the maths box, use the square-root tool". The **dot** says which toolbox it came from, which also prevents two tools with the same name from clashing.

## 4. How it works

| Form | Use | Call |
|------|-----|------|
| `import math` | whole module | `math.sqrt(9)` |
| `from math import sqrt` | specific names | `sqrt(9)` |
| `import datetime as dt` | nickname | `dt.date.today()` |
| `from x import *` | everything (avoid!) | unclear where names come from |

**Where does Python look?** First your current folder, then the standard library, then installed packages (Day 25 covers `pip` and `venv`). That is why `import mytools` works when the file is next to your script.

**`__name__`:** every module has a built-in `__name__`.
- When you **run** a file directly → `__name__ == "__main__"`.
- When it is **imported** → `__name__` is the module's name.

So `if __name__ == "__main__":` means **"only run this part when I'm the main program, not when I'm imported."**

## 5. Code walkthrough, block by block

### Block 1: import a whole module

```python
import math
print(math.sqrt(16))
print(math.pi)
print(math.ceil(4.1), math.floor(4.9))
```

**What it does:** `import math` loads the module. Everything inside is reached with `math.` in front: a function (`sqrt`), a constant (`pi`), rounding helpers (`ceil` rounds up → 5, `floor` rounds down → 4). Same dot you used for string and list methods; the idea of "things that belong to something" is consistent in Python.

### Block 2: import specific names

```python
from random import randint, choice
print(randint(1, 6))
print(choice(["red", "green", "blue"]))
```

**What it does:** pulls just two tools into your file so you can use them **without** the prefix. `randint(1, 6)` is a random integer from 1 to 6 inclusive. `choice` picks a random item from a list (Day 10).

### Block 3: nickname

```python
import datetime as dt
print(dt.date.today())
```

**What it does:** `as dt` gives a short alias. This is a standard habit for long names. (You used `from datetime import datetime` on Day 7, which is the "specific name" style.)

### Block 4: more of the standard library

```python
import os
import sys
from collections import Counter

print(os.getcwd())
print(sys.version.split()[0])
print(Counter("mississippi"))
```

**What it does:**
- `os.getcwd()` → current working folder.
- `sys.version` → Python's version as text; `.split()[0]` (Day 3) takes the first word.
- `Counter` does automatically what you wrote by hand on Day 13: it counts each letter and returns `Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})`. Now that you understand the manual way, the shortcut has meaning.

### Block 5: your own module

```python
import mytools
print(mytools.circle_area(3))
print(mytools.shout("modules work"))
```

**What it does:** imports the file `mytools.py` that sits next to this script, then uses its functions. **A module is just a file.** There is nothing special to set up. Open `mytools.py`: it has `PI`, `circle_area` and `shout`, which are plain Day 14 functions.

### Block 6: discovering what is inside

```python
print([name for name in dir(math) if not name.startswith("_")][:8])
```

**What it does:** `dir(module)` lists every name inside. The bracket expression is a preview of **list comprehensions** (Day 21): it loops through the names, skips the private ones starting with `_`, and `[:8]` keeps the first eight (a slice, Day 3). `help(math.sqrt)` shows documentation (the docstrings you wrote on Day 14 appear the same way).

### Block 7: `__name__` in action

```python
print("This file's __name__ is:", __name__)
print("mytools' __name__ is:", mytools.__name__)
```

**What it does:** prints `__main__` for the file you ran, and `mytools` for the imported one. Now look at the bottom of `mytools.py`:

```python
if __name__ == "__main__":
    print("Testing mytools directly")
```

When you run `day17_modules.py`, importing `mytools` does **not** trigger that test block, because inside `mytools`, `__name__` is `"mytools"`. Run `python3 mytools.py` directly and the block **does** run. This is how a file can be **both a reusable library and a runnable script**, and it is why every `dayNN` file in your repo ends with that same pattern.

## 6. How the blocks connect

```
Blocks 1 to 4   USE modules others wrote (standard library)
Block 5         USE a module YOU wrote (same mechanism!)
Block 6         EXPLORE any module (dir, help)
Block 7         explains how one file can be both library and script
```

The idea: **there is no difference between a "built-in" module and your own**. Both are files you import.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Naming your file `random.py` or `math.py` | your file shadows the real one, weird errors | pick unique names |
| `ModuleNotFoundError` for your own file | wrong folder / typo | run from the folder, check spelling (no `.py` in the import) |
| Forgetting the `math.` prefix after `import math` | `NameError` | `math.sqrt` |
| Using `from x import *` | name clashes, unclear code | import explicitly |
| Circular imports (A imports B, B imports A) | `ImportError` | move shared code into a third module |
| Putting test code at module top level | runs on every import | put it under `if __name__ == "__main__":` |

## 8. Practice

1. Fill in `day17_modules.py`: use `random` to simulate rolling two dice 10 times and print the totals.
2. Use `datetime` to print today's weekday name and the number of days until the end of the year.
3. Create `validators.py` with your `ask_int` (Day 16) and `is_even` (Day 14). Import and use them from another file.
4. Use `collections.Counter` to find the 3 most common words in a sentence (`.most_common(3)`).
5. Use `os.listdir()` to list the files in your `week1_basics` folder.
6. Explore: `import this` (a poem about Python's philosophy).

## 9. Self-check

- What is a module, physically?
- What is the difference between `import math` and `from math import sqrt`?
- What does `if __name__ == "__main__":` protect against?
- Why should you avoid `from module import *`?

**Next:** Day 18: bundle **data and functions together** into your own types with classes.

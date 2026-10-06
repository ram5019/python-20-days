# Day 20: Final Project, Student Record Manager

**Time:** ~3 to 4 hours | **Example:** `examples/day20_student_manager.py` | **Your practice file:** `week4_realworld/day20_student_manager.py`

---

## 1. The big idea

You have learned the pieces. Today you assemble them into one **complete, usable program** that stores data permanently, validates input, survives mistakes, and presents a menu. The real lesson is **how to organise a program in layers** so it stays understandable.

## 2. Why does this exist?

Small exercises teach syntax. A project teaches **design**: which function does what, where data lives, how errors are handled, how pieces talk to each other. This pattern (menu, load data, act, save data) is the skeleton of countless real tools: inventory trackers, ticket systems, CLI utilities.

Your existing `day20_student_manager.py` already works. The example version keeps the same idea but adds validation, safe loading, update/delete, and a cleaner structure. Compare them line by line to see what each improvement buys you.

## 3. Simple way to understand

A **small restaurant**:

| Restaurant | Program layer |
|-----------|---------------|
| Storage room (ingredients kept safely) | **Layer 1: storage** (load/save JSON) |
| Waiter who checks the order makes sense | **Layer 2: input helpers** (validation) |
| Chef's recipes (rules, no talking to customers) | **Layer 3: logic** (pure functions) |
| Workflows: take order → cook → store → serve | **Layer 4: actions** |
| The head waiter running the evening | **Layer 5: `main` menu loop** |

Each layer only talks to the one below it. If you change how ingredients are stored (CSV instead of JSON), the chef's recipes do not change.

## 4. How it works: the data and the flow

### The data shape

```python
students = [
    {"name": "Asha",  "marks": 88.0},
    {"name": "Meena", "marks": 95.0},
]
```

A **list of dicts** (Day 13, Block 6). It lives in memory while the program runs and is saved to JSON after every change.

### The program flow

```
start
  │
  ▼
load_students()  ──► students (list in memory)
  │
  ▼
┌─► show MENU ─► read choice ─► call an action ─┐
│                                │              │
│            (action may call input helpers,    │
│             logic functions, save_students)   │
└────────────────────────────────◄──────────────┘
  │ choice 6
  ▼
exit
```

## 5. Code walkthrough, layer by layer

### Setup

```python
import json
from pathlib import Path
DATA_FILE = Path(__file__).parent / "students_demo.json"
```

**What it does:** imports (Day 17) and defines the data file's location relative to the script (Day 15). It is a **constant** (UPPER_CASE by convention), so the filename is defined **in one place**.

### Layer 1: storage

```python
def load_students():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: data file is corrupted...")
        return []

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)
```

**What it does:** the only two functions that touch the disk. `load_students` always returns a list: empty on first run or on a damaged file (Days 15, 16, 19). `save_students` writes the whole list. **Why isolate this?** If you later switch to a database, only these two change.

Compare with your original: `json.load(open(FILE)) if os.path.exists(FILE) else []` crashes if the file is corrupted, and `open(...)` without `with` is never explicitly closed.

### Layer 2: input helpers

```python
def ask_name():
    while True:
        name = input("Name: ").strip().title()
        if name:
            return name
        print("Name cannot be empty.")

def ask_marks():
    while True:
        try:
            marks = float(input("Marks (0-100): "))
        except ValueError:
            print("Please type a number.")
            continue
        if 0 <= marks <= 100:
            return marks
        print("Marks must be between 0 and 100.")
```

**What it does:** each function **keeps asking until the answer is acceptable**, then returns it (the `ask_int` pattern from Day 16).
- `ask_name`: strip spaces (Day 3), normalise capitalisation, reject empty (truthiness, Day 6).
- `ask_marks`: `try/except` catches non-numbers; `continue` skips to the next round; the chained comparison checks the range.

Because the rest of the program receives only **clean data**, it never has to re-check it.

### Layer 3: logic (pure functions)

```python
def find_student(students, name): ...
def average_marks(students): ...
def topper(students): ...
def grade_for(marks): ...
```

**What it does:** these take data in and give data out. They do **not** use `input`, `print` or files. That makes them predictable and easy to test: `grade_for(80)` is always `"B"`.
- `find_student` loops (Day 8) comparing lowercase names so `asha` matches `Asha`, returning the dict or `None`.
- `average_marks` guards against an empty list (Day 14) and uses a generator expression inside `sum`.
- `topper` uses `max(..., key=lambda ...)` from Day 13.
- `grade_for` is the Day 6 `elif` chain; **the order of conditions matters** (highest first).

### Layer 4: actions

```python
def add_student(students):
    name = ask_name()
    if find_student(students, name):
        print(f"{name} already exists. Use Update instead.")
        return
    students.append({"name": name, "marks": ask_marks()})
    save_students(students)
    print("Added.")
```

**What it does:** the glue. One action reads like the plan:
1. **Input**: `ask_name()` (Layer 2).
2. **Check**: `find_student` (Layer 3); stop early if it is a duplicate.
3. **Change data**: `students.append(...)` (Day 11).
4. **Persist**: `save_students` (Layer 1).
5. **Feedback**: `print`.

`update_student` and `delete_student` follow the same recipe. Note `update` modifies the dict that `find_student` returned. Because dicts are mutable and shared (Day 10 aliasing), changing it changes the one inside `students`. That is why no extra step is needed before `save_students`.

`show_all` formats a table with f-string alignment: `{'Name':<15}` left-aligns in 15 characters, `{marks:>8.1f}` right-aligns a number with one decimal. `sorted(..., key=...)` displays alphabetically **without changing** the stored order (Day 11: `sorted` returns a new list).

### Layer 5: `main()`

```python
def main():
    students = load_students()
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "1":
            add_student(students)
        ...
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
```

**What it does:** loads the data **once**, then loops forever (`while True`, Day 9) until the user picks 6 (`break`). An `if/elif` chain (Day 6) routes each choice to an action. The same `students` list is passed to every action, so they all work on the same data. `MENU` is a triple-quoted string defined at the top so the layout is easy to edit.

### Entry point

```python
if __name__ == "__main__":
    main()
```

**What it does:** runs `main()` only if you launch the file directly (Day 17).

## 6. How the blocks connect

```
            main (menu loop)
              │ calls
              ▼
          actions  ──────────────┐
  add / update / delete          │
  show_all / show_stats          │
     │          │          │     │
     ▼          ▼          ▼     ▼
 input      logic        storage
 helpers    find_student  load_students
 ask_name   average       save_students
 ask_marks  topper             │
            grade_for          ▼
                           JSON file
```

Which day appears where:

| Piece | Days used |
|-------|-----------|
| Layer 1 storage | 15 (files), 16 (errors), 19 (JSON) |
| Layer 2 helpers | 3 (strings), 4 (input), 9 (while), 16 (try/except) |
| Layer 3 logic | 6 (if), 8 (for), 13 (dict), 14 (functions) |
| Layer 4 actions | 10 and 11 (lists), 13 (dicts), 14 (functions) |
| Layer 5 main | 6, 9, 17 |

Every earlier day shows up. That is the point.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Forgetting `save_students` after a change | data lost on exit | save after every modification |
| Loading inside the loop each time | slow and loses unsaved changes | load once in `main` |
| Mixing `print`/`input` into logic functions | impossible to test or reuse | keep Layer 3 pure |
| Case-sensitive name matching | "asha" not found | compare `.lower()` |
| Removing items while looping over the same list | skipped items | find first, then remove (as `delete_student` does) |
| Storing marks as text | cannot calculate | `float(...)` in `ask_marks` |
| One giant `main()` with everything inline | unreadable | one function per job |

## 8. Practice and extensions

Work through them in this order, running the program after each.

1. Fill in `week4_realworld/day20_student_manager.py`: **start from your working version**, then apply one improvement at a time from the example (safe loading, then validation, then update/delete).
2. Add a **search** option (names that *contain* a text).
3. Add **subjects**: each student gets a `{"math": 80, "science": 90}` dict, and show the per-subject average.
4. Add **export to CSV** with Python's `csv` module (Day 27 preview).
5. Convert the student dict into a `Student` class (Day 18) with `to_dict()` and `from_dict()` methods for saving and loading.
6. Write a few **tests** in a separate file: `assert grade_for(90) == "A"` and so on. This is where pure functions pay off.
7. Change the project to manage something from your own work: tickets, clusters, runbooks. Only the field names change; the layers stay the same.

## 9. Self-check

- Why is `grade_for` a pure function, and why does that help?
- Why does `update_student` not need to copy the dict before changing it?
- Where would you change code if you switched from JSON to a database?
- Why is `load_students()` called once in `main` and not in each action?
- Trace what happens, function by function, when the user chooses "1. Add student".

---

## You have finished the 20 days

You now know:

| Area | Skills |
|------|--------|
| **Data** | strings, numbers, booleans, lists, tuples, sets, dicts |
| **Flow** | conditions, for loops, while loops |
| **Structure** | functions, modules, classes |
| **Real world** | files, JSON, error handling |
| **Design** | layering a program, separating input, logic and storage |

**Where next:** your `advanced/` folder (Days 21 to 28): comprehensions, lambda/map/filter, decorators, generators, virtual environments, APIs, CSV/JSON, and a weather CLI. Beyond that, pick a real problem from your own work, such as parsing log files or calling an API, and build it. That is how the skills become permanent.

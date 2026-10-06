# Python in 20 Days: Learning Path

A guided path from "what is a variable?" to a working record-keeping program.
Each day has **one lesson** (`dayNN_*.md`) and **one runnable example** (`examples/dayNN_*.py`).

Your existing practice stubs (`week1_basics/`, `week2_logic/`, ...) stay as they are.
Each lesson tells you which stub to fill in after you finish reading.

---

## How to use each day (about 1.5 to 2.5 hours)

1. **Read** the lesson (20 min). Do not skip "Simple way to understand".
2. **Run** the example: `python3 learning-path/examples/dayNN_*.py`
3. **Change** it. Break it on purpose. Read the error message.
4. **Practice**: fill in your stub file for that day plus the tasks in the lesson.
5. **Self-check**: answer the questions at the bottom without looking.

> Rule of thumb: if you only read, you will forget. If you type and break things, you will remember.

---

## The 20-day map

| Week | Day | Topic | One-line purpose | Your practice file |
|------|-----|-------|------------------|--------------------|
| **1: Basics** | 1 | Hello Python, print, running code | Make the computer show something | `week1_basics/day01_hello.py` |
| | 2 | Variables and data types | Give names to data so you can reuse it | `day02_variables.py` |
| | 3 | Strings | Work with text | `day03_strings.py` |
| | 4 | Input | Let the user give your program data | `day04_input.py` |
| | 5 | Operators | Calculate and compare | `day05_operators.py` |
| | 6 | Conditionals (if/elif/else) | Make decisions | `day06_conditionals.py` |
| | 7 | Mini project: age calculator | Combine days 1 to 6 | `day07_age_calculator.py` |
| **2: Logic** | 8 | for loops | Repeat things a known number of times | `week2_logic/day08_for_loop.py` |
| | 9 | while loops | Repeat until something changes | `day09_while_loop.py` |
| | 10 | Lists | Store many items in order | `day10_lists.py` |
| | 11 | List methods | Add, remove, sort, search | `day11_list_methods.py` |
| | 12 | Tuples and sets | Fixed data and unique data | `day12_tuples_sets.py` |
| | 13 | Dictionaries | Look things up by name | `day13_dictionaries.py` |
| | 14 | Functions | Package code to reuse it | `day14_functions.py` |
| **3: Structure** | 15 | Files | Save and load data on disk | `week3_structure/day15_files.py` |
| | 16 | Errors and exceptions | Survive bad input and failures | `day16_errors.py` |
| | 17 | Modules and imports | Reuse code written by others | `day17_modules.py` |
| | 18 | OOP: classes and objects | Model real things in code | `day18_oop.py` |
| **4: Real world** | 19 | JSON | Exchange structured data | `week4_realworld/day19_json.py` |
| | 20 | Final project: student manager | Everything together | `day20_student_manager.py` |

After day 20, continue with the **advanced path** in [`advanced/`](advanced/README.md): Days 21 to 28 (comprehensions, lambda, decorators, generators, venv, APIs, CSV/JSON, CLI tools) plus five specialisation tracks: Data Science (NumPy, Pandas, Matplotlib), Web (Flask, FastAPI, Django), Automation (BeautifulSoup, Selenium), AI/ML (scikit-learn, PyTorch) and Cloud/DevOps (boto3, Azure SDK, OCI SDK). Your own `advanced/` stubs at the repo root map to Days 21 to 28.

---

## The big picture: how the days build on each other

```
Day 1  print()         ──► output
Day 2  variables       ──► remember data
Day 3  strings         ──► text is a data type
Day 4  input()         ──► data comes IN from the user
Day 5  operators       ──► transform and compare data
Day 6  if/else         ──► choose what runs, using comparisons
Day 7  PROJECT         ──► 1 to 6 working together
                              │
Day 8  for             ──► repeat
Day 9  while           ──► repeat with a condition (uses Day 6)
Day 10 list            ──► many values in one variable (for loops over it)
Day 11 list methods    ──► change that collection
Day 12 tuple / set     ──► variations on the collection idea
Day 13 dict            ──► collection with named slots
Day 14 function        ──► package any of the above for reuse
                              │
Day 15 files           ──► data survives after the program ends
Day 16 errors          ──► files and input fail; handle it
Day 17 modules         ──► your code in many files, plus the standard library
Day 18 classes         ──► bundle data (Day 13 idea) with functions (Day 14)
Day 19 JSON            ──► dict/list  <──►  text file
Day 20 PROJECT         ──► functions + dict + list + files + JSON + loops + errors
```

Three ideas run through everything:

1. **Data**: variables, lists, dicts hold it.
2. **Flow**: if, for, while decide what runs and how often.
3. **Packaging**: functions, modules, classes organise code so it stays readable.

---

## Setup (once)

```bash
cd ~/Desktop/python-20-days
python3 --version          # should print 3.9 or newer
python3 learning-path/examples/day01_hello.py
```

Tip: in the terminal, `python3` with no file name opens an interactive prompt (REPL) where you can try one line at a time. Exit with `exit()`.

---

## Reading order for the "why / how / purpose" parts

Every lesson uses the same sections so you always know where to look:

| Section | Answers |
|---------|---------|
| The big idea | **What** is it? |
| Why it exists | **Why** do we need it? What problem does it solve? |
| Simple way to understand | An everyday analogy |
| How it works | **How**: syntax and rules |
| Code walkthrough | What each block does, line by line |
| How the blocks connect | The relationship between blocks |
| Common mistakes | What will go wrong for you, and why |
| Practice and self-check | Make it stick |

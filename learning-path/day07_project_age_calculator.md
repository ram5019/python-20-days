# Day 7: Mini Project, Age Calculator

**Time:** ~2 hours | **Example:** `examples/day07_age_calculator.py` | **Your practice file:** `week1_basics/day07_age_calculator.py`

---

## 1. The big idea

Today you write nothing new. You **combine** everything from Days 1 to 6 into one working program, and learn how to **split a program into small pieces** that each do one job.

## 2. Why does this exist?

Knowing separate tools is not the same as building something. A project teaches the skill that matters most: **breaking a problem into steps**, then writing each step and joining them.

## 3. Simple way to understand

A **kitchen assembly line**:

1. One person takes the order (**input**).
2. One cooks (**process**).
3. One decides how it should be plated (**decide**).
4. One serves (**output**).
5. A manager (**main**) tells each when to work.

Each worker does one job well. If the plating is wrong, you fix the plater, not the cook.

## 4. How it works: the plan

Before coding, write the plan in plain words:

```
1. Ask the name and the birth year.
2. Check the year makes sense.
3. Age = this year - birth year.
4. Decide the life stage from the age.
5. Print a friendly result.
```

Each step becomes **one small function**. You will study functions properly on Day 14. For now, read `def name(inputs): ... return result` as **"a named recipe that hands back an answer"**.

## 5. Code walkthrough, block by block

### Block 0: the import

```python
from datetime import datetime
```

**What it does:** brings in a ready-made tool from Python's standard library so you do not have to know today's date yourself. `datetime.now().year` gives the current year. This is a first look at **modules** (Day 17).

### Block 1: INPUT

```python
def get_birth_year():
    text = input("Birth year (e.g. 1988): ").strip()
    return int(text)
```

**What it does:** asks, cleans (`strip`, Day 3), converts (`int`, Day 4) and **returns** the number. `return` hands the value back to whoever called the function.

### Block 2: PROCESS

```python
def calculate_age(birth_year, current_year):
    return current_year - birth_year
```

**What it does:** pure arithmetic (Day 5). It takes two numbers in and gives one back. It does not print or ask anything, so it is easy to test: `calculate_age(2000, 2026)` is always `26`.

### Block 3: DECIDE

```python
def life_stage(age):
    if age < 0:
        return "not born yet"
    elif age < 13:
        return "child"
    ...
```

**What it does:** an `elif` chain (Day 6) that maps a number to a label. Checks go from **lowest to highest**, so the first match wins. A `return` ends the function immediately, so no `else` is needed between branches.

### Block 4: OUTPUT

```python
def show_result(name, age, stage):
    print(f"\nHello, {name.title()}!")
    print(f"You are about {age} years old ({stage}).")
```

**What it does:** f-strings (Day 3) turn the data into sentences. `\n` adds a blank line. `.title()` fixes `"ram"` → `"Ram"`.

### Block 5: `main()`, the manager

```python
def main():
    name = input("Your name: ").strip()
    birth_year = get_birth_year()
    current_year = datetime.now().year

    if birth_year > current_year:
        print("That year is in the future!")
        return

    age = calculate_age(birth_year, current_year)
    stage = life_stage(age)
    show_result(name, age, stage)
```

**What it does:** calls each worker **in order** and passes data between them:

```
get_birth_year() ──► birth_year ─┐
datetime.now()   ──► current_year┴─► calculate_age() ──► age ──► life_stage() ──► stage
                                                          └────────────┬──────────────┘
                                                                       ▼
                                                           show_result(name, age, stage)
```

The guard `if birth_year > current_year` stops early with a message if the data is nonsense. `return` with nothing simply exits `main`.

## 6. How the blocks connect

| Block | Takes in | Gives out | Day used |
|-------|----------|-----------|----------|
| 1 get_birth_year | (user typing) | `int` year | 3, 4 |
| 2 calculate_age | two years | age | 5 |
| 3 life_stage | age | label (str) | 6 |
| 4 show_result | name, age, label | prints | 1, 3 |
| 5 main | none | none (runs the flow) | all |

**Key lesson:** blocks do not touch each other's variables. They communicate only through **arguments (in)** and **return values (out)**. That is why you can change one without breaking the others.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Function defined but never called | nothing happens | call `main()` |
| Using `print` instead of `return` in a calculation | caller gets `None` | `return` the value |
| Calling `calculate_age()` with one argument | `TypeError` | pass both |
| Typing a name as the year | `ValueError` | Day 16 handles this |
| Birth year with a typo like 19988 | negative age | validate (see the guard in `main`) |

## 8. Practice

1. Open your stub `day07_age_calculator.py`. It already works. Run it, then split it into the 4 blocks above.
2. Add the input check: reject years before 1900.
3. Add "days until your next birthday" using `datetime` (ask for month and day too).
4. Add a menu: "1) age 2) life stage 3) quit" using `if/elif`.
5. Explain in words what each function takes in and gives out.

## 9. Self-check

- Why is it better to split the program into functions than to write it top to bottom?
- How do functions pass data to each other?
- What does `return` do?
- What would break if `life_stage` checked `age < 60` before `age < 13`?

**Next:** Week 2. You can now decide. Next you will **repeat**: loops.

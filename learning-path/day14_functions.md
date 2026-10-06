# Day 14: Functions

**Time:** ~2.5 hours | **Example:** `examples/day14_functions.py` | **Your practice file:** `week2_logic/day14_functions.py`

---

## 1. The big idea

A **function** is a **named, reusable block of code**. You define it once and **call** it whenever you need it. It can take **inputs (parameters)** and give back an **output (return value)**.

## 2. Why does this exist?

Three reasons, in order of importance:

1. **Don't Repeat Yourself (DRY).** Without functions you copy-paste the same code, then fix a bug in five places.
2. **Readability.** `calculate_tax(price)` explains itself; ten lines of maths do not.
3. **Testing and teamwork.** A small function with clear inputs and outputs is easy to test and easy for someone else to use without reading its insides.

You have already **used** functions: `print`, `len`, `input`, `range`, `sum`. Today you write your own. Day 7 used them without explanation, and now you see how they work.

## 3. Simple way to understand

A function is a **vending machine** or a **recipe card**.

```
   inputs                   machine                 output
 (parameters)  ───►   [ the code inside ]   ───►  (return value)
 coin + button         you don't need to know      a snack
                       how it works inside
```

- **Define** = build the machine (nothing is dispensed yet).
- **Call** = press the button.
- **Parameters** = the coin and button choice.
- **Return** = the snack that drops out.

Anyone can use the machine without knowing what happens inside. That is called **abstraction**.

## 4. How it works

```python
def function_name(parameter1, parameter2):
    """Optional docstring: what it does."""
    # body
    return result
```

| Term | Meaning |
|------|---------|
| `def` | keyword that starts a definition |
| **parameter** | the variable name in the definition (`a`, `b`) |
| **argument** | the actual value you pass when calling (`3`, `4`) |
| `return` | sends a value back **and exits the function immediately** |
| no `return` | function returns `None` |
| default value | `exp=2` lets callers omit that argument |

## 5. Code walkthrough, block by block

### Block 1: define and call

```python
def greet():
    print("Hello from a function!")

greet()
greet()
```

**What it does:** `def` stores the recipe; nothing prints yet. Each `greet()` **runs** it. Two calls, two messages. The code was written once and used twice.

### Block 2: parameters

```python
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Ram")
```

**What it does:** `name` is a placeholder. When you call `greet_person("Ram")`, `name` becomes `"Ram"` **for that call only**. The function now works for any person.

### Block 3: return

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(add(add(1, 2), 3))
```

**What it does:** `return` sends the answer back to the **place that called** the function, so `add(3, 4)` is *replaced by* `7`, and `result = 7`. Because a call becomes a value, you can nest: `add(add(1, 2), 3)` → `add(3, 3)` → `6`. The inner call runs first.

### Block 4: `print` vs `return`

```python
def show_square(n):
    print(n * n)

def get_square(n):
    return n * n

x = show_square(4)    # prints 16
y = get_square(4)     # prints nothing
print(x, y)           # None 16
```

**What it does:** this is the single most important distinction in the lesson.
- `print` **shows** something to a human. The program gets nothing back (`None`).
- `return` **hands** something to the program, so it can store it, compare it or pass it on.

Rule: **calculations should `return`. Only the outer layer (like `main`) should `print`.** That is how Day 7's design worked.

### Block 5: default and keyword arguments

```python
def power(base, exp=2):
    return base ** exp

power(5)                # 25
power(2, 10)            # 1024
power(exp=3, base=2)    # 8
```

**What it does:** `exp=2` is a **default**, used when the caller does not provide it. You can pass arguments by **position** (`2, 10`) or **by name** (`exp=3, base=2`). Names make calls readable and let you change the order. (Same idea as `sep=` and `end=` in `print`, Day 1.)

### Block 6: scope

```python
counter = 100

def change_local():
    counter = 1
    return counter

print(change_local())   # 1
print(counter)          # 100
```

**What it does:** a variable created **inside** a function is **local**: it exists only while the function runs and does not touch a variable of the same name outside. The global `counter` stays 100. This isolation is a feature: functions cannot accidentally break each other. (Avoid the `global` keyword at this stage. Prefer passing in and returning values.)

### Block 7: lists and docstrings

```python
def average(numbers):
    """Return the average of a list of numbers, or 0 if empty."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```

**What it does:**
- The triple-quoted **docstring** documents the function. `help(average)` will show it.
- `if not numbers:` is the truthiness check from Day 6: an empty list is falsy, so it guards against dividing by zero.
- The early `return 0` **exits immediately**, so the last line only runs for non-empty lists.
- It uses `sum`, `len` (Day 10) and division (Day 5), all in a tidy package.

Note: if you pass a **list** and the function **modifies** it (e.g. `append`), the caller's list changes too. That is the aliasing issue from Day 10.

### Block 8: functions calling functions

```python
def is_even(n):
    return n % 2 == 0

def count_evens(numbers):
    count = 0
    for n in numbers:
        if is_even(n):
            count += 1
    return count
```

**What it does:** `count_evens` **uses** `is_even`. Each function has **one small job**. `is_even` answers a question; `count_evens` loops, calls it, and counts. This layering is how large programs are built: small functions combined into bigger ones, just as in Day 7.

## 6. How the blocks connect

```
Block 1  a function with no inputs
Block 2  + inputs (parameters)
Block 3  + output (return)
Block 4  clarify: output is return, NOT print
Block 5  make inputs flexible (defaults, names)
Block 6  understand what is visible where (scope)
Block 7  apply to real data (lists) with a docstring and a guard
Block 8  build bigger functions from smaller ones
```

Growth path: **nothing in, nothing out → in → in and out → flexible → safe → composed.**

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Defining but never calling | nothing happens | call it |
| `print` where you meant `return` | caller gets `None` | `return` |
| Code after `return` | never runs | return should be the last step in that path |
| Wrong number of arguments | `TypeError` | match the parameters |
| Mutable default `def f(x=[])` | list shared across calls | use `None`, then create inside |
| Calling before defining | `NameError` | define above the call |
| Expecting a local variable to exist outside | `NameError` | return it |

## 8. Practice

1. Fill in `day14_functions.py`: write `square(n)`, `is_even(n)` and `greet(name, greeting="Hello")`.
2. Write `max_of_three(a, b, c)` without using `max`.
3. Write `is_prime(n)` returning True/False, then print all primes up to 50 using it.
4. Write `celsius_to_fahrenheit(c)` and a loop that prints a table for 0 to 100 in steps of 10.
5. Refactor your Day 6 grade program: make `get_grade(marks)` return a letter, and have the main code only print.
6. Write `word_count(text)` returning a dictionary of counts (Day 13, Block 5).

## 9. Self-check

- What is the difference between a parameter and an argument?
- What does a function return if it has no `return` statement?
- Why should calculations `return` instead of `print`?
- Why can a local variable not change a global one?

**Next:** Week 3. Now your programs need to **last** (files), **survive** (errors), **grow** (modules) and **model things** (classes).

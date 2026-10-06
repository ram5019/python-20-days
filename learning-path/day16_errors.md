# Day 16: Errors and Exceptions

**Time:** ~2 hours | **Example:** `examples/day16_errors.py` | **Your practice file:** `week3_structure/day16_errors.py`

---

## 1. The big idea

When something goes wrong, Python **raises an exception** and, if nobody handles it, the program **crashes**. With `try / except` you **catch** the problem, respond sensibly, and keep running.

## 2. Why does this exist?

You have already seen the problems:

- Day 4: the user types `abc` where you wanted a number → `ValueError`.
- Day 15: the file does not exist → `FileNotFoundError`.
- Dividing by zero, using a missing key, losing the network...

You cannot control the outside world, but you **can** decide how your program reacts. Good software does not crash; it reports the problem clearly and recovers or exits gracefully.

## 3. Simple way to understand

A **safety net under a trapeze artist**.

- `try:` = "I'm going to attempt something risky."
- `except:` = "If I fall, here is the net, and this is what happens next."
- `else:` = "If I did NOT fall, do this."
- `finally:` = "Either way, tidy up the equipment."

Without the net, one fall ends the show. With it, the show goes on.

Another view: **an error is not the enemy. It is information.** The message tells you exactly what happened.

## 4. How it works

```python
try:
    # risky code
except SpecificError as e:
    # what to do if that error happens
else:
    # runs only if no error happened
finally:
    # always runs
```

Execution rules:

1. Python runs the `try` block line by line.
2. At the **first error**, it **jumps immediately** to the matching `except`. The rest of the `try` is skipped.
3. No error → `except` is skipped, `else` runs.
4. `finally` always runs last.

### Common exceptions

| Exception | Typical cause |
|-----------|---------------|
| `ValueError` | `int("abc")` |
| `TypeError` | `"5" + 3` |
| `ZeroDivisionError` | `10 / 0` |
| `KeyError` | `d["missing"]` |
| `IndexError` | `lst[99]` |
| `FileNotFoundError` | opening a missing file |
| `NameError` | using a variable that does not exist |

## 5. Code walkthrough, block by block

### Block 1: the uncaught error (commented out)

```python
# print(10 / 0)
```

**What it does:** if you remove the `#` the program stops with a traceback. Try it once, read the **last line** (`ZeroDivisionError: division by zero`), and put the `#` back. Knowing how to read this is a skill in itself.

### Block 2: `try / except`

```python
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")
print("Program continues")
```

**What it does:** the error occurs in the `try`, Python jumps to the matching `except`, prints the message, then continues normally. Note `"Program continues"` still prints: **the program survived**.

### Block 3: the error message with `as e`

```python
try:
    number = int("abc")
except ValueError as e:
    print("Bad number:", e)
```

**What it does:** `as e` stores the exception object so you can print Python's own explanation: `invalid literal for int() with base 10: 'abc'`. Useful for logs.

### Block 4: several `except` blocks

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "cannot divide by zero"
    except TypeError:
        return "both values must be numbers"
```

**What it does:** different problems get different responses. Python checks the `except` blocks top to bottom and runs the **first match**. Always catch **specific** errors rather than a bare `except:`, which hides bugs including your own typos. This also uses Day 14 (function with `return` inside `try`).

### Block 5: `else` and `finally`

```python
try:
    value = int("42")
except ValueError:
    print("not a number")
else:
    print("Converted OK:", value)
finally:
    print("Always runs (cleanup)")
```

**What it does:**
- `else` runs **only when there was no error**, which keeps the success path separate from the risky line.
- `finally` runs **no matter what**: closing connections, deleting temp files, printing "done".

(The `with open(...)` statement from Day 15 is essentially a built-in `finally` that closes the file.)

### Block 6: a robust input function

```python
def ask_int(prompt):
    while True:
        text = input(prompt)
        try:
            return int(text)
        except ValueError:
            print("Please type a whole number.")
```

**What it does:** this is the **payoff block**. It combines three earlier days:
- Day 9: `while True` keeps asking.
- Day 4: `input` and `int`.
- Day 16: `try/except` catches the bad input.

Valid input → `return` exits the function and the loop. Invalid → message, loop again. This fixes the crashing problem from Day 4 for good, and you can reuse `ask_int` in every project.

### Block 7: safe file reading

```python
def read_file_safely(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None
```

**What it does:** solves Day 15's missing-file problem. The function either returns the text or `None`. The **caller** decides what to do with `None`. This follows the Day 14 rule: functions return results; they do not decide how to show them.

### Block 8: raising your own error

```python
def set_age(age):
    if age < 0:
        raise ValueError("age cannot be negative")
    return age
```

**What it does:** `raise` creates an error **on purpose** when data breaks a rule. The caller can catch it as in Block 3. This is how a function says "I cannot do this, and here is why", rather than silently returning wrong data.

## 6. How the blocks connect

```
Block 1  see the problem
Block 2  catch it                      (basic net)
Block 3  read the message              (as e)
Block 4  respond differently per type  (multiple except)
Block 5  success path / cleanup path   (else, finally)
Block 6  apply to INPUT   ← Days 4 + 9
Block 7  apply to FILES   ← Day 15
Block 8  CREATE errors yourself        (raise)
```

Two directions: **handling** errors that others cause (1 to 7) and **raising** errors when you detect bad data (8).

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Bare `except:` | hides real bugs | name the exception |
| `try` block too big | unclear what failed | wrap only the risky line |
| Silent `except: pass` | problems vanish | at least print or log |
| Wrong exception type | not caught, still crashes | read the traceback's last line for the right name |
| Catching an error to hide a logic mistake | wrong results | fix the bug instead |
| Exceptions for normal flow when `if` is simpler | harder to read | use `if` for expected cases like "is the list empty?" |

## 8. Practice

1. Fill in `day16_errors.py`: ask for two numbers and divide them. Handle bad text **and** divide-by-zero with different messages.
2. Write `ask_float(prompt)` like `ask_int`.
3. Write `ask_choice(prompt, options)` that repeats until the answer is in the list of options.
4. Read a file chosen by the user. If it is missing, ask again (up to 3 tries).
5. Write `get_item(lst, index)` that returns the item or `None` if the index is invalid.
6. Update your Day 9 guessing game so typing letters does not crash it.

## 9. Self-check

- What happens to the rest of the `try` block after an error?
- When does `else` run? When does `finally` run?
- Why is a bare `except:` risky?
- What does `raise` do and when would you use it?

**Next:** Day 17: your code is getting big. Learn to split it into **modules** and use Python's built-in library.

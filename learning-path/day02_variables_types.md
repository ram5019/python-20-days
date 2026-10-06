# Day 2: Variables and Data Types

**Time:** ~2 hours | **Example:** `examples/day02_variables.py` | **Your practice file:** `week1_basics/day02_variables.py`

---

## 1. The big idea

A **variable** is a name that points to a value stored in memory.

```python
age = 38
```

Read it as "the name `age` now refers to the value `38`". Every value also has a **type** that says what kind of thing it is and what you can do with it.

## 2. Why does this exist?

Without variables you would retype values everywhere:

```python
print("Ram is 38")
print("Ram will be 39 next year")
```

If the name changes, you must edit every line. With a variable you change **one place** and every use updates. Variables are also how a program **remembers** things while it runs: scores, names, totals.

Types exist because different data behaves differently. You can add two numbers, but "adding" two names means joining them. Python needs to know which one you mean.

## 3. Simple way to understand

A variable is a **sticky label on a box**.

- The box holds the value (`38`).
- The label is the name (`age`).
- `age = age + 1` takes the value out, calculates, puts the new value in, and sticks the label on the new box.

Types are like **box shapes**: a number box, a text box, a yes/no box. You can only do number things with number boxes.

## 4. How it works

### Creating a variable

`name = value`: the single `=` means **assign** (store), not "equals" like in maths.

### Naming rules

- Letters, digits, underscore. Cannot start with a digit.
- No spaces, no reserved words (`if`, `for`, `class`...).
- Convention: `snake_case` (`first_name`, `total_marks`).
- Pick names that explain themselves: `total_marks`, not `tm`.

### The four basic types

| Type | Name in Python | Example | Used for |
|------|----------------|---------|----------|
| Whole number | `int` | `38` | counts, ages |
| Decimal | `float` | `1.75` | measurements, prices |
| Text | `str` | `"Ram"` | names, messages |
| True/False | `bool` | `True` | yes/no answers, decisions |

Python works out the type from the value. You do not declare it.

## 5. Code walkthrough, block by block

### Block 1: create variables

```python
name = "Ram"
age = 38
height_m = 1.75
is_engineer = True
```

**What it does:** four assignments. Each line creates a name and attaches a value of a different type. `True` has a capital T and no quotes: it is a Python keyword.

### Block 2: use variables

```python
print(name, age, height_m, is_engineer)
```

**What it does:** Python replaces each name with its value, then prints. The variables you created in Block 1 are looked up here. **This is the link between blocks:** Block 2 only works because Block 1 ran first.

### Block 3: inspect types

```python
print(type(name))      # <class 'str'>
print(type(age))       # <class 'int'>
```

**What it does:** `type()` returns the type of a value. Use it whenever you are unsure what you are holding. It is your best debugging tool this week.

### Block 4: re-assignment

```python
age = age + 1
print("Next year:", age)
```

**What it does:** the right side runs first (`38 + 1 = 39`), then the result is stored back into `age`. The old value `38` is discarded. This pattern, updating a variable using its own value, appears in every counter and total you will ever write.

### Block 5: type conversion

```python
text_number = "10"
real_number = int(text_number)
print(real_number + 5)      # 15
print(text_number + "5")    # 105
```

**What it does:** `"10"` is text. `int("10")` converts it to the number `10`.
- `real_number + 5` → numeric addition → `15`.
- `text_number + "5"` → string joining → `"105"`.

Same symbol `+`, different behaviour because the **types** differ. This is the most important idea of the day, and on Day 4 it will matter because `input()` always gives you text.

Conversion functions: `int()`, `float()`, `str()`, `bool()`.

### Block 6: copying values

```python
a = 5
b = a
a = 99
print(a, b)     # 99 5
```

**What it does:** `b = a` copies the **value** `5`. Changing `a` afterwards does not affect `b`. For simple types (numbers, strings, booleans) variables are independent. Lists behave differently, and Day 10 covers that.

## 6. How the blocks connect

```
Block 1  create names ──► Block 2  read them
                      └─► Block 3  ask what type they are
                      └─► Block 4  change one (needs old value)
Block 5  convert between types (fixes type mismatches)
Block 6  how copying works
```

The flow is: **create → use → inspect → modify → convert**. That is the life of a variable.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `print(nme)` (typo) | `NameError: name 'nme' is not defined` | Check spelling; use the same name |
| `"5" + 3` | `TypeError: can only concatenate str` | `int("5") + 3` |
| `2name = "x"` | `SyntaxError` | Names cannot start with digits |
| Using `=` when you mean "is equal" | Wrong logic | Equality check is `==` (Day 5) |
| `int("abc")` | `ValueError` | Only convert text that looks like a number (Day 16 handles this safely) |

## 8. Practice

1. Fill in `day02_variables.py`: store your name, age, city and whether you like coffee. Print each with its `type()`.
2. Swap two variables `x = 1`, `y = 2` so that x is 2 and y is 1 (hint: use a third variable).
3. Store a price `499.99` and quantity `3`. Print the total.
4. Predict the output before running: `print("3" * 3)` and `print(3 * 3)`.

## 9. Self-check

- What does `=` do?
- What does `age = age + 1` do step by step?
- Why is `"10" + "5"` different from `10 + 5`?
- When would you use `type()`?

**Next:** Day 3 focuses on the type you will use most: strings.

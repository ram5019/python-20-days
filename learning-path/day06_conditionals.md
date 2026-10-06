# Day 6: Conditionals (if / elif / else)

**Time:** ~2 hours | **Example:** `examples/day06_conditionals.py` | **Your practice file:** `week1_basics/day06_conditionals.py`

---

## 1. The big idea

`if` runs a block of code **only when a condition is True**. `elif` adds more conditions to try. `else` is the fallback when nothing matched.

## 2. Why does this exist?

Until now every line always ran. Real programs must **choose**: is the password right? is the disk full? is the user old enough? Conditionals are what make software feel intelligent, because the same program behaves differently with different data.

## 3. Simple way to understand

A **fork in the road with signposts**.

- `if` → "If it's raining, take an umbrella."
- `elif` → "Otherwise, if it's sunny, wear a hat."
- `else` → "Otherwise, go as you are."

You only walk down **one** path. Python checks signposts from top to bottom and takes the **first one that is True**, then ignores the rest.

## 4. How it works

```python
if condition1:
    # runs if condition1 is True
elif condition2:
    # runs if condition1 was False and condition2 is True
else:
    # runs if none were True
```

Three rules:

1. The line ends with a **colon `:`**.
2. The block is **indented** (4 spaces). Indentation is part of the syntax.
3. `elif` and `else` are optional. `if` alone is fine.

**Truthiness:** conditions do not have to be True/False exactly. These count as **False**: `0`, `""` (empty string), `[]`, `None`, `False`. Almost everything else counts as **True**.

## 5. Code walkthrough, block by block

### Block 1: simple `if`

```python
temperature = 35
if temperature > 30:
    print("It's hot")
```

**What it does:** `temperature > 30` is a comparison (Day 5) that gives `True`. Because it is True, the indented line runs. Change the number to 20 and nothing prints because the block is skipped.

### Block 2: `if / else`

```python
age = 16
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

**What it does:** exactly one of the two blocks runs, never both, never neither. Use this when there are two outcomes.

### Block 3: `if / elif / else`

```python
marks = 72
if marks >= 90:
    grade = "A"
elif marks >= 75:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "F"
print("Grade:", grade)
```

**What it does:** Python tests top to bottom. `72 >= 90`? No. `72 >= 75`? No. `72 >= 60`? Yes, so `grade = "C"` and Python **skips everything else**.

**Why order matters:** if you put `marks >= 60` first, a score of 95 would stop there and get `C`. Always put the **most specific / highest** condition first.

The final `print` is **not indented**, so it is outside the chain and always runs. It uses the variable `grade` created inside the chain. **This is the link between the blocks:** the chain *sets* a variable and the print *reads* it.

### Block 4: combining conditions

```python
has_ticket = True
age = 20
if has_ticket and age >= 18:
    print("Entry allowed")
else:
    print("Entry denied")
```

**What it does:** uses `and` from Day 5 to merge two questions into one condition. Both must be True. Replace `and` with `or` and see how the behaviour changes.

### Block 5: nested `if`

```python
user = "admin"
password = "1234"
if user == "admin":
    if password == "1234":
        print("Welcome, admin")
    else:
        print("Wrong password")
else:
    print("Unknown user")
```

**What it does:** an `if` inside an `if`. The inner check runs **only if** the outer one passed. Each level adds 4 spaces. Use nesting when the second question only makes sense after the first is answered. (If you can flatten it with `and`, prefer that.)

*(Hard-coding a password is for learning only. Never do this in real code.)*

### Block 6: truthiness and the one-line form

```python
name = ""
if not name:
    print("Name is empty")

label = "even" if 10 % 2 == 0 else "odd"
```

**What it does:**
- An empty string is falsy, so `not name` is True. This is the idiomatic way to check "did the user type anything?".
- The last line is a **conditional expression**: `value_if_true if condition else value_if_false`. It is a compact if/else that produces a value. Good for simple cases only.

## 6. How the blocks connect

```
Day 5 comparison/logic ──► produces True/False ──► feeds every block here

Block 1: if                    one path or nothing
Block 2: if / else             two paths
Block 3: if / elif / else      many paths, first match wins
Block 4: and / or              build richer conditions
Block 5: nested                a decision inside a decision
Block 6: truthiness + 1-liner  shortcuts for common patterns
```

Complexity ladder: **1 branch → 2 → many → combined → nested**.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Missing `:` | `SyntaxError` | `if x > 5:` |
| Wrong indentation | `IndentationError` or logic bug | 4 spaces, consistent |
| `if x = 5:` | `SyntaxError` | `==` |
| Conditions in wrong order in `elif` chain | wrong grade | Put the strictest first |
| Using many `if`s instead of `elif` | multiple blocks run | Use `elif` when options are exclusive |
| Comparing input text to numbers: `if age > 18` where `age = input()` | `TypeError` | `int(input())` |

## 8. Practice

1. Fill in `day06_conditionals.py`: ask for a number and print positive, negative or zero.
2. Ask for marks and print the grade (A/B/C/F). Test the boundaries: 90, 89, 75, 60, 59.
3. Ask for a year and print leap year or not (use Day 5 logic).
4. Simple login: ask username and password, print `Welcome` or the right error message.
5. Triangle check: three sides, can they form a triangle? (Sum of any two > third.)
6. Rewrite your Task 1 using a one-line conditional expression.

## 9. Self-check

- What does Python do after the first True condition in an `elif` chain?
- Why must the `if` line end in `:`?
- Which of these are falsy: `0`, `"0"`, `""`, `[]`?
- When would you use `elif` rather than a second `if`?

**Next:** Day 7: combine Days 1 to 6 in one small project.

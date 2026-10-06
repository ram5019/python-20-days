# Day 5: Operators

**Time:** ~2 hours | **Example:** `examples/day05_operators.py` | **Your practice file:** `week1_basics/day05_operators.py`

---

## 1. The big idea

**Operators** are symbols that act on values. There are three families:

1. **Arithmetic**: calculate (`+ - * / // % **`)
2. **Comparison**: compare, giving `True` or `False` (`== != < > <= >=`)
3. **Logical**: combine True/False answers (`and or not`)

## 2. Why does this exist?

- Arithmetic is the PROCESS step of INPUT → PROCESS → OUTPUT.
- Comparison and logic are how a program **asks questions** about data. Tomorrow's `if` statements need a True/False answer, and these operators produce it.

Without comparison, a program can only calculate. With it, it can **decide**.

## 3. Simple way to understand

- **Arithmetic** = a calculator.
- **Comparison** = a referee who only answers yes or no. "Is 5 bigger than 10?" → `False`.
- **Logic** = a club doorman with rules. `and`: you need **both** the ticket **and** the ID. `or`: either one is enough. `not`: flips the answer.

Special pair to remember: `//` and `%` are like sharing sweets. 17 sweets among 5 kids: each gets `17 // 5 = 3`, and `17 % 5 = 2` are left over.

## 4. How it works

### Arithmetic

| Op | Meaning | Example | Result |
|----|---------|---------|--------|
| `+` `-` `*` | add, subtract, multiply | `17 * 5` | `85` |
| `/` | divide (always float) | `17 / 5` | `3.4` |
| `//` | floor divide | `17 // 5` | `3` |
| `%` | remainder (modulo) | `17 % 5` | `2` |
| `**` | power | `17 ** 2` | `289` |

Order: `**`, then `* / // %`, then `+ -`. Use parentheses when unsure.

### Comparison

`==` equal, `!=` not equal, `<`, `>`, `<=`, `>=`. They always return a bool.

**`=` stores, `==` compares.** Mixing these up is the classic mistake.

### Logical

| Op | True when |
|----|-----------|
| `a and b` | both are True |
| `a or b` | at least one is True |
| `not a` | `a` is False |

## 5. Code walkthrough, block by block

### Block 1: arithmetic

```python
a, b = 17, 5
print(a / b)     # 3.4
print(a // b)    # 3
print(a % b)     # 2
```

**What it does:** `a, b = 17, 5` assigns two variables on one line. Then every operator is tried on the same pair so you can compare results side by side. `/` always gives a decimal even if it divides evenly (`10 / 2` → `5.0`).

### Block 2: order of operations

```python
print(2 + 3 * 4)     # 14
print((2 + 3) * 4)   # 20
```

**What it does:** shows that multiplication binds tighter than addition, like in school maths. Parentheses override the default. When your formula looks confusing, add parentheses even if they are not needed. It helps the next reader.

### Block 3: shortcut assignment

```python
score = 10
score += 5
score *= 2
```

**What it does:** `score += 5` means `score = score + 5` (the Day 2 pattern, shortened). Then `score *= 2` doubles it. Result: `(10 + 5) * 2 = 30`. Every counter and running total uses this.

### Block 4: comparison

```python
print(5 == 5)    # True
print(5 != 3)    # True
print(5 > 10)    # False
```

**What it does:** each line asks a question and prints the yes/no answer. The output type is `bool`. **Look ahead:** Day 6 will put such a question directly after `if`.

### Block 5: logical operators

```python
age = 25
has_id = True
print(age >= 18 and has_id)    # True
print(age < 18 or has_id)      # True
print(not has_id)              # False
```

**What it does:** the first expression is evaluated in two steps. First `age >= 18` → `True`. Then `True and has_id` → `True`. Logic operators combine comparison answers into **bigger questions**. Here, "adult **and** has ID".

### Block 6: practical use of `%` and `//`

```python
n = 7
print("even" if n % 2 == 0 else "odd")
minutes = 135
print(minutes // 60, "hours", minutes % 60, "minutes")
```

**What it does:**
- Even/odd: an even number leaves remainder 0 when divided by 2. `n % 2 == 0` is a comparison built from an arithmetic result, and arithmetic feeding comparison is the key link of the day.
- Time split: `135 // 60 = 2` hours, `135 % 60 = 15` minutes left. Unit conversions and pagination (items per page) use exactly this.
- `"even" if ... else "odd"` is a one-line decision, previewed here. Tomorrow explains it.

## 6. How the blocks connect

```
Blocks 1 to 3: arithmetic ──► produce numbers
                 │
                 ▼  numbers go into...
Block 4: comparison ──► produces True/False
                 │
                 ▼  True/False go into...
Block 5: logical ──► combines True/False
                 │
                 ▼
Block 6: all three together to solve small problems → Day 6 if
```

It is a **pipeline**: numbers → booleans → decisions.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `if x = 5` | `SyntaxError` | Use `==` |
| `10 / 2` expecting `5` | gets `5.0` | Use `//` for whole numbers |
| `0.1 + 0.2 == 0.3` | `False`! (float rounding) | Use `round()` or `math.isclose` |
| `5 > 3 > 1` confusion | works but surprising | Break into `and` for clarity |
| `x == 1 or 2` | always truthy | Write `x == 1 or x == 2` |
| `"5" > 3` | `TypeError` | Convert first |

## 8. Practice

1. Fill in `day05_operators.py`: read two numbers, print every arithmetic result.
2. Ask for seconds, print as `H hours M minutes S seconds`.
3. Is a number divisible by both 3 and 5? Print True/False.
4. Ask for a year and print whether it is a leap year (divisible by 4 and not by 100, or divisible by 400).
5. Predict: `print(2 ** 3 ** 2)` and `print(-7 // 2)`. Then run.

## 9. Self-check

- Difference between `=` and `==`?
- What do `//` and `%` return for `17` and `5`?
- When is `a and b` True? `a or b`?
- Why does `/` return a float?

**Next:** Day 6: use True/False answers to choose which code runs.

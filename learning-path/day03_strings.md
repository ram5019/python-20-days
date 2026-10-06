# Day 3: Strings

**Time:** ~2 hours | **Example:** `examples/day03_strings.py` | **Your practice file:** `week1_basics/day03_strings.py`

---

## 1. The big idea

A **string** (`str`) is a sequence of characters: text. Python gives you tools to join, slice, search and clean text.

## 2. Why does this exist?

Most real data is text: names, emails, log lines, file paths, messages. As a support engineer you already read logs and error strings all day. Python lets you automate that: pull the hostname out of a log line, check whether a message contains "error", clean up user input.

## 3. Simple way to understand

A string is a **row of numbered lockers**, one character per locker.

```
 P  y  t  h  o  n
 0  1  2  3  4  5      ← positions counted from the left
-6 -5 -4 -3 -2 -1      ← positions counted from the right
```

- **Indexing** = open one locker: `word[0]` → `P`.
- **Slicing** = take a range of lockers: `word[0:3]` → `Pyt`.
- **Methods** = tools attached to the string, like `.upper()`.

Counting starts at **0**, not 1. This is the number one beginner trip-up.

## 4. How it works

| Task | Code | Result |
|------|------|--------|
| Join | `"a" + "b"` | `"ab"` |
| Repeat | `"ab" * 3` | `"ababab"` |
| Length | `len("hello")` | `5` |
| Insert variables | `f"Hi {name}"` | `"Hi Ram"` |
| Slice `[start:stop]` | `"Python"[0:3]` | `"Pyt"` (stop is **excluded**) |
| Step `[::step]` | `"Python"[::-1]` | `"nohtyP"` |

Common methods: `.lower()`, `.upper()`, `.strip()`, `.replace(a, b)`, `.split(sep)`, `.startswith()`, `.endswith()`, `.find()`.

## 5. Code walkthrough, block by block

### Block 1: join strings

```python
first = "Ramakrishna"
last = "Subbarao"
full = first + " " + last
```

**What it does:** `+` joins strings (this is **concatenation**). The `" "` in the middle adds the space, otherwise you would get `RamakrishnaSubbarao`. Joined text goes into a new variable, `full`.

### Block 2: f-strings

```python
age = 38
print(f"{first} is {age} years old")
```

**What it does:** the `f` before the quote turns on **formatting**. Anything in `{ }` is evaluated and inserted. Note `age` is an `int`, but the f-string converts it automatically. Without it you would need `str(age)`. **Link to previous block:** it reuses `first` from Block 1.

### Block 3: indexing and slicing

```python
word = "Python"
print(word[0])      # P
print(word[-1])     # n
print(word[0:3])    # Pyt
print(word[::-1])   # nohtyP
```

**What it does:**
- `[0]` first character; `[-1]` last character (negative = from the end).
- `[0:3]` characters at positions 0, 1, 2. Position 3 is excluded.
- `[::-1]` step of -1 walks backwards, so the string is reversed.

Why "stop is excluded"? Because `word[0:3]` has exactly `3 - 0 = 3` characters, which makes the math easy to reason about.

### Block 4: methods

```python
message = "  Hello, World  "
print(message.strip())
print(message.lower())
print(message.replace("World", "Python"))
print("a,b,c".split(","))
```

**What it does:**
- `.strip()` removes spaces at both ends (essential for cleaning user input).
- `.lower()` / `.upper()` change case (use for case-insensitive comparisons).
- `.replace(old, new)` swaps text.
- `.split(",")` cuts a string into a **list** of pieces. You will meet lists on Day 10. This is a preview of how strings and lists work together.

A method is a function that belongs to a value. The dot means "use this tool **on** this string".

### Block 5: checking inside strings

```python
email = "ram@weka.io"
print("@" in email)
print(email.endswith(".io"))
print(len(email))
```

**What it does:** `in` answers True/False: "is this text inside that text?". `endswith` checks the tail. `len` counts characters. These produce **booleans** (Day 2), which become the inputs for `if` statements on Day 6.

### Block 6: strings are immutable

```python
word = "Python"
new_word = word.upper()
print(word, new_word)   # Python PYTHON
```

**What it does:** methods never change the original. They **return a new string**. If you want to keep the result you must store it: `word = word.upper()`. A common bug is writing `word.upper()` on its own line and wondering why nothing changed.

## 6. How the blocks connect

```
Block 1  build text (+)           ──┐
Block 2  build text with data (f"")─┤ creating strings
Block 3  take pieces out ([ ])      ┐
Block 4  transform ( .method() )    ├ working with strings
Block 5  ask questions (in, len) ───┘ → returns True/False → Day 6 if
Block 6  rule behind all of it: originals never change
```

Pattern: **clean → inspect → decide**. For example: `.strip().lower()` then `in` then `if`.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `"Age: " + 38` | `TypeError` | `f"Age: {38}"` or `"Age: " + str(38)` |
| `word[6]` for `"Python"` | `IndexError` | Valid indexes are 0 to 5 |
| `text.upper()` without saving | Nothing changes | `text = text.upper()` |
| Forgetting `f` | prints `{name}` literally | Add the `f` prefix |
| Expecting `[0:3]` to include index 3 | Off by one | Stop is excluded |

## 8. Practice

1. Fill in `day03_strings.py`: store a sentence and print its length, uppercase and the first word.
2. Given `"  ram@weka.io  "`, clean it and print the part before the `@`. (Hint: `strip`, `split("@")`.)
3. Check if the word "error" appears in `"Node 5 reported ERROR: disk full"` regardless of case.
4. Reverse your own name.
5. Print a name tag: `Hello, my name is ____` using an f-string.

## 9. Self-check

- Why is `"Python"[0:3]` equal to `"Pyt"` and not `"Pyth"`?
- Does `.upper()` change the original string?
- What is the difference between `+` and an f-string?
- What type does `.split()` return?

**Next:** Day 4: instead of hard-coding text, ask the user for it.

# Day 13: Dictionaries

**Time:** ~2.5 hours | **Example:** `examples/day13_dictionaries.py` | **Your practice file:** `week2_logic/day13_dictionaries.py`

---

## 1. The big idea

A **dictionary** (`dict`) stores data as **key → value pairs**. You look up a value by its **name (key)**, not by a position number.

```python
student = {"name": "Asha", "marks": 88}
student["name"]      # "Asha"
```

## 2. Why does this exist?

Lists are great when position is meaningful. But what is `person[2]`? Is it age? city? You must remember the order. A dictionary makes the data **self-describing**: `person["city"]` says exactly what it is.

Dictionaries also give **instant lookup**: even with a million entries, finding a key is fast. They are everywhere in real Python: JSON data (Day 19), configuration, API responses, database rows, and counting things.

## 3. Simple way to understand

A **phone contacts app**, or a **real dictionary**: you look up a *word* (key) and get its *meaning* (value). You never ask for "the 4,213th entry".

```
 key        value
┌────────┬───────────┐
│ name   │ "Asha"    │
│ marks  │ 88        │
│ city   │ "Chennai" │
└────────┴───────────┘
```

Rules: each **key is unique** (a second assignment to the same key replaces the old value). Keys are usually strings or numbers (immutable types, same reason as set members).

## 4. How it works

| Task | Code |
|------|------|
| Create | `{"a": 1, "b": 2}` or `{}` |
| Read | `d["a"]` (error if missing) |
| Safe read | `d.get("a", default)` |
| Add / update | `d["c"] = 3` |
| Delete | `del d["a"]` or `d.pop("a")` |
| Has key? | `"a" in d` |
| Loop keys | `for k in d:` |
| Loop pairs | `for k, v in d.items():` |
| All keys / values | `d.keys()`, `d.values()` |
| Size | `len(d)` |

## 5. Code walkthrough, block by block

### Block 1: create and read

```python
student = {"name": "Asha", "marks": 88, "city": "Chennai"}
print(student["name"])
print(student.get("age", "unknown"))
```

**What it does:** builds a dict with three pairs. `student["name"]` fetches by key. `student["age"]` would crash with `KeyError` because that key does not exist. `.get("age", "unknown")` returns the **default instead of crashing**. Prefer `.get` when a key might be absent.

### Block 2: add, update, delete

```python
student["marks"] = 92
student["grade"] = "A"
del student["city"]
```

**What it does:** the **same assignment syntax** does two jobs: if the key exists it **updates**, if not it **adds**. Then `del` removes a pair. Dicts are mutable, like lists.

### Block 3: checking for a key

```python
print("name" in student)    # True
print("city" in student)    # False
```

**What it does:** `in` checks **keys**, not values. Use it before reading a key that might not exist. It is the dict version of the `in` you used on strings, lists and sets.

### Block 4: looping

```python
for key in student:
    print(key, "->", student[key])

for key, value in student.items():
    print(f"{key}: {value}")
```

**What it does:**
- Looping directly gives you **keys**. You then look up each value.
- `.items()` hands you **(key, value) pairs**, and `key, value` unpacks each pair (tuple unpacking from Day 12). This is the form you will use most.

### Block 5: counting with a dict

```python
text = "to be or not to be"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
```

**What it does:** the classic dictionary recipe.
1. `text.split()` → list of words (Day 3).
2. For each word, `counts.get(word, 0)` gets the current count (or 0 if it is the first time).
3. Add 1 and store back.

Trace: `to` → 0+1=1, `be` → 1, `or` → 1, `not` → 1, `to` → 1+1=2, `be` → 2.
This is the Day 8 accumulator pattern, but with **one counter per key**. Log analysis ("how many times did each error occur?") is exactly this.

### Block 6: list of dicts

```python
students = [
    {"name": "Asha", "marks": 88},
    {"name": "Ravi", "marks": 72},
    {"name": "Meena", "marks": 95},
]
for s in students:
    print(s["name"], s["marks"])
top = max(students, key=lambda s: s["marks"])
```

**What it does:** a list of dicts behaves like a **table**: each dict is a row, each key is a column. The loop gets one row at a time. `max(..., key=...)` finds the row with the highest `marks`. The `lambda` is a tiny unnamed function (Day 22), read as "for each row s, compare `s["marks"]`". **This is the data shape your Day 20 project uses.**

### Block 7: dict of lists

```python
groups = {"even": [], "odd": []}
for n in range(1, 8):
    key = "even" if n % 2 == 0 else "odd"
    groups[key].append(n)
```

**What it does:** each value is a list. `groups[key]` fetches the list for that key, and `.append(n)` adds to it. This is **grouping**: sort items into buckets. It uses almost everything: dict (13), list methods (11), loop (8), modulo (5), one-line conditional (6). Result: `{'even': [2, 4, 6], 'odd': [1, 3, 5, 7]}`.

## 6. How the blocks connect

```
Block 1  one record, read it
Block 2  edit it
Block 3  ask if a field exists
Block 4  walk through it
Block 5  one dict summarising many items (counts)
Block 6  many dicts in a list (table)
Block 7  dict holding lists (groups)
```

Growth path: **one record → many records → grouped records**. Blocks 6 and 7 combine today's idea with Day 10's list.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `d["missing"]` | `KeyError` | `d.get("missing")` or check `in` |
| Expecting `in` to check values | wrong answer | `value in d.values()` |
| Using a list as a key | `TypeError: unhashable` | use a tuple or string |
| Modifying a dict while looping over it | `RuntimeError` | loop over `list(d)` |
| Duplicate keys in the literal | later one silently wins | keys must be unique |
| Assuming old Python order | n/a | Python 3.7+ keeps insertion order |

## 8. Practice

1. Fill in `day13_dictionaries.py`: make a dict for yourself (name, role, city, years), print every pair with `.items()`.
2. Count how many times each letter appears in a word.
3. Phone book: ask for a name; print the number or "not found" (use `.get`).
4. Given a list of student dicts, print the average marks and the name of the lowest scorer.
5. Group words by their first letter into a dict of lists.
6. Merge two dicts and see what happens with a duplicate key. (Try `a.update(b)`.)

## 9. Self-check

- Why use a dict instead of a list for a person's details?
- What is the difference between `d["x"]` and `d.get("x")`?
- What does `for k, v in d.items()` give you each round?
- Why does `counts.get(word, 0) + 1` avoid a `KeyError`?

**Next:** Day 14: **functions**, so everything you have built can be packaged and reused.

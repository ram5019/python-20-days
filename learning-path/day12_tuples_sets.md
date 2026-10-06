# Day 12: Tuples and Sets

**Time:** ~2 hours | **Example:** `examples/day12_tuples_sets.py` | **Your practice file:** `week2_logic/day12_tuples_sets.py`

---

## 1. The big idea

Lists are not the only collection. Two more serve special purposes:

- **Tuple** `( )`: ordered like a list but **cannot be changed**.
- **Set** `{ }`: **unordered**, holds **only unique** values, and is very fast for "is this in here?" checks.

## 2. Why does this exist?

Choosing the right container **communicates intent** and prevents bugs.

- Some data should never change: coordinates, a date, a database row. A tuple **guarantees** nothing alters it by accident.
- Sometimes you only care *whether* something exists, or you need to remove duplicates: unique IP addresses, unique user IDs. A set does this automatically.

## 3. Simple way to understand

- **List** = a notebook. You can erase and rewrite.
- **Tuple** = a **printed ticket**. Fixed once issued. "Seat 12, Row C" does not change.
- **Set** = a **guest list at the door**. Order is irrelevant, nobody can appear twice, and the bouncer can answer "is Sita on the list?" instantly.

## 4. How it works

| | List | Tuple | Set |
|---|------|-------|-----|
| Brackets | `[1, 2]` | `(1, 2)` | `{1, 2}` |
| Ordered | yes | yes | **no** |
| Index `x[0]` | yes | yes | **no** |
| Duplicates | allowed | allowed | **not allowed** |
| Changeable | yes | **no** | yes (add/remove) |
| Typical use | general collection | fixed record | uniqueness, membership |

Set operations (like school Venn diagrams):

| Symbol | Meaning |
|--------|---------|
| `a & b` | in **both** (intersection) |
| `a \| b` | in **either** (union) |
| `a - b` | in a **but not** b (difference) |

## 5. Code walkthrough, block by block

### Block 1: a tuple

```python
point = (10, 20)
print(point[0], point[1])
# point[0] = 99     # TypeError
```

**What it does:** indexing works exactly like lists. But the commented line, if enabled, raises an error: tuples are **immutable**. That is the point. Nobody can accidentally change your data.

### Block 2: unpacking

```python
x, y = point
name, role, years = ("Ram", "TSE", 15)
```

**What it does:** unpacking splits a tuple into separate variables in one line. The number of names on the left must equal the number of items on the right. You saw `i, s` in `enumerate` on Day 10, and that was tuple unpacking too.

### Block 3: swapping

```python
a, b = 1, 2
a, b = b, a
```

**What it does:** Python builds the tuple `(b, a)` = `(2, 1)` on the right first, then unpacks it. No temporary variable needed (compare with the Day 2 practice task).

### Block 4: returning several values

```python
def min_max(values):
    return min(values), max(values)

low, high = min_max([4, 9, 2, 7])
```

**What it does:** `return a, b` really returns **one tuple**. The caller unpacks it into two variables. This is how Python functions give back multiple answers, and you used this idea in Day 7's "pass data in, get data out".

### Block 5: a set removes duplicates

```python
ids = {1, 2, 2, 3, 3, 3}
print(ids)          # {1, 2, 3}
print(2 in ids)     # True
```

**What it does:** the duplicates silently vanish. Order is not guaranteed, so never rely on it. `in` on a set is much faster than on a list for big data because it jumps straight to the answer instead of scanning.

### Block 6: de-duplicate a list

```python
emails = ["a@x.com", "b@x.com", "a@x.com"]
unique = list(set(emails))
```

**What it does:** `set(emails)` drops repeats; `list(...)` turns it back into a list. This is the one-line answer to Day 11's practice task 2. (Order may change. If order matters, use `dict.fromkeys(emails)`, which Day 13 will make clearer.)

### Block 7: add and remove

```python
ids.add(10)
ids.discard(1)
```

**What it does:** `add` inserts (ignored if already present). `discard` removes **without error** if missing. `remove` on a set raises an error if missing, which is the only difference.

### Block 8: set operations

```python
team_a = {"ram", "sita", "arun"}
team_b = {"sita", "john", "arun"}
print(team_a & team_b)    # {'sita', 'arun'}
print(team_a | team_b)    # all four names
print(team_a - team_b)    # {'ram'}
```

**What it does:** answers real questions: "Who is on both teams?", "Everyone involved?", "Who is only on A?". For a support engineer: "which nodes are in the alert list but not in the healthy list?" is exactly `alerts - healthy`.

### Block 9: empty containers

```python
empty_set = set()
empty_tuple = ()
print(type({}), type(empty_set))
```

**What it does:** `{}` creates an empty **dictionary** (Day 13), not a set. Use `set()` for an empty set. Print the types and see for yourself.

## 6. How the blocks connect

```
Tuples:   Block 1 (fixed) ─► Block 2 (unpack) ─► Block 3 (swap) ─► Block 4 (return many)
Sets:     Block 5 (unique) ─► Block 6 (dedupe) ─► Block 7 (modify) ─► Block 8 (compare sets)
Block 9:  a trap that connects sets to the next day's dictionary
```

Two independent mini-stories sharing one theme: **"pick the container that matches what the data is."**

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `t[0] = 5` on a tuple | `TypeError` | Build a new tuple |
| `x = {}` expecting a set | creates a dict | `set()` |
| `s[0]` on a set | `TypeError` | Sets have no order or index |
| `("a")` as a one-item tuple | just a string | `("a",)` with a trailing comma |
| Relying on set order | inconsistent output | `sorted(s)` if you need order |
| Unpacking wrong count | `ValueError` | match counts |
| Putting a list inside a set | `TypeError: unhashable` | Items must be immutable (use tuples) |

## 8. Practice

1. Fill in `day12_tuples_sets.py`: store a person as a tuple `(name, age, city)` and unpack it.
2. Write a function that returns the sum **and** the average of a list, then unpack both.
3. Count the distinct words in a sentence using a set.
4. Two lists of server names, `all_nodes` and `healthy_nodes`. Find the unhealthy ones with a set difference.
5. Given `[3, 1, 3, 2, 1]`, produce a sorted list without duplicates in one expression.
6. Try to change a tuple item and read the error.

## 9. Self-check

- What can a tuple do that a list cannot, and the other way around?
- Why is membership checking faster on a set?
- Why does `{}` not create an empty set?
- What does `a - b` give for sets?

**Next:** Day 13: dictionaries, which store data by **name** instead of position.

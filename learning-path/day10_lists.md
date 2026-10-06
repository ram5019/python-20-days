# Day 10: Lists

**Time:** ~2 hours | **Example:** `examples/day10_lists.py` | **Your practice file:** `week2_logic/day10_lists.py`

---

## 1. The big idea

A **list** is an ordered, changeable collection of values stored under **one name**.

```python
servers = ["web01", "web02", "db01"]
```

## 2. Why does this exist?

Until now each variable held one value. Real data comes in groups: 50 server names, 200 student marks, a day's worth of log lines. You cannot create `server1`, `server2`, ... `server50`. A list lets you hold the whole group and use a **loop** (Day 8) to process every item with the same code.

## 3. Simple way to understand

A **train**: numbered carriages (positions), each carrying one item.

```
index:    0        1        2
        ┌──────┐ ┌──────┐ ┌──────┐
        │web01 │ │web02 │ │ db01 │
        └──────┘ └──────┘ └──────┘
index:   -3       -2       -1
```

- You can ask for carriage number 1 (**indexing**).
- You can swap what is inside a carriage (lists are **mutable**).
- You can add or remove carriages (Day 11).
- It is the same lockers idea as strings on Day 3, except now you may change the contents.

## 4. How it works

| Task | Code | Notes |
|------|------|-------|
| Create | `[1, 2, 3]` or `[]` | square brackets, commas |
| Length | `len(x)` | number of items |
| Get item | `x[0]`, `x[-1]` | 0-based, negative from the end |
| Slice | `x[1:3]` | new list; stop excluded |
| Change item | `x[1] = "new"` | strings cannot do this |
| Check inside | `"web01" in x` | True/False |
| Loop | `for item in x:` | Day 8 |

Helpful built-ins for number lists: `sum()`, `min()`, `max()`, `sorted()`.

## 5. Code walkthrough, block by block

### Block 1: create and inspect

```python
servers = ["web01", "web02", "db01"]
print(servers)
print(len(servers))
```

**What it does:** one variable now holds three strings. `print` shows the whole list with brackets. `len` tells you how many items (3). The last valid index is always `len - 1`.

### Block 2: index and slice

```python
print(servers[0])      # web01
print(servers[-1])     # db01
print(servers[0:2])    # ['web01', 'web02']
```

**What it does:** exactly the same rules as strings (Day 3). A single index returns **one item**. A slice returns a **new list**.

### Block 3: lists can change

```python
servers[1] = "web99"
print(servers)
```

**What it does:** replaces the item at position 1 in place. This is **mutability**, the big difference from strings, which cannot be changed in place. After this line the list itself is different.

### Block 4: loop over a list

```python
for s in servers:
    print("Checking", s)
```

**What it does:** the loop variable `s` receives each item in turn. Day 8 said "loop over any sequence". Now there is a real one. This is the **most common pairing in Python**: a list plus a for loop.

### Block 5: `enumerate`

```python
for i, s in enumerate(servers, start=1):
    print(f"{i}. {s}")
```

**What it does:** `enumerate` hands you **both the position and the item** each round. `i, s` unpacks the pair into two variables. `start=1` makes counting begin at 1 for human-friendly numbering. Use it whenever you need the index, instead of `range(len(...))`.

### Block 6: mixed and nested lists

```python
mixed = ["Ram", 38, True, [1, 2, 3]]
print(mixed[3][0])     # 1
```

**What it does:** a list may hold any types, including other lists. `mixed[3]` gives the inner list, then `[0]` takes its first item. Read left to right: "item 3, then its item 0". Nested lists are how tables and grids are stored.

### Block 7: statistics

```python
marks = [72, 88, 95, 60]
print("Total:", sum(marks))
print("Average:", sum(marks) / len(marks))
```

**What it does:** built-in functions do the Day 8 accumulator work for you. You could write the loop yourself (and should, once, to see how it works), but `sum`, `min`, `max` are shorter and faster. The average reuses Day 5 division.

### Block 8: the copying pitfall

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)        # [1, 2, 3, 4]
c = a.copy()
```

**What it does:** this surprises everyone. On Day 2, `b = a` copied a number. For a list, `b = a` makes `b` **another name for the same list**. Changing through `b` changes what `a` sees.

```
Numbers:   a ─► 5      b = a  gives  b ─► 5  (copy, independent)
Lists:     a ─► [1,2,3] ◄─ b          (same object, two labels)
```

`a.copy()` (or `a[:]`) makes a real, independent copy. Remember this when you pass lists to functions on Day 14.

## 6. How the blocks connect

```
Block 1  build the collection
Block 2  read from it            (same as strings)
Block 3  change it               (new power vs strings)
Block 4  process every item      (needs Day 8)
Block 5  process with position   (variation of 4)
Block 6  nest collections
Block 7  summarise it            (needs Days 5 and 8)
Block 8  danger: aliasing        (consequence of Block 3)
```

**Block 8 exists because of Block 3.** If lists could not change, sharing a list would be harmless. Because they can change, two names for one list can surprise you.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `servers[3]` on a 3-item list | `IndexError` | Last index is `len - 1` |
| Expecting `b = a` to copy | unexpected edits | `a.copy()` |
| `sum(["1", "2"])` | `TypeError` | Convert to numbers first |
| `print(servers[0:2])` expecting a single item | gets a list | use `[0]` for one item |
| Empty list then `max(x)` | `ValueError` | check `if x:` first |

## 8. Practice

1. Fill in `day10_lists.py`: make a list of 5 favourite tools. Print the first, last and the number of items.
2. Replace the 2nd item and print the list.
3. Given `[4, 8, 15, 16, 23, 42]` print the sum, max, min and average without using `sum`/`max`/`min` (use a loop).
4. Print only the numbers greater than 10.
5. Make a list of 3 lists (a 3×3 grid of numbers) and print the middle element.
6. Reproduce the aliasing bug and then fix it with `.copy()`.

## 9. Self-check

- What makes a list different from a string?
- What does `x[1:3]` return, and what type is it?
- Why does `b = a` not copy a list?
- When do you prefer `enumerate`?

**Next:** Day 11: methods to add, remove, search and sort.

# Day 11: List Methods

**Time:** ~2 hours | **Example:** `examples/day11_list_methods.py` | **Your practice file:** `week2_logic/day11_list_methods.py`

---

## 1. The big idea

A list is changeable (Day 10). **Methods** are the built-in tools that change it: add, remove, search, sort. A method is called with a dot: `my_list.append(x)`.

## 2. Why does this exist?

Real collections are never fixed. Tickets arrive and close, servers join and leave, scores get added. You need standard, reliable ways to **grow, shrink and reorder** a collection without rebuilding it each time.

## 3. Simple way to understand

A **to-do list on a whiteboard**.

- `append` = write a new task at the bottom.
- `insert` = squeeze a task in at a chosen line.
- `remove` = rub out a task by its words.
- `pop` = take the last one off the board and **carry it away** (you get it back).
- `sort` = rearrange the lines alphabetically or by number.

## 4. How it works

| Goal | Method | Changes the list? | Returns |
|------|--------|-------------------|---------|
| Add to end | `x.append(v)` | yes | `None` |
| Add at position | `x.insert(i, v)` | yes | `None` |
| Add many | `x.extend(other)` | yes | `None` |
| Remove by value | `x.remove(v)` | yes | `None` |
| Remove by position, get it back | `x.pop(i)` / `x.pop()` | yes | the item |
| Remove by position | `del x[i]` | yes | (statement) |
| Position of value | `x.index(v)` | no | int |
| Count a value | `x.count(v)` | no | int |
| Sort in place | `x.sort()` | yes | `None` |
| Sorted copy | `sorted(x)` | **no** | new list |
| Reverse in place | `x.reverse()` | yes | `None` |
| Empty it | `x.clear()` | yes | `None` |

**Pattern to remember:** methods that **change** a list return `None`. They do not hand you the list back.

## 5. Code walkthrough, block by block

### Block 1: adding

```python
tasks = ["email", "review"]
tasks.append("deploy")
tasks.insert(0, "standup")
tasks.extend(["lunch", "report"])
```

**What it does:**
- `append("deploy")` → end of list.
- `insert(0, "standup")` → position 0, pushing everything else right.
- `extend([...])` → adds each item of another list, one by one.

State after: `['standup', 'email', 'review', 'deploy', 'lunch', 'report']`.
`append(["a","b"])` would add **one item that is a list**; `extend` adds two items. That is the difference.

### Block 2: removing

```python
tasks.remove("lunch")
last = tasks.pop()
first = tasks.pop(0)
del tasks[0]
```

**What it does:**
- `remove("lunch")` finds the first matching value and deletes it (error if it is not there).
- `pop()` removes the **last** item **and returns it**, so you can store it in `last`.
- `pop(0)` does the same for index 0 (stored in `first`).
- `del tasks[0]` removes by index without giving it back.

After each step: `[... 'report']` → `'report'` and `'standup'` leave → `['email','review','deploy']` → after `del`: `['review','deploy']`.

**Why `pop` is special:** it is how you build a queue or a stack, and the returned value is the item you are now going to work on.

### Block 3: search and count

```python
nums = [5, 3, 8, 3, 1]
print(nums.index(8))    # 2
print(nums.count(3))    # 2
print(8 in nums)        # True
```

**What it does:** these only **read** the list. `index` gives the position of the first match (error if absent). `count` tells you how many. `in` is the safe True/False check, so use it **before** `index` or `remove` to avoid errors.

### Block 4: sorting

```python
nums.sort()
nums.sort(reverse=True)
print(sorted([3, 1, 2]))
```

**What it does:**
- `.sort()` rearranges the **same list** (ascending). `reverse=True` makes it descending.
- `sorted(...)` is a **function** that leaves the original untouched and gives a **new** sorted list.

Choose `.sort()` when you do not need the old order; `sorted()` when you do.

### Block 5: the classic bug

```python
result = [3, 1, 2].sort()
print(result)     # None
```

**What it does:** shows that `sort()` changes the list and returns `None`. The mistake `nums = nums.sort()` **wipes out your list** by replacing it with `None`. Remember the rule from the table above.

### Block 6: build a list in a loop

```python
squares = []
for n in range(1, 6):
    squares.append(n * n)
```

**What it does:** start with an **empty list**, loop, `append` each result. This is the list version of the accumulator pattern from Day 8. After the loop: `[1, 4, 9, 16, 25]`.

### Block 7: filter into a new list

```python
scores = [45, 82, 67, 91, 30]
passed = []
for s in scores:
    if s >= 50:
        passed.append(s)
```

**What it does:** combines **four earlier ideas**: a list (10), a for loop (8), an `if` (6), `append` (11). The result is `[82, 67, 91]`. "Loop, test, collect" is among the most common patterns in programming.

### Block 8: comprehension preview

```python
squares2 = [n * n for n in range(1, 6)]
```

**What it does:** a one-line shortcut for Block 6. You do not need it yet (it is Day 21). Notice that it gives the same result: seeing both forms side by side helps the shortcut make sense later.

## 6. How the blocks connect

```
Blocks 1, 2   change the SIZE of the list (grow / shrink)
Block 3       read-only questions about it
Block 4       change the ORDER
Block 5       warning about return values of Blocks 1, 2, 4
Block 6, 7    use Blocks 1 + loops to BUILD new lists
Block 8       a shortcut for Block 6
```

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `x = x.sort()` | `x` becomes `None` | `x.sort()` alone, or `x = sorted(x)` |
| `x.remove("zzz")` when absent | `ValueError` | `if "zzz" in x:` first |
| `x.pop()` on an empty list | `IndexError` | `if x:` first |
| `append` vs `extend` confusion | nested list | `extend` for many items |
| Removing items while looping over the same list | skips items | loop over `x.copy()` or build a new list |
| `x.index(v)` when absent | `ValueError` | check with `in` |

## 8. Practice

1. Fill in `day11_list_methods.py`: start with `[]`, append 5 names typed by the user, then sort and print them.
2. Remove duplicates from `[1,2,2,3,3,3]` using a loop and `in` (Day 12 shows an easier way).
3. Build a simple **stack**: push 3 items with `append`, pop them back and print the order.
4. Ask for numbers until the user types `done`, keep them in a list, then print the largest, smallest and sorted order.
5. Given a list of marks, create `passed` and `failed` lists.
6. Reproduce the `x = x.sort()` bug and explain what happened.

## 9. Self-check

- What do `append`, `insert` and `extend` each do?
- What is the difference between `remove`, `pop` and `del`?
- Why does `nums = nums.sort()` lose your data?
- When would you use `sorted()` rather than `.sort()`?

**Next:** Day 12: two more collection types, **tuple** (cannot change) and **set** (no duplicates).

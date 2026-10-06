# Day 22: lambda, map, filter

**Example:** `examples/day22_lambda_map_filter.py` | **Your stub:** `advanced/day22_lambda_map_filter.py`

---

## 1. The big idea

- A **lambda** is a small **unnamed function** written on one line: `lambda x: x * 2`.
- `map(func, items)` **applies** a function to every item.
- `filter(func, items)` **keeps** the items for which the function returns True.

The deeper idea: **functions are values.** You can pass a function to another function, just as you pass a number.

## 2. Why does it exist?

Sometimes you need a function for **one moment only**: "sort these by marks", "find the busiest server". Writing a full `def` with a name for a one-liner is clutter. A lambda lets you write it right where you need it. You already met one in Day 13 (`max(..., key=lambda s: s["marks"])` in the project).

## 3. Simple way to understand

A **sticky note instruction** handed to a worker.

- Normal function = a printed procedure manual with a title (you reuse it often).
- Lambda = a sticky note: "multiply by 2". You hand it over, it is used, and then it is thrown away.
- `map` = the worker applies the note to **every** item on the belt.
- `filter` = the worker applies the note as a **yes/no test** and keeps the yeses.

## 4. How it works

```python
lambda parameters: expression
```

- No `return` keyword: the expression's value **is** the result.
- Only **one expression**, no multi-line bodies.
- `map` and `filter` return a lazy iterator (see Day 24), so wrap them in `list(...)` to see results.

Compare:

| Task | map/filter | Comprehension (Day 21) |
|------|-----------|------------------------|
| double each | `list(map(lambda x: x*2, nums))` | `[x*2 for x in nums]` |
| keep evens | `list(filter(lambda x: x%2==0, nums))` | `[x for x in nums if x%2==0]` |

Python style prefers comprehensions for these. **Where lambda really shines is `key=`.**

## 5. Code walkthrough, block by block

### Block 1: def vs lambda
`double` and `double_l` do the same job. The lambda version is shorter, but assigning a lambda to a name is not good style: if it needs a name, use `def`. It is here only to show they are equivalent.

### Block 2: `map`
The lambda is the machine; `nums` is the belt. Each number goes in, its double comes out. `list()` collects the results.

### Block 3: `filter`
The lambda is a **test** returning True/False (a Day 5 comparison). Only numbers where it is True survive.

### Block 4: `sorted(..., key=lambda ...)`
Sorting tuples by default compares the first item (the name). `key=lambda s: s[1]` says "**sort by the second item**", the marks. `reverse=True` gives highest first. This is the most useful lambda pattern in everyday Python.

### Block 5: `key=` with dicts
`max(servers, key=lambda s: s["cpu"])` returns the **whole dict** with the largest `cpu`. The lambda tells `max` *what to compare*, while `max` still returns the original item.

### Block 6: functions as arguments
`apply_twice(func, value)` calls whatever function you give it, two times. This is the core idea: behaviour can be **passed around**. It leads straight to decorators (Day 23).

### Block 7: comprehension versions
The same results as Blocks 2 and 3 in the more readable Day 21 form. Knowing both lets you read other people's code.

### Block 8: a mini pipeline
`map(str.lower, words)` lowercases (passing an existing method as the function, no lambda needed) → `filter(... len(w) > 2)` drops short words → `sorted(..., key=len)` orders by length. Read it **from the inside out**.

## 6. How the blocks connect

```
Block 1  lambda = small function
Blocks 2, 3  pass it to map / filter
Blocks 4, 5  pass it as key= (most useful)
Block 6  the principle: functions can be arguments
Block 7  the alternative style
Block 8  chain everything
```

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `map(...)` printed directly | `<map object at ...>` | wrap in `list()` |
| Multi-statement lambda | `SyntaxError` | use `def` |
| Complicated lambdas | unreadable | name it with `def` |
| `sorted(students, key=lambda s: s[1])` expecting highest first | ascending | add `reverse=True` |
| Using a lambda just to call another function: `lambda x: len(x)` | pointless | pass `len` directly |

## 8. Practice

1. Sort a list of words by their last letter.
2. Sort a list of dicts (name, age) by age, then print only the names.
3. Use `filter` to keep strings that contain `"@"`.
4. Use `max` with `key=` to find the longest word.
5. Write `apply_n_times(func, value, n)`.
6. Rewrite your `map`/`filter` answers as comprehensions.

## 9. Self-check

- What does `key=` tell `sorted` or `max`?
- Why wrap `map` in `list()`?
- When should a lambda become a `def`?

**Next:** Day 23: functions that **wrap other functions** (decorators).

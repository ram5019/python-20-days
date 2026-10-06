# Day 21: Comprehensions

**Example:** `examples/day21_comprehensions.py` | **Your stub:** `advanced/day21_comprehensions.py`

---

## 1. The big idea

A **comprehension** builds a new list, dict or set from an existing sequence **in one expression**.

```python
squares = [n * n for n in range(1, 6)]
```

Read it aloud: **"n times n, for each n in the range"**.

## 2. Why does it exist?

On Day 11 you wrote the "loop, test, collect" pattern many times (create an empty list, loop, `append`). That is 3 to 4 lines for one idea. A comprehension says the same thing in one line that reads like English, and it is usually a bit faster. Experienced Python code uses it constantly.

## 3. Simple way to understand

A **conveyor belt with a machine on it**. Items come in (`for n in ...`), an optional **gate** lets only some through (`if ...`), and the **machine** transforms each one (`n * n`). What comes out the end is your new list.

```
 [  n * n    for n in range(1,6)    if n % 2 == 1  ]
    ▲            ▲                      ▲
 transform    source (belt)          filter (gate)
```

## 4. How it works

| Kind | Syntax | Result |
|------|--------|--------|
| list | `[expr for x in seq if cond]` | list |
| dict | `{k: v for x in seq}` | dict |
| set | `{expr for x in seq}` | set |

Order in the line: **what to produce → where from → optional filter**. An `if/else` that chooses the *value* goes at the **front**; a plain `if` that filters goes at the **end**.

## 5. Code walkthrough, block by block

### Block 1: loop vs comprehension
Both versions build `[1, 4, 9, 16, 25]`. The `print(... == ...)` proves they are identical. The comprehension is the loop folded into one line: `append(n * n)` became the expression at the front.

### Block 2: with a filter
`[s for s in scores if s >= 50]` is Day 11's "filter into a new list" in one line. The `if` at the end is the gate. Items that fail are simply not included.

### Block 3: transform text
`[n.strip().title() for n in names]` applies Day 3 string methods to every item. No filter, just a transformation.

### Block 4: `if/else` inside
`["pass" if s >= 50 else "fail" for s in scores]`. Here we want **one output per input** with a choice of value, so the Day 6 one-line conditional sits at the front. Rule: **filtering (drop items) → `if` at the end; choosing (value for every item) → `if/else` at the front.**

### Block 5: dict comprehension
`{w: len(w) for w in words}` builds `key: value` pairs. This replaces a Day 13 loop that did `d[key] = value`.

### Block 6: set comprehension
Curly braces **without** a colon make a set, so duplicates vanish (Day 12). Here it collects unique email domains.

### Block 7: nested loops
`[value for row in grid for value in row]` flattens a list of lists. Read the `for` parts **left to right in the same order as nested loops would be written**: outer first, then inner.

### Block 8: real use
Filtering log lines that start with `ERROR`. Replace the list with lines read from a file (Day 15) and you have a one-line log filter.

## 6. How the blocks connect

```
Block 1  proof it equals the loop you know
Block 2  + filter
Block 3  + transform
Block 4  + choose a value
Block 5, 6  same idea, other containers
Block 7  two loops in one
Block 8  everyday use
```

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `[x for x in data if x > 1 else 0]` | `SyntaxError` | `if/else` goes at the **front** |
| Cramming 3 conditions and nested loops into one line | unreadable | use a normal loop |
| Using a comprehension just for side effects: `[print(x) for x in data]` | wasteful list of `None` | use a `for` loop |
| `{x for x in ...}` expecting a dict | gets a set | add `key: value` |
| Building a huge list you only loop over once | wastes memory | use a generator (Day 24) |

**Rule of thumb:** if it does not fit comfortably on one line and read like a sentence, use a normal loop.

## 8. Practice

1. In your stub, create the squares of the even numbers from 1 to 20.
2. Given a list of words, make a list of their lengths.
3. Given `[3, -1, 4, -5]`, make `["pos", "neg", ...]`.
4. Build `{n: n**3 for n in range(1, 6)}`.
5. From a sentence, make a set of the unique first letters.
6. Rewrite one of your Day 11 loops as a comprehension and check the results match.

## 9. Self-check

- What are the three parts of a list comprehension?
- Where does a filter `if` go? Where does an `if/else` go?
- When should you **not** use one?

**Next:** Day 22: tiny anonymous functions and the `map` / `filter` tools.

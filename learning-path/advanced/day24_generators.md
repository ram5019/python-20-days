# Day 24: Generators

**Example:** `examples/day24_generators.py` | **Your stub:** `advanced/day24_generators.py`

---

## 1. The big idea

A **generator** produces values **one at a time, on demand**, instead of building the whole collection in memory. A function becomes a generator when it uses `yield` instead of `return`.

## 2. Why does it exist?

Imagine analysing a 20 GB log file or a million database rows. A list would load **everything** into memory first and may crash the machine. A generator hands over **one item, then pauses**, then produces the next when asked. Memory use stays tiny, and you can even represent **infinite** sequences.

This is how Python reads files line by line (Day 15), how pandas reads big CSVs in chunks, and how many web frameworks stream data.

## 3. Simple way to understand

- **List** = a printed 1,000-page book on your desk. All of it takes up space at once.
- **Generator** = a **streaming service**. You watch one episode at a time; the rest is not sitting in your room.

Or a **bookmark in a book**: `yield` is "hand over this page and keep my place". The next request resumes from the bookmark.

## 4. How it works

```python
def count_up(limit):
    n = 1
    while n <= limit:
        yield n       # hand back n and PAUSE
        n += 1        # resume here next time
```

- Calling `count_up(3)` does **not** run the body. It returns a generator object.
- Each `next()` (or each round of a `for` loop) runs the body **until the next `yield`**, then pauses with all local variables intact.
- When the function ends, `StopIteration` is raised and a `for` loop quietly stops.

Generator **expression**: like a list comprehension (Day 21) but with `()`: `(n * n for n in range(10))`.

## 5. Code walkthrough, block by block

### Block 1: first generator
A `while` loop (Day 9) with `yield` in it. The `for` loop receives 1, 2, 3 in turn. After each value the function **freezes**; when the loop asks again it unfreezes at `n += 1`.

### Block 2: `next()` by hand
Shows what `for` does behind the scenes: ask for a value, get it, ask again. When there is nothing left, `StopIteration` appears, and `for` loops catch that for you. (Day 16's `try/except` in action.)

### Block 3: memory
`[...]` builds a million numbers in memory. `(...)` builds only the recipe. `sys.getsizeof` shows the list is far bigger. `sum(big_gen)` still works because `sum` just keeps asking for the next value.

### Block 4: single use
A generator is **consumed** as you read it. After `list(g)` once, it is empty. If you need the data twice, store it in a list or create a new generator.

### Block 5: infinite sequences
`while True` with `yield` never ends, which would be fatal in a normal function. Because values come on demand, you take only as many as you ask for (`next(fib)` ten times). `a, b = b, a + b` is tuple swapping from Day 12.

### Block 6: lazy filtering
`error_lines` yields only matching lines. With a real file you would loop `for line in f:` (Day 15), which is itself lazy, so a multi-gigabyte log never loads at once.

### Block 7: pipelines
`numbers → squares → evens`. Each stage is a small generator that consumes the previous one. **No intermediate lists are ever created**, and each item flows all the way through before the next one starts. `yield from range(...)` is shorthand for looping and yielding each item.

## 6. How the blocks connect

```
Block 1  yield pauses a function
Block 2  next() drives it manually
Block 3  why it matters: memory
Block 4  watch out: single use
Block 5  infinite data
Block 6  real use: lazy log filtering
Block 7  combine into pipelines
```

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Iterating a generator twice | second pass is empty | recreate it or store a list |
| Using `return value` instead of `yield` | normal function | use `yield` |
| `len(gen)` | `TypeError` | generators have no length; count while looping |
| Indexing `gen[0]` | `TypeError` | use `next(gen)` |
| Converting a huge generator to a list | memory problem again | keep it lazy |
| Using `[]` when you meant `()` | builds a full list | parentheses for a generator expression |

## 8. Practice

1. Write a generator `countdown(n)` that yields n down to 1.
2. Write `read_chunks(items, size)` yielding lists of `size` items (batching).
3. Write `first_n_primes(n)` as a generator.
4. Make a pipeline: lines of text → stripped → non-empty → upper-cased.
5. Compare `sum([i*i for i in range(10**6)])` with `sum(i*i for i in range(10**6))` using `sys.getsizeof` or the Day 23 `@timer`.

## 9. Self-check

- What happens to a function when it hits `yield`?
- Why is a generator better for huge data?
- Why does a generator work only once?
- What is the difference between `[x for ...]` and `(x for ...)`?

**Next:** Day 25: keep each project's libraries organised with virtual environments.

# Day 23: Decorators

**Example:** `examples/day23_decorators.py` | **Your stub:** `advanced/day23_decorators.py`

---

## 1. The big idea

A **decorator** is a function that **takes a function, wraps it with extra behaviour, and returns the wrapped version**. You apply it with `@name` above a function.

```python
@timer
def slow_sum(n): ...
```

## 2. Why does it exist?

Sometimes many functions need the **same extra step**: log every call, time it, retry on failure, check the user is logged in. Copy-pasting that into each function is repetitive and error-prone. A decorator lets you write the extra behaviour **once** and attach it with one line, **without touching the function's own code**.

You will see decorators everywhere in the tracks: `@app.route(...)` in Flask, `@app.get(...)` in FastAPI, `@retry`, `@lru_cache`.

## 3. Simple way to understand

**Gift wrapping.** The function is the gift. The decorator is the wrapping paper: the gift inside is unchanged, but what the recipient receives has something extra around it (a bow that prints a log, a timer, a retry loop).

```
caller ──► [ wrapper: before ] ──► original function ──► [ wrapper: after ] ──► caller
```

## 4. How it works: build it up in three ideas

1. **Functions are values** (Day 22). You can store a function in a variable and pass it around.
2. **A function can define and return another function** (closure). The inner one "remembers" outer variables.
3. **A decorator is those two combined.**

```python
def decorator(func):          # receives the original
    def wrapper(*args, **kwargs):
        # extra behaviour before
        result = func(*args, **kwargs)   # run the original
        # extra behaviour after
        return result
    return wrapper            # hand back the new version

@decorator
def hello(): ...
# is exactly the same as:  hello = decorator(hello)
```

`*args, **kwargs` means "accept **any** positional and keyword arguments and pass them along", so one decorator works on any function.

## 5. Code walkthrough, block by block

### Block 1: functions are values
`f = say_hi` (no parentheses) stores the function itself. `f()` then calls it. Parentheses **call**; no parentheses **refer**.

### Block 2: returning a function
`make_multiplier(3)` returns the inner `multiply`, which **remembers `n = 3`** even after `make_multiplier` finished. That memory is called a **closure**, and it is what lets a wrapper remember which function it is wrapping.

### Block 3: a decorator by hand
`shout(greet)` returns `wrapper`, and we **rebind** the name `greet` to it. Now calling `greet()` runs `wrapper`, which runs the original and upper-cases the result. Nothing magic happened: only Blocks 1 and 2 combined.

### Block 4: the `@` shortcut
`@shout` above `def farewell()` is just shorthand for `farewell = shout(farewell)`. It is neater and shows at a glance that the function is decorated.

### Block 5: `*args`, `**kwargs`, `functools.wraps`
`log_calls` works for **any** function because the wrapper accepts anything and forwards it. It prints before and after. `@functools.wraps(func)` copies the original's name and docstring onto the wrapper; without it, `add.__name__` would say `wrapper`, which confuses debugging tools.

### Block 6: a timing decorator
Records the start time, runs the function, prints elapsed time, returns the result. Note `return result`: forgetting it makes the decorated function return `None` (a very common bug). This is a practical tool for finding slow code.

### Block 7: a decorator with its own argument
`@retry(times=3)` needs **three** levels: `retry(times)` returns `decorator(func)`, which returns `wrapper`. Outer = settings, middle = receives the function, inner = does the work. The loop uses Day 16's `try/except`: on failure it prints and tries again; after the last attempt it raises. The demo function fails twice then succeeds, so you see two failures and a success.

## 6. How the blocks connect

```
Block 1  function = value
Block 2  function returns function (closure)
Block 3  decorator written by hand   (1 + 2)
Block 4  @ shorthand
Block 5  works for any function      (*args/**kwargs, wraps)
Block 6  real example: timing
Block 7  real example: retry, with settings (3-level nesting)
```

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Wrapper forgets `return result` | decorated function returns `None` | always return it |
| Writing `@shout()` for a no-argument decorator | `TypeError` | `@shout` (no parentheses) |
| Writing `@retry` for one that needs arguments | wrong behaviour | `@retry(times=3)` |
| Omitting `functools.wraps` | lost name/docstring | add it |
| Wrapper has fixed parameters | breaks other functions | use `*args, **kwargs` |

## 8. Practice

1. Write `@announce` that prints "Starting..." before and "Done." after any function.
2. Write `@count_calls` that counts how many times a function was called (store in `wrapper.calls`).
3. Write `@require_positive` that raises `ValueError` if the first argument is negative.
4. Stack two decorators (`@timer` over `@log_calls`) and observe the order.
5. Try `functools.lru_cache` on a recursive Fibonacci and time it.

## 9. Self-check

- What does `@decorator` expand to?
- Why must the wrapper return the original's result?
- What are `*args` and `**kwargs` for?
- Why does `@retry(times=3)` have three nested functions?

**Next:** Day 24: generators, producing values **one at a time** to save memory.

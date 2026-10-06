"""Day 23 example: decorators.

Run:  python3 learning-path/advanced/examples/day23_decorators.py
"""

import functools
import time

# BLOCK 1: functions are values: store and pass them
def say_hi():
    return "hi"

f = say_hi                       # no parentheses: the function itself
print(f())                       # hi

# BLOCK 2: a function that returns a function
def make_multiplier(n):
    def multiply(x):
        return x * n             # remembers n (closure)
    return multiply

triple = make_multiplier(3)
print(triple(5))                 # 15

# BLOCK 3: a decorator by hand
def shout(func):
    def wrapper():
        return func().upper() + "!"
    return wrapper

def greet():
    return "hello"

greet = shout(greet)             # replace greet with the wrapped version
print(greet())                   # HELLO!

# BLOCK 4: the @ shortcut
@shout
def farewell():
    return "goodbye"

print(farewell())                # GOODBYE!

# BLOCK 5: a decorator that works with any arguments
def log_calls(func):
    @functools.wraps(func)       # keep the original name/docstring
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b

add(2, 3)
print(add.__name__)              # add (thanks to functools.wraps)

# BLOCK 6: a useful decorator: timing
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(1_000_000)

# BLOCK 7: a decorator that takes its own argument
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
            raise RuntimeError("all attempts failed")
        return wrapper
    return decorator

calls = {"n": 0}

@retry(times=3)
def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("network down")
    return "success"

print(flaky())                   # succeeds on the 3rd try

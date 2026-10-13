"""Day 23: Decorators. 10 examples, simple to complex.

Run:  python3 advanced/day23_decorators/more_examples.py
"""

import functools
import time


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Functions are values")
# WHAT: store a function in a variable and call it.
# HOW : no parentheses = the function itself; with parentheses = call it.
# WHY : decorators only make sense once this is clear.
def hello():
    return "hello"


f = hello
print(f(), f is hello)
funcs = [len, str.upper, hello]
print([fn.__name__ for fn in funcs])

# ---------------------------------------------------------------
show(2, "A function that returns a function (closure)")
# WHAT: build a function with a memory.
# HOW : the inner function remembers `n` after make_adder has finished.
# WHY : a decorator's wrapper remembers which function it wraps.
def make_adder(n):
    def add(x):
        return x + n
    return add


add5 = make_adder(5)
print(add5(10), make_adder(100)(1))

# ---------------------------------------------------------------
show(3, "A decorator written by hand")
# WHAT: wrap a function to change what it does.
# HOW : the decorator takes a function, defines wrapper, returns wrapper.
#       Then we replace the name with the wrapped version.
# WHY : adds behaviour without touching the original function.
def shout(func):
    def wrapper():
        return func().upper() + "!"
    return wrapper


def greet():
    return "good morning"


greet = shout(greet)
print(greet())

# ---------------------------------------------------------------
show(4, "The @ shortcut")
# WHAT: the same thing, written neatly.
# HOW : @shout above def means  farewell = shout(farewell).
# WHY : one line shows the function is decorated.
@shout
def farewell():
    return "see you"


print(farewell())

# ---------------------------------------------------------------
show(5, "A decorator for ANY function: *args, **kwargs, wraps")
# WHAT: a logging decorator that works on every signature.
# HOW : the wrapper accepts anything and forwards it. functools.wraps keeps
#       the original name and docstring.
# WHY : forgetting wraps hides the real function name in debugging.
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  -> {func.__name__}{args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"  <- {result}")
        return result
    return wrapper


@log_calls
def add(a, b=0):
    """Add two numbers."""
    return a + b


add(2, 3)
add(5, b=10)
print(add.__name__, "|", add.__doc__)

# ---------------------------------------------------------------
show(6, "A timing decorator")
# WHAT: measure how long any function takes.
# HOW : note the time before and after; return the original result.
# WHY : finding slow code is the first step of optimising.
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} finished in {'fast' if elapsed < 1 else 'slow'} time")
        return result
    return wrapper


@timer
def count_to(n):
    return sum(range(n))


print(count_to(500_000))

# ---------------------------------------------------------------
show(7, "A decorator that takes its own argument")
# WHAT: @repeat(3) runs a function three times.
# HOW : THREE levels: repeat(times) -> decorator(func) -> wrapper.
#       Outer = settings, middle = receives the function, inner = does the work.
# WHY : configurable decorators (@app.route("/path"), @retry(times=3)).
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(3)
def ping():
    print("  ping")


ping()

# ---------------------------------------------------------------
show(8, "Retry on failure")
# WHAT: try again when a function raises an error.
# HOW : loop with try/except; give up after the last attempt.
# WHY : networks and disks fail temporarily; retries hide the glitch.
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as error:
                    print(f"  attempt {attempt} failed: {error}")
            raise RuntimeError(f"{func.__name__} failed {times} times")
        return wrapper
    return decorator


state = {"calls": 0}


@retry(times=3)
def flaky():
    state["calls"] += 1
    if state["calls"] < 3:
        raise ConnectionError("network down")
    return "connected"


print(flaky())

# ---------------------------------------------------------------
show(9, "Caching results (memoisation)")
# WHAT: remember answers so repeated calls are instant.
# HOW : a dict maps arguments to results. functools.lru_cache does this
#       for you.
# WHY : turns the slow recursive Fibonacci into a fast one.
def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper


@memoize
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(60))


@functools.lru_cache(maxsize=None)
def fib2(n):
    return n if n < 2 else fib2(n - 1) + fib2(n - 2)


print(fib2(80), fib2.cache_info().hits > 0)

# ---------------------------------------------------------------
show(10, "Mini program: a command registry and stacked decorators")
# WHAT: the pattern behind Flask's @app.route.
# HOW : a decorator REGISTERS the function in a dict and returns it unchanged;
#       a second decorator checks permissions. Decorators stack bottom-up.
# WHY : frameworks use decorators to connect your functions to events.
COMMANDS = {}


def command(name):
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator


def requires_admin(func):
    @functools.wraps(func)
    def wrapper(user, *args):
        if user != "admin":
            return f"{user}: permission denied"
        return func(user, *args)
    return wrapper


@command("status")
def status(user):
    return f"{user}: all systems normal"


@command("restart")
@requires_admin
def restart(user, service):
    return f"{user}: restarted {service}"


print(sorted(COMMANDS))
print(COMMANDS["status"]("guest"))
print(COMMANDS["restart"]("guest", "web"))
print(COMMANDS["restart"]("admin", "web"))

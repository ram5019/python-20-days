"""Day 14: Functions. 10 examples, simple to complex.

Run:  python3 week2_logic/day14_functions/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Define once, call many times")
# WHAT: a named block of code.
# HOW : def stores it; calling it with () runs it.
# WHY : write once, reuse everywhere.
def say_hello():
    print("Hello from a function!")


say_hello()
say_hello()

# ---------------------------------------------------------------
show(2, "Parameters: give the function inputs")
# WHAT: one function, different data each call.
# HOW : parameters are names in the definition; arguments are the actual
#       values passed in the call.
# WHY : makes a function general instead of fixed.
def greet(name, punctuation):
    print(f"Hello, {name}{punctuation}")


greet("Asha", "!")
greet("Ravi", ".")

# ---------------------------------------------------------------
show(3, "return: give an answer back")
# WHAT: a function that computes a value.
# HOW : the call is replaced by the returned value, so calls can be nested.
# WHY : lets other code use the result.
def add(a, b):
    return a + b


total = add(3, 4)
print(total)
print(add(add(1, 2), add(3, 4)))

# ---------------------------------------------------------------
show(4, "print versus return")
# WHAT: the most important distinction of the day.
# HOW : print SHOWS something to a human; return HANDS a value to the program.
#       A function without return gives back None.
# WHY : calculations should return; only the outer layer should print.
def show_square(n):
    print(n * n)


def get_square(n):
    return n * n


x = show_square(5)
y = get_square(5)
print("x =", x, "| y =", y)
print("can reuse y:", y + 1)

# ---------------------------------------------------------------
show(5, "Default values and keyword arguments")
# WHAT: optional parameters; naming arguments in the call.
# HOW : exp=2 is used when the caller omits it; name=value in a call lets
#       you change the order.
# WHY : readable calls and sensible defaults.
def power(base, exp=2):
    return base ** exp


print(power(5), power(2, 10), power(exp=3, base=2))


def make_label(text, width=10, fill="."):
    return text.ljust(width, fill)


print(make_label("Name"), make_label("Age", fill="_"), make_label("City", width=6))

# ---------------------------------------------------------------
show(6, "Early return and several return values")
# WHAT: leave a function as soon as the answer is known; return a pair.
# HOW : return ends the function immediately. `return a, b` is a tuple.
# WHY : guard clauses keep code flat; tuples return (result, status).
def safe_divide(a, b):
    if b == 0:
        return None, "cannot divide by zero"
    return a / b, "ok"


print(safe_divide(10, 4))
value, status = safe_divide(1, 0)
print(value, "|", status)

# ---------------------------------------------------------------
show(7, "*args and **kwargs: any number of arguments")
# WHAT: accept a flexible list of inputs.
# HOW : *args collects extra positional arguments into a tuple;
#       **kwargs collects keyword arguments into a dict.
# WHY : wrappers, loggers and flexible tools (decorators use this, Day 23).
def total_of(*numbers):
    return sum(numbers)


def describe(**details):
    return ", ".join(f"{k}={v}" for k, v in details.items())


print(total_of(1, 2, 3), total_of(10), total_of())
print(describe(name="Asha", city="Paris", age=28))

# ---------------------------------------------------------------
show(8, "Scope: local versus global")
# WHAT: where a variable exists.
# HOW : a variable created inside a function is local: it vanishes when the
#       function ends and never changes a global of the same name.
# WHY : functions cannot accidentally break each other.
counter = 100


def change_local():
    counter = 1                 # a NEW local variable
    return counter


def read_global():
    return counter + 1          # reading a global is fine


print(change_local(), counter, read_global())
try:
    print(local_only)
except NameError as error:
    print("Error:", error)

# ---------------------------------------------------------------
show(9, "Recursion: a function that calls itself")
# WHAT: solve a problem by solving a smaller copy of it.
# HOW : a base case stops it; each call moves toward the base case.
# WHY : natural for trees, folders and mathematical definitions.
def factorial(n):
    if n <= 1:                   # base case
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(factorial(5))
print([fibonacci(i) for i in range(10)])


# ---------------------------------------------------------------
show(10, "Mini program: a toolkit built from small functions")
# WHAT: small functions that call each other, including a function passed
#       as an argument.
# HOW : each function does ONE job; `apply_to_all` takes another function.
# WHY : this is how large programs stay readable. Docstrings document them.
def clean(text):
    """Lowercase and strip a piece of text."""
    return text.strip().lower()


def is_valid_email(text):
    """Very simple check: one @ and a dot after it."""
    text = clean(text)
    return text.count("@") == 1 and "." in text.split("@")[1]


def apply_to_all(func, items):
    return [func(item) for item in items]


def password_strength(password):
    checks = [
        len(password) >= 8,
        any(c.isdigit() for c in password),
        any(c.isupper() for c in password),
        any(not c.isalnum() for c in password),
    ]
    return ["weak", "weak", "fair", "good", "strong"][sum(checks)]


emails = ["  Sam@Example.com ", "bad.email", "a@b"]
print(apply_to_all(clean, emails))
print(apply_to_all(is_valid_email, emails))
for pw in ("abc", "abcdefgh", "Abcdefg1", "Abcdef1!"):
    print(f"{pw:<10} -> {password_strength(pw)}")
print(is_valid_email.__doc__)

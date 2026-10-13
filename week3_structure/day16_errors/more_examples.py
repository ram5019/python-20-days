"""Day 16: Errors and exceptions. 10 examples, simple to complex.

Run:  python3 week3_structure/day16_errors/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Catch an error and keep going")
# WHAT: survive a divide-by-zero.
# HOW : the risky code goes in try; if it fails, Python jumps to the matching
#       except. The program continues afterwards.
# WHY : crashes are not acceptable for users; handled errors are.
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")
print("The program is still running")

# ---------------------------------------------------------------
show(2, "Read the error message with `as e`")
# WHAT: see what Python says about the problem.
# HOW : `except ValueError as e` stores the error object; print(e) shows it.
# WHY : good messages make debugging and logging possible.
try:
    int("abc")
except ValueError as e:
    print("Problem:", e)

# ---------------------------------------------------------------
show(3, "A tour of common exceptions")
# WHAT: trigger the usual suspects on purpose.
# HOW : each lambda causes a different error; we print its class and message.
# WHY : learn to recognise them by name; the name tells you what is wrong.
problems = {
    "ValueError": lambda: int("x"),
    "TypeError": lambda: "5" + 3,
    "KeyError": lambda: {"a": 1}["b"],
    "IndexError": lambda: [1, 2][5],
    "ZeroDivisionError": lambda: 1 / 0,
    "NameError": lambda: undefined_name,
    "AttributeError": lambda: "text".no_such_method(),
    "FileNotFoundError": lambda: open("/no/such/file.txt"),
}
for expected, trigger in problems.items():
    try:
        trigger()
    except Exception as e:
        print(f"{type(e).__name__:<18} {str(e)[:48]}")

# ---------------------------------------------------------------
show(4, "Several except blocks")
# WHAT: respond differently to different problems.
# HOW : Python tries the except blocks top to bottom; the first match wins.
#       Catch SPECIFIC errors rather than everything.
# WHY : a bare `except:` hides real bugs.
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "cannot divide by zero"
    except TypeError:
        return "both values must be numbers"


print(safe_divide(10, 2), "|", safe_divide(10, 0), "|", safe_divide("10", 2))

# ---------------------------------------------------------------
show(5, "else and finally")
# WHAT: code for success only; code that must always run.
# HOW : else runs only if NO error occurred; finally runs no matter what.
# WHY : keeps the risky line small; guarantees cleanup.
def convert(text):
    try:
        value = int(text)
    except ValueError:
        print(f"  '{text}': not a number")
    else:
        print(f"  '{text}': converted to {value}")
    finally:
        print(f"  '{text}': done")


convert("42")
convert("4x2")

# ---------------------------------------------------------------
show(6, "Validate input with a retry function")
# WHAT: never crash on bad input.
# HOW : loop until int() succeeds. The answers are scripted here.
# WHY : fixes the crashing programs of Day 4.
answers = iter(["abc", "", "7"])


def ask_int(prompt):
    while True:
        text = next(answers)
        print(f"{prompt}{text}")
        try:
            return int(text)
        except ValueError:
            print("  Please type a whole number.")


print("Got:", ask_int("How many? "))

# ---------------------------------------------------------------
show(7, "Raise your own errors")
# WHAT: stop when data breaks a rule.
# HOW : `raise ValueError("message")` creates an error on purpose.
# WHY : a function should refuse bad data loudly, not return wrong answers.
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("age must be a whole number")
    if age < 0:
        raise ValueError("age cannot be negative")
    return age


for candidate in (30, -5, "ten"):
    try:
        print("OK:", set_age(candidate))
    except (ValueError, TypeError) as e:
        print(f"Rejected {candidate!r}: {e}")

# ---------------------------------------------------------------
show(8, "Custom exception classes")
# WHAT: give your own errors a name.
# HOW : subclass Exception. Callers can catch exactly this kind.
# WHY : lets a program tell "my rule was broken" apart from other bugs.
class InsufficientFunds(Exception):
    pass


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFunds(f"balance {balance}, requested {amount}")
    return balance - amount


try:
    withdraw(50, 80)
except InsufficientFunds as e:
    print("Declined:", e)

# ---------------------------------------------------------------
show(9, "Safe file reading with a fallback")
# WHAT: a function that returns None instead of crashing.
# HOW : catch FileNotFoundError; the caller decides what None means.
# WHY : functions return results; the caller handles the story.
def read_or_none(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None


print(read_or_none("definitely_missing.txt"))


def parse_number(text, default=0):
    try:
        return float(text)
    except (ValueError, TypeError):
        return default


print(parse_number("3.5"), parse_number("abc"), parse_number(None, default=-1))

# ---------------------------------------------------------------
show(10, "Mini program: robust data cleaning with a report")
# WHAT: process messy rows; collect good data and a list of problems.
# HOW : try/except inside the loop so one bad row does not stop the rest.
# WHY : real data is messy; reporting problems beats crashing or ignoring.
rows = ["Asha,88", "Ravi,seventy", "Meena,95", "broken", "John,-5", "Li,101"]
good, problems = [], []
for number, row in enumerate(rows, start=1):
    try:
        name, score_text = row.split(",")
        score = int(score_text)
        if not 0 <= score <= 100:
            raise ValueError(f"score {score} out of range")
        good.append((name, score))
    except ValueError as e:
        problems.append((number, row, str(e)))
print("Accepted:", good)
for number, row, why in problems:
    print(f"  row {number} {row!r}: {why}")
print(f"{len(good)} good, {len(problems)} rejected")

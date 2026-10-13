"""Day 4: User input. 10 examples, simple to complex.

Run:  python3 week1_basics/day04_input/more_examples.py

These examples use a helper called ask() instead of input(), so the file runs
by itself with pre-written answers. To type the answers yourself, change
SIMULATE to False. Everything else stays the same.
"""

SIMULATE = True

# Pre-written "typed" answers, handed out one at a time in order.
_fake_answers = iter([
    "Sam",                              # 1
    "30",                               # 2
    "3",                                # 3
    "1.75",                             # 4
    "  paris  ",                        # 5
    "12", "5",                          # 6
    "abc", "", "42",                    # 7 (two bad tries, then good)
    "maybe", "YES",                     # 8
    "9", "2",                           # 9
    "oops", "100",                      # 10
])


def ask(prompt):
    """Return what the user types (or the next scripted answer)."""
    if SIMULATE:
        answer = next(_fake_answers)
        print(f"{prompt}{answer}   <- simulated")
        return answer
    return input(prompt)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Ask a question, use the answer")
# WHAT: the simplest input program.
# HOW : input() shows the prompt, waits, and returns what was typed.
# WHY : input is how data gets INTO your program from outside.
name = ask("Your name? ")
print("Hello,", name)

# ---------------------------------------------------------------
show(2, "Input is ALWAYS text")
# WHAT: prove the type of what you get back.
# HOW : even if you type 30, you receive the string "30".
# WHY : this one fact explains most beginner input bugs.
age_text = ask("Your age? ")
print(type(age_text).__name__, repr(age_text))

# ---------------------------------------------------------------
show(3, "Convert to a whole number")
# WHAT: turn text into an int so maths works.
# HOW : int(text). Without it, "3" * 2 would repeat text instead of multiplying.
# WHY : convert immediately after reading, then forget about text.
quantity = int(ask("How many items? "))
print("Double is", quantity * 2)
print('Without int, "3" * 2 would give:', "3" * 2)

# ---------------------------------------------------------------
show(4, "Convert to a decimal and calculate")
# WHAT: read a decimal number and use it.
# HOW : float(text) for numbers with a decimal point.
# WHY : heights, prices and measurements are decimals.
height_m = float(ask("Height in metres? "))
print(f"That is {height_m * 100:.0f} cm")

# ---------------------------------------------------------------
show(5, "Clean messy input")
# WHAT: tidy what the user typed.
# HOW : strip() removes outer spaces; title() capitalises each word.
# WHY : users add spaces and mix case; clean data on arrival.
city = ask("City? ").strip().title()
print(f"Welcome from {city}!")

# ---------------------------------------------------------------
show(6, "Two numbers, one calculation")
# WHAT: input -> process -> output with two values.
# HOW : read both, convert both, calculate, print.
# WHY : the shape of almost every small program.
a = int(ask("First number? "))
b = int(ask("Second number? "))
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b:.2f}")


# ---------------------------------------------------------------
show(7, "Keep asking until the answer is a number")
# WHAT: a reusable function that never crashes on bad input.
# HOW : a loop asks again; try/except catches the ValueError from int().
#       (while is Day 9, try/except is Day 16: a preview of both.)
# WHY : real users type anything; robust programs expect that.
def ask_int(prompt):
    while True:
        text = ask(prompt)
        try:
            return int(text)
        except ValueError:
            print("  Please type a whole number.")


print("You chose", ask_int("Pick a number: "))


# ---------------------------------------------------------------
show(8, "A yes/no question")
# WHAT: accept only valid answers, in any letter case.
# HOW : lower() makes comparison case-insensitive; 'in' checks a set of options.
# WHY : constrained answers make later decisions simple.
def ask_yes_no(prompt):
    while True:
        answer = ask(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please answer yes or no.")


print("Confirmed:", ask_yes_no("Continue? (yes/no) "))


# ---------------------------------------------------------------
show(9, "A menu choice within a range")
# WHAT: ask for a number that must be between two limits.
# HOW : combine conversion, validation and a range check.
# WHY : menus and ratings both need this.
def ask_choice(prompt, low, high):
    while True:
        value = ask_int(prompt)
        if low <= value <= high:
            return value
        print(f"  Choose between {low} and {high}.")


choice = ask_choice("Menu option (1-5): ", 1, 5)
print("You picked option", choice)


# ---------------------------------------------------------------
show(10, "Mini program: temperature converter with validation")
# WHAT: put the helpers together into a small tool.
# HOW : read a validated number, convert it, print a formatted result.
# WHY : small functions + validation = a program you can trust.
def ask_float(prompt):
    while True:
        try:
            return float(ask(prompt))
        except ValueError:
            print("  Please type a number.")


celsius = ask_float("Temperature in Celsius? ")
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius:.1f} C = {fahrenheit:.1f} F")

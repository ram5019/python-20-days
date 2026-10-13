"""Day 6: Conditionals (if / elif / else). 10 examples, simple to complex.

Run:  python3 week1_basics/day06_conditionals/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "A single if")
# WHAT: run code only when a condition is True.
# HOW : the line ends with a colon; the block is indented 4 spaces.
# WHY : the first way a program can choose what to do.
temperature = 35
if temperature > 30:
    print("It's hot")
print("This line always runs (it is not indented)")

# ---------------------------------------------------------------
show(2, "if / else: exactly one of two paths")
# WHAT: two outcomes, one always runs.
# HOW : else has no condition; it catches everything else.
# WHY : "yes or no" decisions.
age = 16
if age >= 18:
    print("Adult")
else:
    print("Minor")

# ---------------------------------------------------------------
show(3, "if / elif / else: many paths, first match wins")
# WHAT: grade from marks.
# HOW : Python checks top to bottom and stops at the FIRST True condition.
#       Order matters: put the strictest condition first.
# WHY : any rule with several ranges works like this.
for marks in (95, 80, 65, 40):
    if marks >= 90:
        grade = "A"
    elif marks >= 75:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    else:
        grade = "F"
    print(marks, "->", grade)

# ---------------------------------------------------------------
show(4, "Combining conditions with and / or / not")
# WHAT: a rule with several parts.
# HOW : and = all must be True; or = any one; not = flip.
# WHY : real rules are rarely a single comparison.
has_ticket, age, is_vip = True, 15, False
if has_ticket and (age >= 18 or is_vip):
    print("Entry allowed")
else:
    print("Entry denied")
if not has_ticket:
    print("Please buy a ticket")

# ---------------------------------------------------------------
show(5, "Nested if: a decision inside a decision")
# WHAT: check the password only if the user exists.
# HOW : the inner if sits inside the outer block (8 spaces).
# WHY : when the second question only makes sense after the first.
#       (Never store real passwords in code; this is only practice.)
users = {"sam": "pw123"}
username, password = "sam", "wrong"
if username in users:
    if users[username] == password:
        print("Welcome")
    else:
        print("Wrong password")
else:
    print("Unknown user")

# ---------------------------------------------------------------
show(6, "Truthiness: what counts as False")
# WHAT: conditions do not have to be True/False.
# HOW : 0, "", [], {}, None and False are "falsy"; almost everything else
#       is "truthy".
# WHY : the idiomatic way to ask "is there anything here?".
for value in (0, 1, "", "hi", [], [0], None):
    print(f"{value!r:>6} is", "truthy" if value else "falsy")
name = ""
if not name:
    print("Name is empty")

# ---------------------------------------------------------------
show(7, "The one-line conditional expression")
# WHAT: choose a VALUE based on a condition.
# HOW : value_if_true if condition else value_if_false.
# WHY : compact and readable for simple choices.
n = 10
label = "even" if n % 2 == 0 else "odd"
print(label)
price = 120
shipping = 0 if price >= 100 else 9.99
print("Shipping:", shipping)

# ---------------------------------------------------------------
show(8, "Testing membership with in")
# WHAT: replace long chains of == with one in.
# HOW : letter in "aeiou"; day in (tuple of values).
# WHY : shorter and easier to extend.
for letter in ("a", "k"):
    if letter in "aeiou":
        print(letter, "is a vowel")
    else:
        print(letter, "is a consonant")
day = "Sat"
print("Weekend" if day in ("Sat", "Sun") else "Weekday")

# ---------------------------------------------------------------
show(9, "Guard clauses: check bad cases first, return early")
# WHAT: a function that rejects bad input before doing the real work.
# HOW : each if returns immediately, so the main logic stays un-nested.
# WHY : flatter code, easier to read than deeply nested ifs.
def describe_bmi(weight_kg, height_m):
    if height_m <= 0 or weight_kg <= 0:
        return "invalid input"
    bmi = weight_kg / height_m ** 2
    if bmi < 18.5:
        return f"{bmi:.1f}: underweight"
    if bmi < 25:
        return f"{bmi:.1f}: normal"
    if bmi < 30:
        return f"{bmi:.1f}: overweight"
    return f"{bmi:.1f}: obese"


print(describe_bmi(70, 1.75))
print(describe_bmi(50, 1.80))
print(describe_bmi(70, 0))

# ---------------------------------------------------------------
show(10, "Mini program: shipping cost calculator")
# WHAT: many rules in one function.
# HOW : weight bands with elif, a surcharge with if, a discount with and.
# WHY : business rules look exactly like this.
def shipping_cost(weight_kg, country, order_total):
    if weight_kg <= 0:
        return None                          # invalid
    if weight_kg <= 1:
        cost = 5
    elif weight_kg <= 5:
        cost = 12
    else:
        cost = 25
    if country != "FR":
        cost += 10                           # international surcharge
    if order_total >= 100 and country == "FR":
        cost = 0                             # free domestic shipping
    return cost


for case in [(0.5, "FR", 20), (3, "DE", 40), (8, "FR", 150), (-1, "FR", 10)]:
    print(case, "->", shipping_cost(*case))

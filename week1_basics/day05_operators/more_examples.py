"""Day 5: Operators. 10 examples, simple to complex.

Run:  python3 week1_basics/day05_operators/more_examples.py
"""

import math


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Basic arithmetic")
# WHAT: add, subtract, multiply.
# HOW : + - * work like a calculator.
# WHY : the PROCESS step of every program.
print(12 + 5, 12 - 5, 12 * 5)

# ---------------------------------------------------------------
show(2, "The four division-style operators")
# WHAT: /  //  %  ** side by side, on the same numbers.
# HOW : / true division (float); // floor division (whole part);
#       % remainder; ** power.
# WHY : // and % are a pair: 17 sweets shared among 5 kids -> 3 each, 2 left.
a, b = 17, 5
print(a / b, a // b, a % b, a ** 2)

# ---------------------------------------------------------------
show(3, "Order of operations")
# WHAT: which part is calculated first.
# HOW : ** first, then * / // %, then + -. Parentheses override everything.
# WHY : when in doubt, add parentheses; the next reader will thank you.
print(2 + 3 * 4)
print((2 + 3) * 4)
print(2 ** 3 ** 2)          # right-to-left: 2 ** (3 ** 2) = 512
print(-3 ** 2, (-3) ** 2)   # -9 and 9

# ---------------------------------------------------------------
show(4, "Shortcut assignment: += -= *= /=")
# WHAT: update a variable using its own value.
# HOW : x += 5 means x = x + 5.
# WHY : counters and running totals everywhere.
score = 10
score += 5
score *= 2
score -= 3
score //= 4
print(score)

# ---------------------------------------------------------------
show(5, "Comparison operators give True or False")
# WHAT: ask yes/no questions about values.
# HOW : == != < > <= >=. NOTE: = stores, == compares.
# WHY : these answers drive every decision (Day 6).
print(5 == 5, 5 != 5, 5 < 3, 5 >= 5)
print("apple" == "apple", "a" < "b")
print(3 == 3.0)

# ---------------------------------------------------------------
show(6, "Chained comparisons")
# WHAT: check a range in one expression.
# HOW : 1 <= x <= 10 means (1 <= x) and (x <= 10).
# WHY : reads like maths, and avoids repeating x.
x = 7
print(1 <= x <= 10)
print(10 < x < 20)

# ---------------------------------------------------------------
show(7, "Logical operators: and, or, not")
# WHAT: combine yes/no answers.
# HOW : and = both; or = at least one; not = flip.
# WHY : real conditions have several parts ("adult AND has a ticket").
print("and:")
for p in (True, False):
    for q in (True, False):
        print(f"  {p!s:5} and {q!s:5} -> {p and q}")
print("or  :", True or False, False or False)
print("not :", not True, not False)

# ---------------------------------------------------------------
show(8, "Everyday uses of % and //")
# WHAT: even/odd, clock time, wrap-around.
# HOW : n % 2 == 0 means even; // and % split minutes into hours and minutes;
#       % cycles back to 0.
# WHY : paging, scheduling, round-robin and many puzzles use these.
n = 7
print(n, "is even" if n % 2 == 0 else "is odd")
minutes = 135
print(f"{minutes} minutes = {minutes // 60} h {minutes % 60} min")
today = 5                           # 0=Mon ... 6=Sun
print("3 days later is day", (today + 3) % 7)

# ---------------------------------------------------------------
show(9, "Floating-point surprise")
# WHAT: 0.1 + 0.2 is not exactly 0.3 in a computer.
# HOW : decimals are stored in binary and cannot all be exact.
#       Compare with math.isclose or round instead of ==.
# WHY : prevents very confusing bugs with money and measurements.
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(round(0.1 + 0.2, 2) == 0.3)

# ---------------------------------------------------------------
show(10, "Mini program: eligibility and leap year checks")
# WHAT: combine arithmetic, comparison and logic.
# HOW : build each rule as a True/False expression, then combine.
# WHY : turning rules into expressions is the heart of programming.
age, has_id, order_total = 20, True, 75.0
can_buy = age >= 18 and has_id
free_shipping = order_total >= 50 or age >= 65
print("Can buy:", can_buy, "| Free shipping:", free_shipping)

for year in (1900, 2000, 2024, 2025):
    leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
    print(year, "leap" if leap else "not leap")

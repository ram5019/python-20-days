"""Day 7: Mini project (age calculator). 10 examples, simple to complex.

Run:  python3 week1_basics/day07_project_age_calculator/more_examples.py

Dates are fixed (TODAY) so the output is the same every time you run it.
Change TODAY to date.today() to use the real current date.
"""

from datetime import date

TODAY = date(2026, 10, 13)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Age from birth year only")
# WHAT: the simplest version.
# HOW : this year minus birth year (can be off by one before the birthday).
# WHY : a first working program; refine it in later examples.
birth_year = 1995
print("Age about", TODAY.year - birth_year)

# ---------------------------------------------------------------
show(2, "Exact age, using month and day too")
# WHAT: subtract one if the birthday has not happened yet this year.
# HOW : compare (month, day) pairs; a True comparison counts as 1.
# WHY : correctness: details matter even in small programs.
def exact_age(born, today):
    had_birthday = (today.month, today.day) >= (born.month, born.day)
    return today.year - born.year - (0 if had_birthday else 1)


print(exact_age(date(1995, 3, 20), TODAY))     # birthday already passed
print(exact_age(date(1995, 12, 5), TODAY))     # birthday still to come

# ---------------------------------------------------------------
show(3, "Days until the next birthday")
# WHAT: how long to wait.
# HOW : build this year's birthday; if it is past, use next year's.
# WHY : date arithmetic: subtracting two dates gives a timedelta (.days).
def days_until_birthday(born, today):
    this_year = date(today.year, born.month, born.day)
    if this_year < today:
        this_year = date(today.year + 1, born.month, born.day)
    return (this_year - today).days


print(days_until_birthday(date(1995, 12, 5), TODAY))
print(days_until_birthday(date(1995, 10, 13), TODAY))      # today!

# ---------------------------------------------------------------
show(4, "Classify the life stage")
# WHAT: map a number to a label.
# HOW : an if/elif chain, smallest range first.
# WHY : the same shape as the grade example (Day 6).
def life_stage(age):
    if age < 0:
        return "not born yet"
    elif age < 13:
        return "child"
    elif age < 20:
        return "teenager"
    elif age < 60:
        return "adult"
    return "senior"


for a in (-1, 8, 16, 35, 70):
    print(a, "->", life_stage(a))

# ---------------------------------------------------------------
show(5, "Age in different units")
# WHAT: the same age as days, weeks and hours.
# HOW : subtract two dates; divide the day count.
# WHY : unit conversion is simple arithmetic with clear names.
born = date(1995, 3, 20)
days_alive = (TODAY - born).days
print("Days  :", days_alive)
print("Weeks :", days_alive // 7)
print("Hours :", days_alive * 24)

# ---------------------------------------------------------------
show(6, "Validating a birth date")
# WHAT: reject impossible input.
# HOW : try to build a date (Python raises ValueError for 30 February),
#       then check it is not in the future.
# WHY : never trust input (Day 4). Validation is half of any real program.
def parse_birth_date(year, month, day):
    try:
        born = date(year, month, day)
    except ValueError as error:
        return None, f"invalid date: {error}"
    if born > TODAY:
        return None, "date is in the future"
    return born, "ok"


print(parse_birth_date(1995, 3, 20))
print(parse_birth_date(1995, 2, 30))
print(parse_birth_date(2030, 1, 1))

# ---------------------------------------------------------------
show(7, "Compare two people")
# WHAT: who is older, and by how many days?
# HOW : compare dates directly (earlier date = older person).
# WHY : comparing values is Day 5; dates support the same operators.
sam, alex = date(1995, 3, 20), date(1998, 7, 2)
older, younger = ("Sam", "Alex") if sam < alex else ("Alex", "Sam")
print(f"{older} is older than {younger} by {abs((sam - alex).days)} days")

# ---------------------------------------------------------------
show(8, "Chinese zodiac from the birth year")
# WHAT: a fun lookup with the remainder operator.
# HOW : (year - 4) % 12 cycles through 12 animals.
# WHY : % is perfect for anything that repeats in a cycle.
ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
           "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
for year in (1995, 2000, 2024):
    print(year, "->", ANIMALS[(year - 4) % 12])

# ---------------------------------------------------------------
show(9, "Retirement countdown")
# WHAT: years and days until a target age.
# HOW : compute the date of the target birthday, then subtract today.
# WHY : "how long until X" is a very common question in software.
def countdown_to_age(born, target_age, today):
    try:
        target_date = date(born.year + target_age, born.month, born.day)
    except ValueError:                            # born on 29 February
        target_date = date(born.year + target_age, 3, 1)
    days = (target_date - today).days
    if days < 0:
        return "already passed"
    return f"{days // 365} years and {days % 365} days to go"


print(countdown_to_age(date(1995, 3, 20), 60, TODAY))
print(countdown_to_age(date(1950, 3, 20), 60, TODAY))

# ---------------------------------------------------------------
show(10, "The complete age report")
# WHAT: combine every piece into one function with a tidy printout.
# HOW : small functions (examples 2 to 8) are called by a manager function.
# WHY : small pieces + one coordinator is how bigger programs are built.
def age_report(name, born, today=TODAY):
    age = exact_age(born, today)
    lines = [
        f"Report for {name.title()}",
        "-" * 28,
        f"Born       : {born.isoformat()}",
        f"Age        : {age} ({life_stage(age)})",
        f"Next b-day : in {days_until_birthday(born, today)} days",
        f"Days alive : {(today - born).days:,}",
        f"In 10 years: {age + 10}",
    ]
    return "\n".join(lines)


print(age_report("sam", date(1995, 3, 20)))

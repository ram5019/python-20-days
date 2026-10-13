"""Day 3: Strings. 10 examples, simple to complex.

Run:  python3 week1_basics/day03_strings/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Join and repeat")
# WHAT: build bigger strings from smaller ones.
# HOW : + joins, * repeats. Add your own spaces.
# WHY : the basis of every message your programs print.
first = "Ada"
last = "Lovelace"
print(first + " " + last)
print("ha" * 3)
print("-" * 15)

# ---------------------------------------------------------------
show(2, "Length and positions")
# WHAT: count characters and pick one by position.
# HOW : len() counts; [0] is the FIRST character; [-1] is the LAST.
# WHY : positions start at 0, the number one beginner trip-up.
word = "Python"
print(len(word))
print(word[0], word[5], word[-1], word[-2])

# ---------------------------------------------------------------
show(3, "Slicing")
# WHAT: take a piece of a string.
# HOW : [start:stop] includes start and EXCLUDES stop. Leave one out for
#       "from the start" or "to the end". [::-1] reverses.
# WHY : slicing works the same way on lists (Day 10).
word = "Python"
print(word[0:3])        # Pyt
print(word[:2])         # Py
print(word[2:])         # thon
print(word[::-1])       # nohtyP

# ---------------------------------------------------------------
show(4, "Case and cleaning")
# WHAT: change case, trim spaces.
# HOW : methods return a NEW string; the original never changes.
# WHY : users type messy data; clean it before using it.
raw = "   Hello, World   "
print(raw.strip())
print(raw.strip().lower())
print(raw.strip().upper())
print("hello world".title())

# ---------------------------------------------------------------
show(5, "f-strings: put variables into text")
# WHAT: build sentences with values inside.
# HOW : f"...{name}..." evaluates what is inside { }. :.2f gives 2 decimals.
# WHY : cleaner than joining with + and str().
name = "Sam"
age = 30
price = 4.5
print(f"{name} is {age} years old")
print(f"Total: {price * 3:.2f}")
print(f"{name!r} in quotes, {age:>5} right-aligned")

# ---------------------------------------------------------------
show(6, "Checking what is inside")
# WHAT: ask yes/no questions about text.
# HOW : in, startswith, endswith, find, count. The answers are bool/int.
# WHY : these answers become the conditions of if statements (Day 6).
email = "sam@example.com"
print("@" in email)
print(email.endswith(".com"))
print(email.startswith("sam"))
print(email.find("@"))              # position, or -1 if missing
print("banana".count("a"))

# ---------------------------------------------------------------
show(7, "Replace and split")
# WHAT: edit text and cut it into pieces.
# HOW : replace(old, new); split(sep) returns a LIST of strings.
# WHY : parsing lines such as "name,age,city" is everyday work.
line = "Sam,30,Paris"
print(line.replace(",", " | "))
parts = line.split(",")
print(parts)
print(parts[2])

# ---------------------------------------------------------------
show(8, "Join: the opposite of split")
# WHAT: glue a list of strings into one.
# HOW : "separator".join(list). The separator goes BETWEEN items.
# WHY : building CSV lines, paths and sentences from pieces.
words = ["disk", "full", "on", "node-3"]
print(" ".join(words))
print("-".join(words))
print(",".join(["a", "b", "c"]))

# ---------------------------------------------------------------
show(9, "Immutability: strings never change in place")
# WHAT: see that methods give new strings.
# HOW : text.upper() returns a new value; you must store it to keep it.
# WHY : forgetting this causes the classic "nothing changed" bug.
text = "python"
text.upper()                         # result thrown away
print(text)                          # still lowercase
text = text.upper()                  # now we keep it
print(text)
try:
    text[0] = "J"                    # cannot assign into a string
except TypeError as error:
    print("Error:", error)

# ---------------------------------------------------------------
show(10, "Mini program: parse and tidy a log line")
# WHAT: combine split, strip, slicing, in, f-strings.
# HOW : cut the line into fields, clean each one, then report.
# WHY : turning messy text into clean data is a core automation skill.
log = "  2026-10-13 | ERROR |  Disk full on node-3  "
date, level, message = [part.strip() for part in log.split("|")]
print(f"Date   : {date}")
print(f"Level  : {level.lower()}")
print(f"Message: {message}")
print("Is it serious?", level == "ERROR")
print("Mentions disk?", "disk" in message.lower())
print("Node   :", message.split()[-1])

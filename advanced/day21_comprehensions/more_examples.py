"""Day 21: Comprehensions. 10 examples, simple to complex.

Run:  python3 advanced/day21_comprehensions/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "From a loop to a comprehension")
# WHAT: the same list built two ways.
# HOW : [expression for item in sequence]. Read it as "n*n for each n".
# WHY : one readable line instead of three.
squares_loop = []
for n in range(1, 6):
    squares_loop.append(n * n)
squares = [n * n for n in range(1, 6)]
print(squares, squares == squares_loop)

# ---------------------------------------------------------------
show(2, "Transform every item")
# WHAT: apply an operation to a whole list.
# HOW : put the operation in front of the for.
# WHY : cleaning, converting and formatting data.
names = ["  ana ", "RAVI", "meena"]
print([n.strip().title() for n in names])
prices_text = ["4.50", "12", "3.25"]
print([float(p) for p in prices_text])
print([len(n.strip()) for n in names])

# ---------------------------------------------------------------
show(3, "Filter with if at the END")
# WHAT: keep only the items that pass a test.
# HOW : [x for x in data if condition]. Items that fail are dropped.
# WHY : the loop-test-append pattern in one line.
scores = [45, 82, 67, 91, 30]
print([s for s in scores if s >= 50])
print([n for n in range(1, 21) if n % 3 == 0])
words = ["sun", "moon", "star", "sky"]
print([w for w in words if w.startswith("s")])

# ---------------------------------------------------------------
show(4, "if/else INSIDE: choose a value for every item")
# WHAT: label each item.
# HOW : [a if cond else b for x in data]. The if/else goes at the FRONT.
# WHY : filtering (end) drops items; choosing (front) keeps them all.
print(["pass" if s >= 50 else "fail" for s in scores])
print([abs(n) for n in [-3, 2, -1]])
print(["even" if n % 2 == 0 else "odd" for n in range(5)])

# ---------------------------------------------------------------
show(5, "Filter AND transform together")
# WHAT: both ideas in one expression.
# HOW : the value expression at the front, the filter at the end.
# WHY : the most common real-world form.
orders = [120.0, 15.5, 80.0, 300.0, 9.99]
print([round(o * 1.18, 2) for o in orders if o >= 50])
text = "Hello World from Python"
print([w.upper() for w in text.split() if len(w) > 4])

# ---------------------------------------------------------------
show(6, "Two loops in one comprehension")
# WHAT: flatten a grid; build all pairs.
# HOW : the for parts read in the same order as nested loops.
# WHY : replaces a nested loop that appends.
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print([v for row in grid for v in row])
print([(c, n) for c in "AB" for n in (1, 2)])
print([[row[i] for row in grid] for i in range(3)])       # transpose

# ---------------------------------------------------------------
show(7, "Dictionary comprehensions")
# WHAT: build a dict from a sequence.
# HOW : {key: value for ...}.
# WHY : lookups, inversions, counting tables.
print({n: n ** 2 for n in range(1, 6)})
fruits = ["apple", "fig", "banana"]
print({f: len(f) for f in fruits})
codes = {"FR": "France", "DE": "Germany"}
print({v: k for k, v in codes.items()})
print({k: v for k, v in {"a": 1, "b": 0, "c": 3}.items() if v})

# ---------------------------------------------------------------
show(8, "Set comprehensions: unique results")
# WHAT: a comprehension that removes duplicates.
# HOW : curly braces WITHOUT a colon.
# WHY : distinct domains, distinct first letters.
emails = ["a@x.com", "b@x.com", "c@y.org", "d@x.com"]
print(sorted({e.split("@")[1] for e in emails}))
print(sorted({w[0] for w in ["apple", "avocado", "banana"]}))

# ---------------------------------------------------------------
show(9, "Data wrangling on a list of dicts")
# WHAT: extract, filter and reshape records.
# HOW : comprehensions over dictionaries combine with sorted/sum/max.
# WHY : what you will do all day with API and CSV data.
people = [
    {"name": "Asha", "dept": "IT", "salary": 50},
    {"name": "Ravi", "dept": "HR", "salary": 40},
    {"name": "Meena", "dept": "IT", "salary": 65},
]
print([p["name"] for p in people if p["dept"] == "IT"])
print(sum(p["salary"] for p in people if p["dept"] == "IT"))
print({p["name"]: p["salary"] for p in people})
print(sorted((p["name"] for p in people), reverse=True))
by_dept = {d: [p["name"] for p in people if p["dept"] == d]
           for d in {p["dept"] for p in people}}
print(dict(sorted(by_dept.items())))

# ---------------------------------------------------------------
show(10, "When NOT to use one, and a readable middle ground")
# WHAT: a comprehension that has become unreadable, then a cleaner version.
# HOW : move complicated logic into a named function.
# WHY : the goal is clarity, not fewer lines.
data = ["10", "x", "30", "", "50.5", "70"]
# Too clever (hard to read):
# [int(v) for v in data if v.isdigit() and int(v) > 20 and int(v) % 10 == 0]


def is_round_big_number(text):
    return text.isdigit() and int(text) > 20 and int(text) % 10 == 0


print([int(v) for v in data if is_round_big_number(v)])
print("Rule of thumb: if it needs more than one line to read, use a normal loop.")

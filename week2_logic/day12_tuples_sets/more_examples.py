"""Day 12: Tuples and sets. 10 examples, simple to complex.

Run:  python3 week2_logic/day12_tuples_sets/more_examples.py
"""

import time


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "A tuple: an ordered, fixed record")
# WHAT: group related values that belong together.
# HOW : round brackets; index like a list. A one-item tuple needs a comma.
# WHY : coordinates, dates and database rows are fixed records.
point = (10, 20)
print(point, point[0], point[-1], len(point))
print(type((5,)).__name__, type((5)).__name__)       # tuple vs just an int

# ---------------------------------------------------------------
show(2, "Tuples cannot be changed")
# WHAT: see the error.
# HOW : assignment into a tuple raises TypeError.
# WHY : this is a FEATURE: nobody can change the record by accident.
try:
    point[0] = 99
except TypeError as error:
    print("Error:", error)
new_point = (99,) + point[1:]               # build a new one instead
print(new_point)

# ---------------------------------------------------------------
show(3, "Unpacking and swapping")
# WHAT: split a tuple into separate variables in one line.
# HOW : the count of names must match the count of values; * collects extras.
# WHY : you already used this in enumerate and dict.items().
name, role, years = ("Sam", "Engineer", 5)
print(name, role, years)
first, *middle, last = (1, 2, 3, 4, 5)
print(first, middle, last)
a, b = 1, 2
a, b = b, a
print(a, b)

# ---------------------------------------------------------------
show(4, "Functions that return several values")
# WHAT: give back more than one answer.
# HOW : `return x, y` really returns ONE tuple; the caller unpacks it.
# WHY : min and max, or (success, message), in a single call.
def min_max(values):
    return min(values), max(values)


low, high = min_max([4, 9, 2, 7])
print(low, high)
result = min_max([1, 2])
print(result, type(result).__name__)

# ---------------------------------------------------------------
show(5, "Tuples as dictionary keys and in lists")
# WHAT: tuples are allowed where lists are not.
# HOW : a key must never change, so tuples (immutable) work as keys.
# WHY : grids, (row, col) lookups, composite keys.
distances = {("Paris", "Lyon"): 465, ("Paris", "Nice"): 930}
print(distances[("Paris", "Nice")])
people = [("Asha", 88), ("Ravi", 72)]
for person, score in people:
    print(person, score)

# ---------------------------------------------------------------
show(6, "A set: unique items, no order")
# WHAT: duplicates disappear automatically.
# HOW : curly braces (or set(...)). There is no index.
# WHY : "which distinct values do I have?".
ids = {1, 2, 2, 3, 3, 3}
print(ids, len(ids))
print(set("mississippi"))
print(len(set([4, 4, 5, 6, 6])))

# ---------------------------------------------------------------
show(7, "Add, remove and fast membership")
# WHAT: change a set, and test membership quickly.
# HOW : add / discard (discard never errors) / remove (errors if missing).
#       `in` on a set jumps straight to the answer; on a list it scans.
# WHY : checking membership in big collections.
colors = {"red", "green"}
colors.add("blue")
colors.add("red")                          # ignored: already there
colors.discard("yellow")                   # fine even though missing
colors.remove("green")
print(sorted(colors))
big_list = list(range(300_000))
big_set = set(big_list)
t = time.perf_counter()
for _ in range(100):
    299_999 in big_list
list_time = time.perf_counter() - t
t = time.perf_counter()
for _ in range(100):
    299_999 in big_set
set_time = time.perf_counter() - t
print("set lookup faster than list lookup:", set_time < list_time)

# ---------------------------------------------------------------
show(8, "Set operations like Venn diagrams")
# WHAT: compare two groups.
# HOW : & both, | either, - only in the first, ^ in exactly one.
# WHY : "who is in both?", "who is missing?", "what changed?".
team_a = {"ravi", "sita", "arun"}
team_b = {"sita", "john", "arun"}
print("both      :", sorted(team_a & team_b))
print("either    :", sorted(team_a | team_b))
print("only in A :", sorted(team_a - team_b))
print("one only  :", sorted(team_a ^ team_b))
print("subset?   :", {"sita"} <= team_a)

# ---------------------------------------------------------------
show(9, "Removing duplicates from a list")
# WHAT: unique values from a list, two flavours.
# HOW : set() loses the order; dict.fromkeys keeps first-seen order;
#       sorted(set(...)) gives a sorted unique list.
# WHY : cleaning data (Day 11 did this with a loop).
raw = [3, 1, 3, 2, 1, 5]
print(sorted(set(raw)))
print(list(dict.fromkeys(raw)))

# ---------------------------------------------------------------
show(10, "Mini program: compare two server lists")
# WHAT: which servers are down, which are new, which alerts are duplicates?
# HOW : sets make each question one expression.
# WHY : a typical audit/monitoring task.
all_nodes = {"n1", "n2", "n3", "n4", "n5"}
healthy = {"n1", "n3", "n5"}
alerts = ["n2", "n4", "n2", "n2", "n4"]
print("Unhealthy nodes   :", sorted(all_nodes - healthy))
print("Nodes with alerts :", sorted(set(alerts)))
print("Alerts on healthy :", sorted(set(alerts) & healthy) or "none")
print("Unknown to inventory:", sorted(set(["n9", "n1"]) - all_nodes))
words = "the cat and the hat and the bat".split()
print("Distinct words:", len(set(words)), "of", len(words))

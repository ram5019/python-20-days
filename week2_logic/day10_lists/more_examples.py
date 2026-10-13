"""Day 10: Lists. 10 examples, simple to complex.

Run:  python3 week2_logic/day10_lists/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Create a list and ask its size")
# WHAT: many values under one name.
# HOW : square brackets and commas; len() counts the items.
# WHY : real data comes in groups, not single values.
servers = ["web01", "web02", "db01"]
print(servers)
print(len(servers))
empty = []
print(empty, len(empty))

# ---------------------------------------------------------------
show(2, "Indexing: first, last, from the end")
# WHAT: pick one item by position.
# HOW : counting starts at 0; negative numbers count from the end.
# WHY : same rules as strings (Day 3).
print(servers[0], servers[2], servers[-1], servers[-2])
try:
    print(servers[3])
except IndexError as error:
    print("Error:", error)

# ---------------------------------------------------------------
show(3, "Slicing: take a piece")
# WHAT: get several items as a NEW list.
# HOW : [start:stop] excludes stop; [::-1] reverses; [::2] every other item.
# WHY : "first 3", "last 5" and "every 10th" are common needs.
nums = [10, 20, 30, 40, 50, 60]
print(nums[1:4])
print(nums[:2], nums[-2:])
print(nums[::2])
print(nums[::-1])

# ---------------------------------------------------------------
show(4, "Lists can change (mutable)")
# WHAT: replace an item in place.
# HOW : list[index] = new_value. Strings cannot do this; lists can.
# WHY : lists are the "working memory" of a program.
servers[1] = "web99"
print(servers)
marks = [50, 60, 70]
marks[0] += 10
marks[-1] = marks[-1] * 2
print(marks)

# ---------------------------------------------------------------
show(5, "Loop over a list, with and without positions")
# WHAT: visit every item.
# HOW : a for loop gives items; enumerate gives (position, item).
# WHY : the standard pairing: list + for.
for s in servers:
    print("Checking", s)
for position, s in enumerate(servers, start=1):
    print(f"{position}. {s}")

# ---------------------------------------------------------------
show(6, "Built-in helpers for number lists")
# WHAT: totals and extremes without writing a loop.
# HOW : sum, min, max, len, sorted. sorted returns a NEW list.
# WHY : quick statistics.
data = [72, 88, 95, 60, 88]
print("sum", sum(data), "| min", min(data), "| max", max(data))
print("average", sum(data) / len(data))
print("sorted", sorted(data))
print("sorted descending", sorted(data, reverse=True))
print("original untouched", data)

# ---------------------------------------------------------------
show(7, "Is it in there? How many? Where?")
# WHAT: questions about contents.
# HOW : in -> True/False; count -> how many; index -> first position.
# WHY : check before you act (Day 6).
print(88 in data, 100 in data)
print(data.count(88))
print(data.index(95))

# ---------------------------------------------------------------
show(8, "Lists inside lists: a grid")
# WHAT: a table as a list of rows.
# HOW : grid[row][col]. Two loops visit every cell.
# WHY : spreadsheets, game boards and images are grids.
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print(grid[1][2])
for row in grid:
    print(row, "sum =", sum(row))
diagonal = [grid[i][i] for i in range(3)]
print("diagonal", diagonal)
flat = []
for row in grid:
    for value in row:
        flat.append(value)
print("flat", flat)

# ---------------------------------------------------------------
show(9, "The copying pitfall: two names, one list")
# WHAT: b = a does NOT copy a list.
# HOW : both names point to the same list, so a change through one shows
#       in the other. .copy() (or a[:]) makes a real copy.
# WHY : the source of many "why did my data change?" bugs.
a = [1, 2, 3]
b = a
b.append(4)
print("a:", a, "| b:", b, "| same object:", a is b)
c = a.copy()
c.append(5)
print("a:", a, "| c:", c, "| same object:", a is c)

# ---------------------------------------------------------------
show(10, "Mini program: a tiny gradebook")
# WHAT: several lists working together.
# HOW : parallel lists (names and scores), loops, statistics, a filter.
# WHY : this is where lists + loops + conditions become useful.
names = ["Asha", "Ravi", "Meena", "John"]
scores = [88, 72, 95, 55]
print("Class average:", sum(scores) / len(scores))
best_index = scores.index(max(scores))
print("Top student:", names[best_index], scores[best_index])
passed = [name for name, score in zip(names, scores) if score >= 60]
print("Passed:", passed)
ranking = sorted(zip(scores, names), reverse=True)
for rank, (score, name) in enumerate(ranking, start=1):
    print(f"  {rank}. {name:<6} {score}")

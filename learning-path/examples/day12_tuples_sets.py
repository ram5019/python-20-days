"""Day 12 example: tuples and sets.

Run:  python3 learning-path/examples/day12_tuples_sets.py
"""

# BLOCK 1: tuple: ordered, but cannot be changed
point = (10, 20)
print(point[0], point[1])
# point[0] = 99     # would raise TypeError

# BLOCK 2: tuple unpacking
x, y = point
print(f"x={x}, y={y}")
name, role, years = ("Ram", "TSE", 15)
print(name, role, years)

# BLOCK 3: swapping with tuples
a, b = 1, 2
a, b = b, a
print(a, b)                         # 2 1

# BLOCK 4: functions often return tuples
def min_max(values):
    return min(values), max(values)

low, high = min_max([4, 9, 2, 7])
print(low, high)                    # 2 9

# BLOCK 5: set: unordered, no duplicates
ids = {1, 2, 2, 3, 3, 3}
print(ids)                          # {1, 2, 3}
print(2 in ids)                     # True (very fast)

# BLOCK 6: remove duplicates from a list
emails = ["a@x.com", "b@x.com", "a@x.com"]
unique = list(set(emails))
print(len(unique))                  # 2

# BLOCK 7: add / remove on sets
ids.add(10)
ids.discard(1)                      # no error if missing
print(ids)

# BLOCK 8: set operations
team_a = {"ram", "sita", "arun"}
team_b = {"sita", "john", "arun"}
print(team_a & team_b)              # intersection (in both)
print(team_a | team_b)              # union (in either)
print(team_a - team_b)              # difference (only in A)

# BLOCK 9: empty containers (gotcha)
empty_set = set()                   # {} would create a dict!
empty_tuple = ()
print(type({}), type(empty_set))

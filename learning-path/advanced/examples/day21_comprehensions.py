"""Day 21 example: comprehensions.

Run:  python3 learning-path/advanced/examples/day21_comprehensions.py
"""

# BLOCK 1: the long way (Day 11) vs the comprehension
squares_loop = []
for n in range(1, 6):
    squares_loop.append(n * n)

squares = [n * n for n in range(1, 6)]
print(squares_loop == squares)            # True, same result

# BLOCK 2: with a filter (if at the end)
scores = [45, 82, 67, 91, 30]
passed = [s for s in scores if s >= 50]
print(passed)                             # [82, 67, 91]

# BLOCK 3: transform text
names = ["  ram ", "SITA", "arun"]
clean = [n.strip().title() for n in names]
print(clean)                              # ['Ram', 'Sita', 'Arun']

# BLOCK 4: if/else INSIDE (goes before the for)
labels = ["pass" if s >= 50 else "fail" for s in scores]
print(labels)

# BLOCK 5: dict comprehension
word_len = {w: len(w) for w in ["disk", "cluster", "node"]}
print(word_len)                           # {'disk': 4, 'cluster': 7, 'node': 4}

# BLOCK 6: set comprehension (unique values)
domains = {e.split("@")[1] for e in ["a@x.com", "b@x.com", "c@y.org"]}
print(domains)                            # {'x.com', 'y.org'} (order may vary)

# BLOCK 7: nested loop flattened
grid = [[1, 2, 3], [4, 5, 6]]
flat = [value for row in grid for value in row]
print(flat)                               # [1, 2, 3, 4, 5, 6]

# BLOCK 8: real-world: pull ERROR lines out of a log
log = ["INFO start", "ERROR disk full", "INFO ok", "ERROR timeout"]
errors = [line for line in log if line.startswith("ERROR")]
print(errors)

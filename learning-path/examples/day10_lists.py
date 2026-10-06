"""Day 10 example: lists.

Run:  python3 learning-path/examples/day10_lists.py
"""

# BLOCK 1: create and print a list
servers = ["web01", "web02", "db01"]
print(servers)
print(len(servers))             # 3

# BLOCK 2: index and slice (same rules as strings)
print(servers[0])               # web01
print(servers[-1])              # db01
print(servers[0:2])             # ['web01', 'web02']

# BLOCK 3: lists are MUTABLE (unlike strings)
servers[1] = "web99"
print(servers)

# BLOCK 4: loop over a list
for s in servers:
    print("Checking", s)

# BLOCK 5: loop with index using enumerate
for i, s in enumerate(servers, start=1):
    print(f"{i}. {s}")

# BLOCK 6: lists can hold mixed types, even other lists
mixed = ["Ram", 38, True, [1, 2, 3]]
print(mixed[3][0])              # 1

# BLOCK 7: totals and statistics
marks = [72, 88, 95, 60]
print("Total:", sum(marks))
print("Max:", max(marks), "Min:", min(marks))
print("Average:", sum(marks) / len(marks))

# BLOCK 8: copying pitfall
a = [1, 2, 3]
b = a                           # NOT a copy: same list, two names
b.append(4)
print(a)                        # [1, 2, 3, 4]
c = a.copy()                    # real copy
c.append(5)
print(a, c)

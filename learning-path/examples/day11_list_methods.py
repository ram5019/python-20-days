"""Day 11 example: list methods.

Run:  python3 learning-path/examples/day11_list_methods.py
"""

# BLOCK 1: add items
tasks = ["email", "review"]
tasks.append("deploy")              # add to the end
tasks.insert(0, "standup")          # add at position 0
tasks.extend(["lunch", "report"])   # add several
print(tasks)

# BLOCK 2: remove items
tasks.remove("lunch")               # by value (first match)
last = tasks.pop()                  # remove and RETURN last
first = tasks.pop(0)                # remove and return index 0
print(tasks, "| popped:", last, first)
del tasks[0]                        # remove by index, no return
print(tasks)

# BLOCK 3: search and count
nums = [5, 3, 8, 3, 1]
print(nums.index(8))                # position of first 8 -> 2
print(nums.count(3))                # how many 3s -> 2
print(8 in nums)                    # True

# BLOCK 4: sort and reverse
nums.sort()                         # changes nums in place
print(nums)
nums.sort(reverse=True)
print(nums)
print(sorted([3, 1, 2]))            # returns NEW list; original untouched

# BLOCK 5: .sort() returns None (classic bug)
result = [3, 1, 2].sort()
print(result)                       # None

# BLOCK 6: building a list in a loop
squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)

# BLOCK 7: filtering into a new list
scores = [45, 82, 67, 91, 30]
passed = []
for s in scores:
    if s >= 50:
        passed.append(s)
print(passed)

# BLOCK 8: list comprehension preview (Day 21)
squares2 = [n * n for n in range(1, 6)]
print(squares2)

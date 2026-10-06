"""Day 22 example: lambda, map, filter, sorted with key.

Run:  python3 learning-path/advanced/examples/day22_lambda_map_filter.py
"""

# BLOCK 1: a normal function vs a lambda
def double(x):
    return x * 2

double_l = lambda x: x * 2
print(double(5), double_l(5))             # 10 10

# BLOCK 2: map(): apply a function to every item
nums = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, nums))
print(doubled)                            # [2, 4, 6, 8]

# BLOCK 3: filter(): keep items where function returns True
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)                              # [2, 4]

# BLOCK 4: sorted() with key=: the MOST common use of lambda
students = [("Asha", 88), ("Ravi", 72), ("Meena", 95)]
by_marks = sorted(students, key=lambda s: s[1], reverse=True)
print(by_marks)

# BLOCK 5: key= with dicts
servers = [{"name": "web01", "cpu": 40}, {"name": "db01", "cpu": 85}]
busiest = max(servers, key=lambda s: s["cpu"])
print(busiest["name"])                    # db01

# BLOCK 6: passing a function as an argument
def apply_twice(func, value):
    return func(func(value))

print(apply_twice(lambda x: x + 3, 10))   # 16

# BLOCK 7: the same work as comprehensions (usually clearer)
print([x * 2 for x in nums])
print([x for x in nums if x % 2 == 0])

# BLOCK 8: a small pipeline
words = ["Disk", "cluster", "NODE", "io"]
result = sorted(
    filter(lambda w: len(w) > 2, map(str.lower, words)),
    key=len,
)
print(result)                             # ['disk', 'node', 'cluster']

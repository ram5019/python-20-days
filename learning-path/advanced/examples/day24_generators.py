"""Day 24 example: generators.

Run:  python3 learning-path/advanced/examples/day24_generators.py
"""

import sys

# BLOCK 1: a generator function uses yield instead of return
def count_up(limit):
    n = 1
    while n <= limit:
        yield n                  # pause here, hand back n
        n += 1                   # resumes here on the next request

for x in count_up(3):
    print(x)                     # 1 2 3

# BLOCK 2: see the pause/resume with next()
gen = count_up(2)
print(next(gen))                 # 1
print(next(gen))                 # 2
try:
    next(gen)
except StopIteration:
    print("generator exhausted")

# BLOCK 3: memory: list vs generator
big_list = [n for n in range(1_000_000)]
big_gen = (n for n in range(1_000_000))     # () not []
print(sys.getsizeof(big_list) > sys.getsizeof(big_gen))   # True
print(sum(big_gen))                          # works fine

# BLOCK 4: a generator is single-use
g = (n for n in range(3))
print(list(g))                   # [0, 1, 2]
print(list(g))                   # [] (already consumed)

# BLOCK 5: infinite sequence: impossible with a list
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(10)])        # first 10 Fibonacci numbers

# BLOCK 6: read a big file lazily (pattern; demo with a list)
def error_lines(lines):
    for line in lines:
        if "ERROR" in line:
            yield line.strip()

log = ["INFO ok\n", "ERROR disk\n", "INFO ok\n", "ERROR net\n"]
print(list(error_lines(log)))

# BLOCK 7: chaining generators into a pipeline
def numbers():
    yield from range(1, 11)

def squares(src):
    for n in src:
        yield n * n

def evens(src):
    for n in src:
        if n % 2 == 0:
            yield n

print(list(evens(squares(numbers()))))       # [4, 16, 36, 64, 100]

"""Day 8 example: for loops.

Run:  python3 learning-path/examples/day08_for_loop.py
"""

# BLOCK 1: repeat N times with range()
for i in range(5):
    print("Round", i)           # 0,1,2,3,4

# BLOCK 2: range with start, stop, step
for n in range(1, 11, 2):
    print(n, end=" ")           # 1 3 5 7 9
print()

# BLOCK 3: loop over a string
for ch in "WEKA":
    print(ch)

# BLOCK 4: accumulator pattern (running total)
total = 0
for n in range(1, 6):
    total += n
print("Sum 1..5 =", total)      # 15

# BLOCK 5: loop with a condition inside
for n in range(1, 11):
    if n % 2 == 0:
        print(n, "is even")

# BLOCK 6: nested loops (multiplication table)
for row in range(1, 4):
    for col in range(1, 4):
        print(row * col, end="\t")
    print()

# BLOCK 7: break and continue
for n in range(1, 10):
    if n == 3:
        continue                # skip 3
    if n == 6:
        break                   # stop completely at 6
    print(n)

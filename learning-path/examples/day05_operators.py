"""Day 5 example: operators.

Run:  python3 learning-path/examples/day05_operators.py
"""

# BLOCK 1: arithmetic
a, b = 17, 5
print(a + b)     # 22
print(a - b)     # 12
print(a * b)     # 85
print(a / b)     # 3.4   (always a float)
print(a // b)    # 3     (floor division)
print(a % b)     # 2     (remainder)
print(a ** 2)    # 289   (power)

# BLOCK 2: order of operations
print(2 + 3 * 4)      # 14
print((2 + 3) * 4)    # 20

# BLOCK 3: shortcut assignment
score = 10
score += 5       # same as score = score + 5
score *= 2
print(score)     # 30

# BLOCK 4: comparison (produces True/False)
print(5 == 5)    # True
print(5 != 3)    # True
print(5 > 10)    # False
print(5 <= 5)    # True

# BLOCK 5: logical operators
age = 25
has_id = True
print(age >= 18 and has_id)      # True
print(age < 18 or has_id)        # True
print(not has_id)                # False

# BLOCK 6: practical uses of % and //
n = 7
print("even" if n % 2 == 0 else "odd")
minutes = 135
print(minutes // 60, "hours", minutes % 60, "minutes")

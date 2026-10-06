"""Day 2 example: variables and data types.

Run:  python3 learning-path/examples/day02_variables.py
"""

# BLOCK 1: create variables
name = "Ram"
age = 38
height_m = 1.75
is_engineer = True

# BLOCK 2: use variables
print(name, age, height_m, is_engineer)

# BLOCK 3: inspect types
print(type(name))
print(type(age))
print(type(height_m))
print(type(is_engineer))

# BLOCK 4: variables can change (re-assignment)
age = age + 1
print("Next year:", age)

# BLOCK 5: type conversion
text_number = "10"
real_number = int(text_number)
print(real_number + 5)       # 15
print(text_number + "5")     # "105" (string joining!)

# BLOCK 6: copying a value between variables
a = 5
b = a
a = 99
print(a, b)                  # 99 5 (b kept the old value)

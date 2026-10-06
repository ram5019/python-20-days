"""Day 14 example: functions.

Run:  python3 learning-path/examples/day14_functions.py
"""

# BLOCK 1: define and call
def greet():
    print("Hello from a function!")

greet()
greet()                              # reuse: call it again

# BLOCK 2: parameters (inputs)
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Ram")
greet_person("Sita")

# BLOCK 3: return (output)
def add(a, b):
    return a + b

result = add(3, 4)
print(result)                        # 7
print(add(add(1, 2), 3))             # 6 (functions can be nested in calls)

# BLOCK 4: print vs return
def show_square(n):
    print(n * n)                     # shows it, but gives back None

def get_square(n):
    return n * n                     # gives the value back

x = show_square(4)                   # prints 16
y = get_square(4)                    # prints nothing
print(x, y)                          # None 16

# BLOCK 5: default and keyword arguments
def power(base, exp=2):
    return base ** exp

print(power(5))                      # 25
print(power(2, 10))                  # 1024
print(power(exp=3, base=2))          # 8

# BLOCK 6: scope (local vs global)
counter = 100                        # global

def change_local():
    counter = 1                      # NEW local variable
    return counter

print(change_local())                # 1
print(counter)                       # 100 (unchanged)

# BLOCK 7: functions with lists / docstrings
def average(numbers):
    """Return the average of a list of numbers, or 0 if empty."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

print(average([70, 80, 90]))         # 80.0
print(average([]))                   # 0

# BLOCK 8: one function calling another
def is_even(n):
    return n % 2 == 0

def count_evens(numbers):
    count = 0
    for n in numbers:
        if is_even(n):
            count += 1
    return count

print(count_evens([1, 2, 3, 4, 6]))  # 3

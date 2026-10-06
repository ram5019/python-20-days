"""Day 16 example: errors and exceptions.

Run:  python3 learning-path/examples/day16_errors.py
"""

# BLOCK 1: what an uncaught error looks like (left commented out on purpose)
# print(10 / 0)        # ZeroDivisionError: crashes the program

# BLOCK 2: try / except
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")
print("Program continues")

# BLOCK 3: catching a specific error + using its message
try:
    number = int("abc")
except ValueError as e:
    print("Bad number:", e)

# BLOCK 4: multiple except blocks
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "cannot divide by zero"
    except TypeError:
        return "both values must be numbers"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("10", 2))

# BLOCK 5: else and finally
try:
    value = int("42")
except ValueError:
    print("not a number")
else:
    print("Converted OK:", value)        # runs only if NO error
finally:
    print("Always runs (cleanup)")

# BLOCK 6: robust input loop (fixes Day 4's crashing)
def ask_int(prompt):
    while True:
        text = input(prompt)
        try:
            return int(text)
        except ValueError:
            print("Please type a whole number.")

# BLOCK 7: safe file reading (fixes Day 15's missing file)
def read_file_safely(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None

content = read_file_safely("nope.txt")
print("File content:", content)

# BLOCK 8: raising your own errors
def set_age(age):
    if age < 0:
        raise ValueError("age cannot be negative")
    return age

try:
    set_age(-5)
except ValueError as e:
    print("Rejected:", e)

# Try it yourself:
# age = ask_int("Your age: ")
# print("Next year:", age + 1)

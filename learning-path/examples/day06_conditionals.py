"""Day 6 example: if / elif / else.

Run:  python3 learning-path/examples/day06_conditionals.py
"""

# BLOCK 1: simple if
temperature = 35
if temperature > 30:
    print("It's hot")

# BLOCK 2: if / else
age = 16
if age >= 18:
    print("Adult")
else:
    print("Minor")

# BLOCK 3: if / elif / else (grading)
marks = 72
if marks >= 90:
    grade = "A"
elif marks >= 75:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "F"
print("Grade:", grade)

# BLOCK 4: combining conditions
has_ticket = True
age = 20
if has_ticket and age >= 18:
    print("Entry allowed")
else:
    print("Entry denied")

# BLOCK 5: nested if
user = "admin"
password = "1234"
if user == "admin":
    if password == "1234":
        print("Welcome, admin")
    else:
        print("Wrong password")
else:
    print("Unknown user")

# BLOCK 6: truthiness and one-line if
name = ""
if not name:
    print("Name is empty")
label = "even" if 10 % 2 == 0 else "odd"
print(label)

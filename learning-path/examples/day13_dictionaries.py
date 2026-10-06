"""Day 13 example: dictionaries.

Run:  python3 learning-path/examples/day13_dictionaries.py
"""

# BLOCK 1: create and read
student = {"name": "Asha", "marks": 88, "city": "Chennai"}
print(student["name"])
print(student.get("age", "unknown"))     # safe lookup with a default

# BLOCK 2: add / update / delete
student["marks"] = 92                    # update
student["grade"] = "A"                   # add new key
del student["city"]                      # delete
print(student)

# BLOCK 3: check for a key
print("name" in student)                 # True
print("city" in student)                 # False

# BLOCK 4: loop over a dict
for key in student:
    print(key, "->", student[key])

for key, value in student.items():       # keys and values together
    print(f"{key}: {value}")

print(list(student.keys()))
print(list(student.values()))

# BLOCK 5: counting with a dict (word frequency)
text = "to be or not to be"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
print(counts)                            # {'to': 2, 'be': 2, 'or': 1, 'not': 1}

# BLOCK 6: list of dicts (like a table)
students = [
    {"name": "Asha", "marks": 88},
    {"name": "Ravi", "marks": 72},
    {"name": "Meena", "marks": 95},
]
for s in students:
    print(s["name"], s["marks"])
top = max(students, key=lambda s: s["marks"])
print("Topper:", top["name"])

# BLOCK 7: dict of lists (grouping)
groups = {"even": [], "odd": []}
for n in range(1, 8):
    key = "even" if n % 2 == 0 else "odd"
    groups[key].append(n)
print(groups)

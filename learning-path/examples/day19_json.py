"""Day 19 example: JSON.

Run:  python3 learning-path/examples/day19_json.py
(Creates and removes a small 'demo_data.json' next to this script.)
"""

import json
from pathlib import Path

FILE = Path(__file__).parent / "demo_data.json"

# BLOCK 1: Python dict -> JSON text (serialise)
data = {
    "name": "Ravi",
    "age": 30,
    "active": True,
    "manager": None,
    "skills": ["Python", "SQL"],
}
text = json.dumps(data, indent=2)
print(text)
print(type(text))                         # <class 'str'>

# BLOCK 2: JSON text -> Python dict (parse)
parsed = json.loads(text)
print(type(parsed))                       # <class 'dict'>
print("Skills:", parsed["skills"])
print(parsed == data)                     # True: round trip is lossless

# BLOCK 3: how Python types map to JSON
print(json.dumps([True, False, None, 1.5, "x"]))
# [true, false, null, 1.5, "x"]

# BLOCK 4: save to a file
with open(FILE, "w") as f:
    json.dump(data, f, indent=2)          # dump (no s) writes to a file

# BLOCK 5: load from a file
with open(FILE) as f:
    loaded = json.load(f)                 # load (no s) reads from a file
print("Loaded name:", loaded["name"])

# BLOCK 6: list of records (like a tiny database)
students = [
    {"name": "Asha", "marks": 88},
    {"name": "Meena", "marks": 95},
]
with open(FILE, "w") as f:
    json.dump(students, f, indent=2)

with open(FILE) as f:
    students = json.load(f)
students.append({"name": "Ravi", "marks": 72})
with open(FILE, "w") as f:
    json.dump(students, f, indent=2)
print(len(students), "students saved")

# BLOCK 7: safe loading (Day 16 + Day 19)
def load_records(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return []                         # first run: no file yet
    except json.JSONDecodeError:
        print("File is corrupted, starting empty")
        return []

print(load_records(FILE))
print(load_records(Path(__file__).parent / "missing.json"))   # []

# BLOCK 8: what JSON cannot store (and the fix)
from datetime import date
try:
    json.dumps({"today": date.today()})
except TypeError as e:
    print("Cannot serialise:", e)
print(json.dumps({"today": str(date.today())}))   # convert to str first

# clean up
FILE.unlink()

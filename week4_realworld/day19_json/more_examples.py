"""Day 19: JSON. 10 examples, simple to complex.

Run:  python3 week4_realworld/day19_json/more_examples.py

Files are created in a temporary folder that is deleted at the end.
"""

import json
import tempfile
from datetime import date
from pathlib import Path

TMP = tempfile.TemporaryDirectory()
BASE = Path(TMP.name)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Python dict -> JSON text (dumps)")
# WHAT: turn data into a string.
# HOW : json.dumps(obj). The result is text, not a dict any more.
# WHY : text can be saved, sent over a network, logged.
person = {"name": "Asha", "age": 28, "skills": ["Python", "SQL"]}
text = json.dumps(person)
print(text)
print(type(text).__name__)

# ---------------------------------------------------------------
show(2, "JSON text -> Python (loads)")
# WHAT: turn text back into data.
# HOW : json.loads(text). Remember: the "s" means "string".
# WHY : the reverse trip; a lossless round trip.
back = json.loads(text)
print(back["skills"][0], type(back).__name__)
print("round trip equal:", back == person)

# ---------------------------------------------------------------
show(3, "How Python types map to JSON")
# WHAT: True/None/tuple become JSON equivalents.
# HOW : True->true, False->false, None->null, tuple->array.
# WHY : you will see "null" and "true" in every API response.
print(json.dumps([True, False, None, 1.5, "x", (1, 2)]))
print(json.loads('{"ok": true, "value": null}'))

# ---------------------------------------------------------------
show(4, "Pretty printing and sorted keys")
# WHAT: human-readable output.
# HOW : indent=2 adds line breaks; sort_keys=True orders the keys;
#       ensure_ascii=False keeps accents readable.
# WHY : config files and debugging need readable JSON.
data = {"b": 2, "a": 1, "city": "Zürich", "nested": {"k": [1, 2]}}
print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))

# ---------------------------------------------------------------
show(5, "Save to a file and load it back")
# WHAT: persist data between runs.
# HOW : json.dump(obj, file) and json.load(file) (no "s": they use files).
# WHY : the simplest "database" for small programs.
path = BASE / "person.json"
with open(path, "w") as f:
    json.dump(person, f, indent=2)
with open(path) as f:
    loaded = json.load(f)
print("loaded:", loaded["name"], "| file size:", path.stat().st_size, "bytes")

# ---------------------------------------------------------------
show(6, "Navigate nested JSON, like an API response")
# WHAT: dig into dicts and lists.
# HOW : chain keys and indexes; use .get() for optional fields.
# WHY : every web API returns nested JSON.
response = json.loads("""
{
  "status": "ok",
  "data": {
    "user": {"id": 7, "name": "Sam", "roles": ["admin", "dev"]},
    "servers": [
      {"name": "web01", "cpu": 35},
      {"name": "db01", "cpu": 91}
    ]
  }
}
""")
print(response["data"]["user"]["name"])
print(response["data"]["user"]["roles"][-1])
print([s["name"] for s in response["data"]["servers"] if s["cpu"] > 80])
print(response["data"]["user"].get("email", "no email"))

# ---------------------------------------------------------------
show(7, "Load -> change -> save")
# WHAT: the update cycle of every small data app.
# HOW : read the list, modify it in memory, write the whole list back.
# WHY : the pattern behind your Day 20 project.
students_file = BASE / "students.json"
students_file.write_text(json.dumps([{"name": "Asha", "marks": 88}]))
students = json.loads(students_file.read_text())
students.append({"name": "Ravi", "marks": 72})
students[0]["marks"] += 5
students_file.write_text(json.dumps(students, indent=2))
print(json.loads(students_file.read_text()))

# ---------------------------------------------------------------
show(8, "Safe loading: missing and corrupted files")
# WHAT: a loader that always returns usable data.
# HOW : catch FileNotFoundError (first run) and JSONDecodeError (damaged file).
# WHY : programs must start even when the data file is absent or broken.
def load_records(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        print("  corrupted file:", error.msg)
        return []


bad = BASE / "bad.json"
bad.write_text("{'single': 'quotes'}")          # invalid JSON
print(load_records(BASE / "nothing.json"))
print(load_records(bad))
print(load_records(students_file)[0])

# ---------------------------------------------------------------
show(9, "What JSON cannot store, and how to cope")
# WHAT: dates, sets and your own objects are not JSON types.
# HOW : convert to basic types first, or pass default= to dumps.
# WHY : a very common TypeError when saving real data.
try:
    json.dumps({"day": date(2026, 10, 13)})
except TypeError as error:
    print("Error:", error)


def to_jsonable(value):
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(f"cannot serialise {type(value).__name__}")


mixed = {"day": date(2026, 10, 13), "tags": {"b", "a"}}
print(json.dumps(mixed, default=to_jsonable))


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


pt = Point(1, 2)
print(json.dumps(pt.__dict__))                  # object -> dict -> JSON

# ---------------------------------------------------------------
show(10, "Mini program: a contacts book saved as JSON")
# WHAT: add, search, update and delete, with persistence.
# HOW : every change loads, modifies and saves; search is a list filter.
# WHY : a complete data app in about 40 lines.
CONTACTS = BASE / "contacts.json"


def load():
    return load_records(CONTACTS)


def save(contacts):
    CONTACTS.write_text(json.dumps(contacts, indent=2))


def add(name, phone):
    contacts = load()
    if any(c["name"].lower() == name.lower() for c in contacts):
        print(f"  {name} already exists")
        return
    contacts.append({"name": name, "phone": phone})
    save(contacts)


def search(text):
    return [c for c in load() if text.lower() in c["name"].lower()]


def remove(name):
    contacts = [c for c in load() if c["name"].lower() != name.lower()]
    save(contacts)


add("Asha Rao", "555-0101")
add("Ravi Kumar", "555-0102")
add("asha rao", "555-9999")
print("search 'rav':", search("rav"))
remove("Asha Rao")
print("remaining:", [c["name"] for c in load()])

TMP.cleanup()
print("\n(temporary files deleted)")

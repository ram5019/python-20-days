"""Day 20: Final project (student manager). 10 examples, simple to complex.

Run:  python3 week4_realworld/day20_project_student_manager/more_examples.py

The examples build the project up layer by layer. Example 10 is the finished
program, rewritten as a class. Files go to a temporary folder that is deleted
at the end.
"""

import csv
import json
import tempfile
from pathlib import Path

TMP = tempfile.TemporaryDirectory()
BASE = Path(TMP.name)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "The data shape: a list of dictionaries")
# WHAT: how the whole program stores its data.
# HOW : one dict per student, all kept in one list.
# WHY : every layer below works on this same shape.
students = [
    {"name": "Asha", "marks": 88.0},
    {"name": "Ravi", "marks": 72.0},
]
print(students)

# ---------------------------------------------------------------
show(2, "Adding a student, with validation")
# WHAT: refuse bad names and bad marks; refuse duplicates.
# HOW : return (ok, message) so the caller can show the reason.
# WHY : keep the rules in ONE function.
def add_student(students, name, marks):
    name = name.strip().title()
    if not name:
        return False, "name cannot be empty"
    if not 0 <= marks <= 100:
        return False, "marks must be between 0 and 100"
    if any(s["name"] == name for s in students):
        return False, f"{name} already exists"
    students.append({"name": name, "marks": float(marks)})
    return True, f"added {name}"


for attempt in [("meena", 95), ("", 50), ("Ravi", 60), ("John", 120)]:
    print(attempt, "->", add_student(students, *attempt))

# ---------------------------------------------------------------
show(3, "Finding a student (case-insensitive)")
# WHAT: look up by name however it was typed.
# HOW : compare lowercase versions; return the dict itself or None.
# WHY : update and delete both start with a find.
def find_student(students, name):
    for s in students:
        if s["name"].lower() == name.strip().lower():
            return s
    return None


print(find_student(students, "  ASHA "))
print(find_student(students, "nobody"))

# ---------------------------------------------------------------
show(4, "Updating and deleting")
# WHAT: change or remove a record.
# HOW : find first. The returned dict IS the one in the list, so editing it
#       edits the list. Delete by removing that dict.
# WHY : shared references (Day 10) are what make this so short.
def update_marks(students, name, marks):
    s = find_student(students, name)
    if s is None:
        return False
    s["marks"] = float(marks)
    return True


def delete_student(students, name):
    s = find_student(students, name)
    if s is None:
        return False
    students.remove(s)
    return True


print(update_marks(students, "ravi", 79), delete_student(students, "john"))
print(students)

# ---------------------------------------------------------------
show(5, "Statistics: pure functions, data in, data out")
# WHAT: average, topper, pass rate.
# HOW : no input() or print() inside; guard the empty list.
# WHY : pure functions are easy to reuse and test.
def average(students):
    return sum(s["marks"] for s in students) / len(students) if students else 0


def topper(students):
    return max(students, key=lambda s: s["marks"]) if students else None


def pass_rate(students, pass_mark=50):
    if not students:
        return 0
    return sum(s["marks"] >= pass_mark for s in students) / len(students)


print(f"average {average(students):.1f} | topper {topper(students)['name']} "
      f"| pass rate {pass_rate(students):.0%}")

# ---------------------------------------------------------------
show(6, "Grades and a formatted report")
# WHAT: turn numbers into a tidy table.
# HOW : an elif chain gives the grade; f-string alignment draws the columns.
# WHY : presentation is a separate job from calculation.
def grade_for(marks):
    if marks >= 90:
        return "A"
    if marks >= 75:
        return "B"
    if marks >= 60:
        return "C"
    return "F"


def report(students):
    lines = [f"{'Name':<10}{'Marks':>7}  Grade", "-" * 25]
    for s in sorted(students, key=lambda s: s["name"]):
        lines.append(f"{s['name']:<10}{s['marks']:>7.1f}  {grade_for(s['marks'])}")
    return "\n".join(lines)


print(report(students))

# ---------------------------------------------------------------
show(7, "Persistence: load and save with JSON")
# WHAT: keep the data between runs.
# HOW : the only two functions that touch the disk.
# WHY : isolating storage means you could swap JSON for a database later.
DATA = BASE / "students.json"


def save_students(students):
    DATA.write_text(json.dumps(students, indent=2))


def load_students():
    try:
        return json.loads(DATA.read_text())
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("  data file corrupted, starting empty")
        return []


print("first run:", load_students())
save_students(students)
print("after save:", [s["name"] for s in load_students()])

# ---------------------------------------------------------------
show(8, "Surviving a corrupted data file")
# WHAT: the program must still start.
# HOW : load_students already catches JSONDecodeError; prove it.
# WHY : files get damaged by crashes, editing and disk problems.
DATA.write_text("{ this is not json")
print("loaded:", load_students())
save_students(students)                          # restore good data

# ---------------------------------------------------------------
show(9, "The menu loop, driven by scripted choices")
# WHAT: connect everything to a menu.
# HOW : while True + if/elif; `choices` replaces the user's typing.
# WHY : this is the main() of the finished program.
def run_menu(students, choices):
    for choice in choices:
        print(f"> {choice}")
        if choice == "1":
            print(" ", add_student(students, "Li", 66)[1])
            save_students(students)
        elif choice == "2":
            print(report(students))
        elif choice == "3":
            print(f"  average {average(students):.1f}, topper {topper(students)['name']}")
        elif choice == "4":
            print("  Goodbye!")
            break
        else:
            print("  Invalid option.")


run_menu(load_students(), ["1", "9", "2", "3", "4"])

# ---------------------------------------------------------------
show(10, "The finished program, refactored into a class + CSV export")
# WHAT: the same features, organised as one class.
# HOW : the class keeps the list and the file path together; methods replace
#       the free functions; export_csv is a new feature.
# WHY : shows how a working function-based program can grow into classes.
class StudentManager:
    def __init__(self, path):
        self.path = Path(path)
        self.students = self._load()

    def _load(self):
        try:
            return json.loads(self.path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self):
        self.path.write_text(json.dumps(self.students, indent=2))

    def add(self, name, marks):
        ok, message = add_student(self.students, name, marks)
        if ok:
            self._save()
        return message

    def update(self, name, marks):
        done = update_marks(self.students, name, marks)
        if done:
            self._save()
        return done

    def delete(self, name):
        done = delete_student(self.students, name)
        if done:
            self._save()
        return done

    def export_csv(self, csv_path):
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "marks", "grade"])
            writer.writeheader()
            for s in self.students:
                writer.writerow({**s, "grade": grade_for(s["marks"])})

    def summary(self):
        best = topper(self.students)
        return (f"{len(self.students)} students, average {average(self.students):.1f}, "
                f"topper {best['name'] if best else '-'}")


manager = StudentManager(BASE / "class_students.json")
print(manager.add("Asha", 88))
print(manager.add("Ravi", 72))
print(manager.add("Ravi", 10))
manager.update("ravi", 81)
manager.delete("nobody")
print(manager.summary())
manager.export_csv(BASE / "students.csv")
print((BASE / "students.csv").read_text())
print("a new manager reloads the same data:", StudentManager(BASE / "class_students.json").summary())

TMP.cleanup()
print("(temporary files deleted)")

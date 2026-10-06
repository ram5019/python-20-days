"""Day 20 example: Student Record Manager (final project).

Combines: functions, lists, dicts, loops, conditionals, files, JSON,
error handling, and the __name__ guard.

Run:  python3 learning-path/examples/day20_student_manager.py
Data is stored in 'students_demo.json' next to this script.
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "students_demo.json"


# ---------- LAYER 1: storage (files + JSON + error handling) ----------
def load_students():
    """Return the list of students from disk, or [] if none/corrupt."""
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting with an empty list.")
        return []


def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)


# ---------- LAYER 2: input helpers (validation loops) ----------
def ask_name():
    while True:
        name = input("Name: ").strip().title()
        if name:
            return name
        print("Name cannot be empty.")


def ask_marks():
    while True:
        try:
            marks = float(input("Marks (0-100): "))
        except ValueError:
            print("Please type a number.")
            continue
        if 0 <= marks <= 100:
            return marks
        print("Marks must be between 0 and 100.")


# ---------- LAYER 3: logic (pure functions: data in, data out) ----------
def find_student(students, name):
    for s in students:
        if s["name"].lower() == name.lower():
            return s
    return None


def average_marks(students):
    if not students:
        return 0
    return sum(s["marks"] for s in students) / len(students)


def topper(students):
    if not students:
        return None
    return max(students, key=lambda s: s["marks"])


def grade_for(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    return "F"


# ---------- LAYER 4: actions (connect input, logic, storage, output) ----------
def add_student(students):
    name = ask_name()
    if find_student(students, name):
        print(f"{name} already exists. Use Update instead.")
        return
    students.append({"name": name, "marks": ask_marks()})
    save_students(students)
    print("Added.")


def update_student(students):
    name = ask_name()
    student = find_student(students, name)
    if student is None:
        print("Student not found.")
        return
    student["marks"] = ask_marks()
    save_students(students)
    print("Updated.")


def delete_student(students):
    name = ask_name()
    student = find_student(students, name)
    if student is None:
        print("Student not found.")
        return
    students.remove(student)
    save_students(students)
    print("Deleted.")


def show_all(students):
    if not students:
        print("No records.")
        return
    print(f"\n{'Name':<15}{'Marks':>8}  Grade")
    print("-" * 31)
    for s in sorted(students, key=lambda s: s["name"]):
        print(f"{s['name']:<15}{s['marks']:>8.1f}  {grade_for(s['marks'])}")


def show_stats(students):
    best = topper(students)
    if best is None:
        print("No records.")
        return
    print(f"Students : {len(students)}")
    print(f"Average  : {average_marks(students):.1f}")
    print(f"Topper   : {best['name']} ({best['marks']})")


# ---------- LAYER 5: the menu loop ----------
MENU = """
1. Add student
2. Update marks
3. Delete student
4. Show all
5. Statistics
6. Exit
"""

def main():
    students = load_students()          # load ONCE at start
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            update_student(students)
        elif choice == "3":
            delete_student(students)
        elif choice == "4":
            show_all(students)
        elif choice == "5":
            show_stats(students)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

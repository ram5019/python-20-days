"""Day 20 — Final Mini Project: Student Record Manager."""

import json
import os

FILE = "students.json"
students = json.load(open(FILE)) if os.path.exists(FILE) else []

def save():
    json.dump(students, open(FILE, "w"), indent=2)

def add_student():
    students.append({
        "name":  input("Name: "),
        "marks": float(input("Marks: ")),
    })
    save()
    print("Added")

def show_all():
    if not students:
        print("No records")
        return
    for s in students:
        print(f"{s['name']} -> {s['marks']}")

def topper():
    if students:
        top = max(students, key=lambda x: x["marks"])
        print("Topper:", top["name"], top["marks"])
    else:
        print("No records")

def main():
    while True:
        print("\n1.Add  2.Show  3.Topper  4.Exit")
        ch = input("Choose: ").strip()
        if ch == "1":
            add_student()
        elif ch == "2":
            show_all()
        elif ch == "3":
            topper()
        elif ch == "4":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
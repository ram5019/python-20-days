"""Day 18 — OOP Basics.
Task: Create a Student class with grade().
"""

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def grade(self):
        if self.marks >= 90:
            return "A"
        elif self.marks >= 60:
            return "B"
        return "C"

def main():
    s = Student("Ravi", 85)
    print(s.name, "->", s.grade())

if __name__ == "__main__":
    main()
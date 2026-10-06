"""Day 7 — Mini Project: Age Calculator."""

from datetime import datetime

def main():
    year = int(input("Birth year: "))
    age = datetime.now().year - year
    print(f"You are {age} years old.")

if __name__ == "__main__":
    main()
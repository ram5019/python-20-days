"""Day 6 — Conditionals.
Task: Check positive / negative / zero.
"""

def main():
    n = float(input("Enter a number: "))
    if n > 0:
        print("Positive")
    elif n < 0:
        print("Negative")
    else:
        print("Zero")

if __name__ == "__main__":
    main()
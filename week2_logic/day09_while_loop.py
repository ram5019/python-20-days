"""Day 9 — while Loop.
Task: Password retry loop.
"""

def main():
    while input("Password: ") != "python123":
        print("Wrong, try again")
    print("Access granted")

if __name__ == "__main__":
    main()
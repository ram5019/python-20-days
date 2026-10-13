"""Day 16 — Error Handling.
Task: Wrap calculator in try/except.
"""

def main():
    try:
        a = float(input("A: "))
        b = float(input("B: "))
        print(a / b)
    except ValueError:
        print("Enter numbers only")
    except ZeroDivisionError:
        print("Cannot divide by zero")
    finally:
        print("Done.")

if __name__ == "__main__":
    main()
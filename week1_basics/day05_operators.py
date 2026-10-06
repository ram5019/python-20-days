"""Day 5 — Operators.
Task: Build a simple calculator.
"""

def main():
    a = float(input("A: "))
    b = float(input("B: "))
    op = input("Operator (+ - * /): ")

    if op == "+":
        print(a + b)
    elif op == "-":
        print(a - b)
    elif op == "*":
        print(a * b)
    elif op == "/":
        print(a / b if b != 0 else "Cannot divide by zero")
    else:
        print("Unknown operator")

if __name__ == "__main__":
    main()
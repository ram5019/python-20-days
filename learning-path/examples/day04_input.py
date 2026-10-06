"""Day 4 example: input() and conversion.

Run:  python3 learning-path/examples/day04_input.py
"""

# BLOCK 1: ask for text
name = input("What is your name? ")
print("Hello,", name)

# BLOCK 2: input is ALWAYS a string
age_text = input("How old are you? ")
print(type(age_text))              # <class 'str'>

# BLOCK 3: convert to a number
age = int(age_text)
print("Next year you will be", age + 1)

# BLOCK 4: shorter: convert immediately
height = float(input("Height in metres? "))
print(f"Height in cm: {height * 100}")

# BLOCK 5: cleaning input
city = input("City? ").strip().title()
print(f"Welcome from {city}!")

# BLOCK 6: input -> process -> output
price = float(input("Price of one item: "))
qty = int(input("Quantity: "))
total = price * qty
print(f"Total: {total:.2f}")       # 2 decimal places

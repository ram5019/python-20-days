"""Day 2: Variables and data types. 10 examples, simple to complex.

Run:  python3 week1_basics/day02_variables_types/more_examples.py

WHAT / HOW / WHY notes explain each example.
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Create and use a variable")
# WHAT: store a value under a name, then use the name.
# HOW : name = value. The single = means "store", not "equals".
# WHY : variables let you reuse a value without retyping it.
city = "Paris"
print(city)
print("I live in", city)

# ---------------------------------------------------------------
show(2, "The four basic types, checked with type()")
# WHAT: see what kind of value each variable holds.
# HOW : Python decides the type from the value you assign.
# WHY : the type decides what you can do with a value (add numbers, join text...).
name = "Sam"            # str
age = 30                # int
height_m = 1.78         # float
is_student = False      # bool
for value in (name, age, height_m, is_student):
    print(value, "->", type(value).__name__)

# ---------------------------------------------------------------
show(3, "Changing a variable (re-assignment)")
# WHAT: give a name a new value; update it using its old value.
# HOW : the right side runs first, then the result is stored back.
# WHY : counters and running totals use exactly this pattern.
score = 10
score = score + 5
print("score is", score)
score = score * 2
print("score is", score)

# ---------------------------------------------------------------
show(4, "Good names versus bad names")
# WHAT: the same calculation written two ways.
# HOW : snake_case, descriptive names. Names cannot start with a digit
#       or contain spaces.
# WHY : you read code far more often than you write it.
x = 3
y = 4.5
z = x * y                                   # what are x, y, z?
items_in_cart = 3
price_per_item = 4.5
total_price = items_in_cart * price_per_item  # now it explains itself
print(z, total_price)

# ---------------------------------------------------------------
show(5, "Assign several at once, and swap two values")
# WHAT: two shortcuts Python gives you.
# HOW : a, b = 1, 2 creates two variables. a, b = b, a swaps them
#       without a temporary variable.
# WHY : swapping and unpacking appear again with tuples (Day 12).
a, b = 1, 2
print("before:", a, b)
a, b = b, a
print("after :", a, b)

# ---------------------------------------------------------------
show(6, "Converting between types")
# WHAT: turn text into numbers and numbers into text.
# HOW : int(), float(), str(). Conversion makes a NEW value.
# WHY : input from users and files always arrives as text (Day 4, Day 15).
text_number = "42"
real_number = int(text_number)
print(real_number + 8)            # 50  (maths)
print(text_number + "8")          # 428 (joining text)
print(float("3.5") * 2)           # 7.0
print("Count: " + str(7))         # numbers must become text to be joined

# ---------------------------------------------------------------
show(7, "int versus float arithmetic")
# WHAT: how Python mixes whole numbers and decimals.
# HOW : / always gives a float; mixing int and float gives a float.
#       int() cuts off the decimals (it does not round).
# WHY : unexpected floats are a common surprise; know where they come from.
print(10 / 2)                     # 5.0
print(7 // 2)                     # 3   (whole-number division)
print(3 + 0.5)                    # 3.5
print(int(3.99))                  # 3
print(round(3.99))                # 4

# ---------------------------------------------------------------
show(8, "Constants and f-strings")
# WHAT: a value that should never change, used in a message.
# HOW : UPPER_CASE is a convention for constants. f"..." inserts values.
# WHY : one named constant means one place to change it later.
TAX_RATE = 0.18
price = 200
tax = price * TAX_RATE
print(f"Price {price}, tax {tax}, total {price + tax}")

# ---------------------------------------------------------------
show(9, "Copying a number: variables are independent")
# WHAT: change one variable after copying it; the other stays.
# HOW : b = a copies the VALUE for simple types (numbers, text, booleans).
# WHY : lists behave differently (Day 10); knowing this case first helps.
a = 5
b = a
a = 99
print("a =", a, "| b =", b)

# ---------------------------------------------------------------
show(10, "Mini program: an invoice calculator")
# WHAT: combine variables, types, conversion and f-strings.
# HOW : quantities arrive as text (as if typed by a user), get converted,
#       then used in arithmetic.
# WHY : this is the input -> process -> output pattern of every program.
quantity_text = "3"
unit_price_text = "499.99"
quantity = int(quantity_text)
unit_price = float(unit_price_text)
subtotal = quantity * unit_price
tax = subtotal * TAX_RATE
total = subtotal + tax
print(f"{quantity} x {unit_price} = {subtotal:.2f}")
print(f"Tax ({TAX_RATE:.0%}): {tax:.2f}")
print(f"Total: {total:.2f}")

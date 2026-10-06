"""Day 9 example: while loops.

Run:  python3 learning-path/examples/day09_while_loop.py
"""

# BLOCK 1: basic while with a counter
count = 1
while count <= 5:
    print("Count:", count)
    count += 1                 # without this: infinite loop!

# BLOCK 2: countdown
n = 3
while n > 0:
    print(n)
    n -= 1
print("Liftoff!")

# BLOCK 3: repeat until valid input
while True:
    answer = input("Enter a number between 1 and 10: ")
    if answer.isdigit() and 1 <= int(answer) <= 10:
        print("Thanks!")
        break
    print("Invalid, try again.")

# BLOCK 4: sentinel value (stop word)
total = 0
while True:
    text = input("Add a number (or 'done'): ")
    if text == "done":
        break
    total += int(text)
print("Total:", total)

# BLOCK 5: guessing game
secret = 7
tries = 0
while True:
    guess = int(input("Guess the number: "))
    tries += 1
    if guess == secret:
        print(f"Correct in {tries} tries!")
        break
    elif guess < secret:
        print("Too low")
    else:
        print("Too high")

# BLOCK 6: while / else (runs if loop ended without break)
attempts = 0
while attempts < 3:
    attempts += 1
else:
    print("Loop finished normally")

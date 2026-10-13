"""Day 9: while loops. 10 examples, simple to complex.

Run:  python3 week2_logic/day09_while_loop/more_examples.py

Where a loop would normally wait for typing, the example uses a pre-written
list of answers (see 'answers' variables) so the file runs by itself.
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "The three parts of a while loop")
# WHAT: count from 1 to 5.
# HOW : SETUP (count = 1), CONDITION (count <= 5), UPDATE (count += 1).
#       Forget the update and the loop never ends.
# WHY : every while loop has these three parts.
count = 1
while count <= 5:
    print("Count:", count)
    count += 1

# ---------------------------------------------------------------
show(2, "Counting down")
# WHAT: the update can go in any direction.
# HOW : n -= 1 moves toward the stopping condition.
# WHY : countdowns, retries remaining, timers.
n = 3
while n > 0:
    print(n)
    n -= 1
print("Liftoff!")

# ---------------------------------------------------------------
show(3, "Loop until a running total passes a limit")
# WHAT: you do not know in advance how many rounds are needed.
# HOW : keep adding until the total reaches 100.
# WHY : this is the situation where while beats for.
total, step, rounds = 0, 7, 0
while total < 100:
    total += step
    step += 3
    rounds += 1
print(f"Reached {total} after {rounds} rounds")

# ---------------------------------------------------------------
show(4, "while True + break: wait for a valid answer")
# WHAT: keep asking until the answer is acceptable.
# HOW : `while True` loops forever; `break` is the planned exit.
#       'answers' pretends to be what the user types.
# WHY : input validation (fixes Day 4's crashing problem).
answers = iter(["abc", "42", "7"])
while True:
    text = next(answers)
    print("User typed:", text)
    if text.isdigit() and 1 <= int(text) <= 10:
        print("Accepted:", text)
        break
    print("Invalid, try again.")

# ---------------------------------------------------------------
show(5, "Sentinel value: stop when the user says 'done'")
# WHAT: add numbers until a special stop word.
# HOW : test for the stop word BEFORE converting to int.
# WHY : lets the user enter 3 items or 300.
answers = iter(["10", "20", "5", "done"])
total = 0
while True:
    text = next(answers)
    if text == "done":
        break
    total += int(text)
print("Total:", total)

# ---------------------------------------------------------------
show(6, "Guessing game with hints")
# WHAT: a complete little game.
# HOW : loop, compare, give a hint, count tries. The guesses are scripted.
# WHY : combines input, conditions and a counter inside a loop.
secret = 37
guesses = iter([50, 25, 40, 37])
tries = 0
while True:
    guess = next(guesses)
    tries += 1
    if guess == secret:
        print(f"{guess}: correct in {tries} tries!")
        break
    elif guess < secret:
        print(f"{guess}: too low")
    else:
        print(f"{guess}: too high")

# ---------------------------------------------------------------
show(7, "The Collatz sequence")
# WHAT: halve if even, else 3n+1, until you reach 1.
# HOW : the number of rounds depends on the data; only while fits.
# WHY : a famous example where nobody can predict the loop length.
n = 27
steps = 0
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps += 1
print("27 reaches 1 after", steps, "steps")

# ---------------------------------------------------------------
show(8, "Limited retries")
# WHAT: allow at most 3 login attempts.
# HOW : the condition has two parts: attempts left AND not yet successful.
# WHY : retry logic for passwords, networks and files.
attempts_left = 3
logged_in = False
tries_typed = iter(["wrong1", "wrong2", "secret123"])
while attempts_left > 0 and not logged_in:
    password = next(tries_typed)
    if password == "secret123":
        logged_in = True
        print("Logged in")
    else:
        attempts_left -= 1
        print(f"Wrong password, {attempts_left} attempts left")
if not logged_in:
    print("Account locked")

# ---------------------------------------------------------------
show(9, "Digits with % and //")
# WHAT: reverse a number and count its digits.
# HOW : n % 10 is the last digit; n // 10 drops it.
# WHY : a pure-arithmetic loop; the pattern appears in many puzzles.
number = 12345
reversed_number, digits = 0, 0
while number > 0:
    last = number % 10
    reversed_number = reversed_number * 10 + last
    number //= 10
    digits += 1
print("Reversed:", reversed_number, "| digits:", digits)

# ---------------------------------------------------------------
show(10, "Mini program: a menu loop and a savings simulation")
# WHAT: two realistic loops.
# HOW : the menu repeats until 'quit'; the simulation loops until the
#       balance doubles.
# WHY : menu loops drive command-line tools; simulations answer "how long?".
choices = iter(["balance", "deposit", "balance", "quit"])
balance = 100
while True:
    choice = next(choices)
    print("> menu choice:", choice)
    if choice == "balance":
        print("  Balance:", balance)
    elif choice == "deposit":
        balance += 50
        print("  Deposited 50")
    elif choice == "quit":
        print("  Bye")
        break

money, years = 1000.0, 0
while money < 2000:
    money *= 1.07
    years += 1
print(f"1000 at 7% doubles after {years} years (to {money:.0f})")

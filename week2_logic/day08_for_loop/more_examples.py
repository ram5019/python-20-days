"""Day 8: for loops. 10 examples, simple to complex.

Run:  python3 week2_logic/day08_for_loop/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Repeat N times")
# WHAT: run a block 3 times.
# HOW : range(3) produces 0, 1, 2. The loop variable takes each value in turn.
# WHY : repetition without copy-paste is why programs exist.
for i in range(3):
    print("Round", i)

# ---------------------------------------------------------------
show(2, "range with start, stop and step")
# WHAT: control which numbers you get.
# HOW : range(start, stop, step). STOP IS EXCLUDED. A negative step counts down.
# WHY : counting up, down, or by twos covers most numeric loops.
print(list(range(1, 6)))            # 1..5
print(list(range(0, 20, 5)))        # 0, 5, 10, 15
print(list(range(5, 0, -1)))        # 5..1
for n in range(10, 0, -3):
    print(n, end=" ")
print()

# ---------------------------------------------------------------
show(3, "Loop over a string")
# WHAT: visit each character.
# HOW : any sequence works after "in"; no index needed.
# WHY : "loop over the thing itself" is the Pythonic style.
for ch in "WORD":
    print(ch)

# ---------------------------------------------------------------
show(4, "Loop over a list")
# WHAT: process every item.
# HOW : the loop variable holds the current item.
# WHY : lists (Day 10) and loops are the most common pairing in Python.
servers = ["web01", "web02", "db01"]
for server in servers:
    print("Checking", server)

# ---------------------------------------------------------------
show(5, "The accumulator pattern: build a total")
# WHAT: sum numbers and find the average.
# HOW : create the variable BEFORE the loop, update it INSIDE, use it AFTER.
# WHY : sums, counts and maximums all work this way.
marks = [72, 88, 95, 60]
total = 0
for m in marks:
    total += m
print("Total:", total, "| Average:", total / len(marks))
biggest = marks[0]
for m in marks:
    if m > biggest:
        biggest = m
print("Biggest:", biggest)

# ---------------------------------------------------------------
show(6, "Loop + if: filter while looping")
# WHAT: act only on items that match.
# HOW : an if inside the loop body decides per item.
# WHY : "for each item, if it matches, do something" is everywhere.
for n in range(1, 11):
    if n % 3 == 0:
        print(n, "is divisible by 3")

# ---------------------------------------------------------------
show(7, "enumerate and zip")
# WHAT: get the position with each item; walk two lists together.
# HOW : enumerate gives (index, item); zip pairs items by position.
# WHY : avoids manual counters and range(len(...)).
tasks = ["email", "review", "deploy"]
for number, task in enumerate(tasks, start=1):
    print(f"{number}. {task}")
names = ["Asha", "Ravi", "Meena"]
scores = [88, 72, 95]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# ---------------------------------------------------------------
show(8, "Nested loops: a multiplication table and a triangle")
# WHAT: a loop inside a loop.
# HOW : the inner loop runs completely for EVERY round of the outer loop.
# WHY : rows x columns problems (tables, grids, comparisons of all pairs).
for row in range(1, 4):
    for col in range(1, 5):
        print(f"{row * col:3}", end="")
    print()
for size in range(1, 5):
    print("*" * size)

# ---------------------------------------------------------------
show(9, "break, continue and loop-else")
# WHAT: control the loop from inside.
# HOW : continue skips to the next item; break stops the loop; the else
#       block runs only if the loop finished WITHOUT hitting break.
# WHY : searching ("stop when found") and skipping bad data.
for n in range(1, 10):
    if n == 3:
        continue                 # skip 3
    if n == 6:
        break                    # stop at 6
    print(n, end=" ")
print()
for name in ["Asha", "Ravi"]:
    if name == "Meena":
        print("found Meena")
        break
else:
    print("Meena not in the list")

# ---------------------------------------------------------------
show(10, "Mini program: primes, FizzBuzz and digit sum")
# WHAT: three classic exercises that combine everything so far.
# HOW : primes use a nested loop with for-else; FizzBuzz uses if/elif;
#       the digit sum uses a while-style loop over a string.
# WHY : these appear in interviews and teach loop thinking.
primes = []
for candidate in range(2, 30):
    for divisor in range(2, candidate):
        if candidate % divisor == 0:
            break
    else:
        primes.append(candidate)
print("Primes below 30:", primes)

for i in range(1, 16):
    if i % 15 == 0:
        print("FizzBuzz", end=" ")
    elif i % 3 == 0:
        print("Fizz", end=" ")
    elif i % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(i, end=" ")
print()

digit_sum = 0
for digit in str(98765):
    digit_sum += int(digit)
print("Digit sum of 98765:", digit_sum)

# Day 9: while Loops

**Time:** ~2 hours | **Example:** `examples/day09_while_loop.py` | **Your practice file:** `week2_logic/day09_while_loop.py`

---

## 1. The big idea

A `while` loop keeps repeating its body **as long as a condition is True**. It checks the condition before every round.

## 2. Why does this exist?

A `for` loop needs to know the sequence up front. But often you do not know how many rounds you need:

- "Keep asking until the user types a valid number."
- "Retry the connection until it works."
- "Keep reading until the file ends."

`while` handles **"until something happens"**; `for` handles **"for each of these"**.

## 3. Simple way to understand

A **kettle with a thermostat**. "While the water is below 100°C, keep heating." You do not count seconds. You watch the condition. When it becomes False, the loop stops.

Or **a guard at a door**: "While the person has no ticket, keep saying 'ticket please'."

The danger: if the condition **never** becomes False, the loop runs forever (an **infinite loop**). Press `Ctrl + C` to stop a stuck program.

## 4. How it works

```python
while condition:
    # body
    # something here must eventually make condition False
```

Each round:
1. Check the condition.
2. True → run the body, go back to 1.
3. False → skip the body, continue after the loop.

Every well-formed `while` loop has three parts:

| Part | Purpose | Example |
|------|---------|---------|
| **Setup** | create the thing being checked | `count = 1` |
| **Condition** | decides whether to go on | `count <= 5` |
| **Update** | moves toward finishing | `count += 1` |

Forget the update → infinite loop.

## 5. Code walkthrough, block by block

### Block 1: basic counter

```python
count = 1
while count <= 5:
    print("Count:", count)
    count += 1
```

**What it does:** this is the three-part structure in its purest form. Setup `count = 1`. Condition `count <= 5`. Update `count += 1` (Day 5). When `count` reaches 6 the condition is False and the loop ends. It does the same job as `for i in range(1, 6)`, which shows how closely the two loops are related.

### Block 2: countdown

```python
n = 3
while n > 0:
    print(n)
    n -= 1
print("Liftoff!")
```

**What it does:** counting down shows the update can go either way. Prints 3, 2, 1, then leaves the loop. `print("Liftoff!")` is unindented, so it runs once after the loop is done.

### Block 3: repeat until valid input

```python
while True:
    answer = input("Enter a number between 1 and 10: ")
    if answer.isdigit() and 1 <= int(answer) <= 10:
        print("Thanks!")
        break
    print("Invalid, try again.")
```

**What it does:** `while True:` means "loop forever", but the `break` is the **planned way out**.
- `answer.isdigit()` is a string method (Day 3) that checks it is all digits.
- `and` (Day 5) is **short-circuiting**: if `isdigit()` is False, the second half is not evaluated. This protects `int(answer)` from crashing on text.
- `1 <= int(answer) <= 10` is a chained comparison.
- Valid → `break` exits. Invalid → the `print` runs and the loop goes round again.

This is the most common real-world use of `while`: **input validation**. It fixes the problem you saw on Day 4 where bad input crashed the program.

### Block 4: sentinel value

```python
total = 0
while True:
    text = input("Add a number (or 'done'): ")
    if text == "done":
        break
    total += int(text)
print("Total:", total)
```

**What it does:** a **sentinel** is a special value that means "stop". It combines the Day 8 accumulator pattern with an open-ended loop: you can add 3 numbers or 300. The check for the sentinel happens **before** the conversion, so `int("done")` is never attempted.

### Block 5: guessing game

```python
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
```

**What it does:** the loop keeps asking. Inside, a Day 6 `if/elif/else` chain decides what to do. `tries` is a counter updated each round and read at the end. All earlier ideas appear together: input, conversion, comparison, branching, counter, f-string. The loop's only job is to **repeat the whole question**.

### Block 6: `while ... else`

```python
attempts = 0
while attempts < 3:
    attempts += 1
else:
    print("Loop finished normally")
```

**What it does:** the `else` block runs when the loop ends because its **condition became False**, not because of a `break`. This is rare; just know it exists when you read other people's code.

## 6. How the blocks connect

```
Block 1  condition + counter           the skeleton (setup / test / update)
Block 2  the same, counting down       update can be anything
Block 3  while True + break            wait for a valid answer
Block 4  while True + break + total    unknown number of rounds
Block 5  while True + if/elif/else     a whole interaction repeated
Block 6  else clause                   detect "no break happened"
```

Two styles:
- **Condition-controlled** (Blocks 1, 2, 6): the `while` line itself decides.
- **Break-controlled** (Blocks 3, 4, 5): `while True` plus `break` inside.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Forgetting the update | infinite loop | add `count += 1`; stop with `Ctrl+C` |
| Updating in the wrong direction | infinite loop | check `<` vs `>` and `+` vs `-` |
| `while count = 5` | `SyntaxError` | `==` or `<=` |
| `int(input())` crashing on text | `ValueError` | check with `.isdigit()` first (or Day 16) |
| Off-by-one (`<` vs `<=`) | one round too few or many | trace by hand with small numbers |
| Using `while` when `for` is simpler | extra code | if you know the sequence, use `for` |

## 8. Practice

1. Fill in `day09_while_loop.py`: print 1 to 10 using a while loop.
2. Ask for a password until the user types `secret123`. Count the attempts.
3. Keep summing numbers until the user types `0`. Print the total and the average.
4. Guessing game with a hint "too low/too high" and a maximum of 5 tries (hint: `while tries < 5`).
5. Print the digits of a number in reverse: use `% 10` and `// 10` in a loop (Day 5!).
6. Simple menu that repeats until the user chooses `Quit`.

## 9. Self-check

- When do you choose `while` over `for`?
- What are the three parts of a well-formed while loop?
- What does `while True:` need in order to end?
- What does `Ctrl + C` do?

**Next:** Day 10: store **many values** in one variable with lists. Then your loops finally have something real to walk through.

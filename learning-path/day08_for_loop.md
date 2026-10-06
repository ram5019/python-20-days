# Day 8: for Loops

**Time:** ~2 hours | **Example:** `examples/day08_for_loop.py` | **Your practice file:** `week2_logic/day08_for_loop.py`

---

## 1. The big idea

A `for` loop runs the same block of code **once for each item** in a sequence. The sequence can be a range of numbers, the characters of a string, or (from Day 10) the items of a list.

## 2. Why does this exist?

Computers are fast and never bored. Imagine printing 1000 log lines, checking 500 servers, or adding up 10,000 prices. You would never write 1000 `print` lines. You write the action **once** and tell Python how many times to repeat it. This idea, **automation of repetition**, is why programming exists.

## 3. Simple way to understand

A **conveyor belt at an airport**. Bags (items) arrive one at a time. A worker (your loop body) does the same task for each bag: check, tag, load. When the belt is empty, the loop ends. The worker holds a bag called the **loop variable**; each round it refers to the next one.

## 4. How it works

```python
for variable in sequence:
    # body: runs once per item
```

- `variable` takes the next value each round.
- The body is **indented**.
- The loop stops by itself when the sequence runs out.

### `range()`: the number generator

| Call | Produces |
|------|----------|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(1, 10, 2)` | 1, 3, 5, 7, 9 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

The stop value is **excluded**, same as slicing on Day 3.

## 5. Code walkthrough, block by block

### Block 1: repeat N times

```python
for i in range(5):
    print("Round", i)
```

**What it does:** `range(5)` produces 0 to 4. Each round, `i` becomes the next number and the body prints it. Five rounds, because there are five numbers. Counting starts at 0 again.

### Block 2: start, stop, step

```python
for n in range(1, 11, 2):
    print(n, end=" ")
print()
```

**What it does:** starts at 1, stops before 11, jumps by 2 → odd numbers. `end=" "` (Day 1) keeps them on one line. The lone `print()` at the end (unindented, so **outside** the loop) just adds the final newline.

### Block 3: loop over a string

```python
for ch in "WEKA":
    print(ch)
```

**What it does:** a string is a sequence of characters (Day 3), so a loop can walk through it. You did not need `range` or an index. Python hands you each item directly. This "loop over the thing itself" style is the most Pythonic.

### Block 4: the accumulator pattern

```python
total = 0
for n in range(1, 6):
    total += n
print("Sum 1..5 =", total)
```

**What it does:**

| Round | n | total before | total after |
|-------|---|--------------|-------------|
| 1 | 1 | 0 | 1 |
| 2 | 2 | 1 | 3 |
| 3 | 3 | 3 | 6 |
| 4 | 4 | 6 | 10 |
| 5 | 5 | 10 | 15 |

`total` is created **before** the loop (otherwise `total += n` has nothing to add to) and **updated inside**. The final `print` is outside, so it runs once at the end. This pattern, **initialise → update in loop → use after**, powers sums, counts, averages and maximums. It combines Day 2 re-assignment with Day 5 `+=`.

### Block 5: a condition inside a loop

```python
for n in range(1, 11):
    if n % 2 == 0:
        print(n, "is even")
```

**What it does:** the loop provides the numbers, the `if` (Day 6) filters them, and `%` (Day 5) does the test. Loop + if = "for each item, **if** it matches, do something". You will use this constantly.

### Block 6: nested loops

```python
for row in range(1, 4):
    for col in range(1, 4):
        print(row * col, end="\t")
    print()
```

**What it does:** the inner loop runs **completely** for every single round of the outer loop.

```
row=1: col=1,2,3 → prints 1 2 3 → newline
row=2: col=1,2,3 → prints 2 4 6 → newline
row=3: col=1,2,3 → prints 3 6 9 → newline
```

The inner `print()` is indented under the outer loop but not the inner one, so it runs once per row to end the line. Total body runs: 3 × 3 = 9.

### Block 7: `break` and `continue`

```python
for n in range(1, 10):
    if n == 3:
        continue
    if n == 6:
        break
    print(n)
```

**What it does:** prints `1 2 4 5`.
- `continue` skips the rest of **this round** and goes to the next item (3 is skipped).
- `break` **exits the loop entirely** (stops at 6, so 6 to 9 never run).

## 6. How the blocks connect

```
Block 1  range(N)           repeat N times
Block 2  range(a, b, step)  control the numbers
Block 3  any sequence       loop over text (later: lists)
Block 4  + variable         build a result across rounds (accumulator)
Block 5  + if               act only on matches
Block 6  loop inside loop   two dimensions
Block 7  break / continue   control the flow from inside
```

Each block **adds one ingredient** to the same basic loop.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `range(5)` expecting 1 to 5 | gets 0 to 4 | `range(1, 6)` |
| Forgetting to initialise `total = 0` | `NameError` | Create it before the loop |
| Putting `total = 0` **inside** the loop | resets each round | Move it outside |
| Printing the result inside the loop | prints every round | Unindent the print |
| Modifying the list you are looping over | skipped items | Loop over a copy (Day 11) |
| Wrong indentation | body outside the loop | Check the indent |

## 8. Practice

1. Fill in `day08_for_loop.py`: print the numbers 1 to 10, then 10 down to 1.
2. Print the 7 times table up to 12.
3. Sum all numbers from 1 to 100. (Check: 5050.)
4. Count the vowels in a sentence typed by the user.
5. Print a right triangle:
   ```
   *
   **
   ***
   ```
6. Print only multiples of 3 or 5 up to 50.

## 9. Self-check

- What does the loop variable hold on each round?
- Why does `range(5)` start at 0 and stop at 4?
- Where must an accumulator be created, and why?
- How is `break` different from `continue`?

**Next:** Day 9: repeat **until something happens**, when you do not know how many rounds in advance.

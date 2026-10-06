# Day 1: Hello Python

**Time:** ~1.5 hours | **Example:** `examples/day01_hello.py` | **Your practice file:** `week1_basics/day01_hello.py`

---

## 1. The big idea

A Python program is a **text file of instructions**. Python reads it **top to bottom, one line at a time**, and does what each line says. Today's first instruction is `print()`, which shows text on the screen.

## 2. Why does this exist?

Computers do exactly what you tell them, nothing more. You need a way to:

- write instructions in a form humans can read (Python), and
- see the result (output).

`print()` is your **window into the program**. For the next 20 days, whenever you wonder "what is my code doing?", you will use `print()` to find out. Professional developers still do this daily.

## 3. Simple way to understand

Think of Python as a **very literal assistant** reading a recipe.

- The recipe = your `.py` file.
- Each line = one step.
- The assistant starts at the top and never skips ahead.
- `print("hello")` = "say the word hello out loud".

If you misspell an instruction, the assistant stops and says "I don't understand this line". That message is called an **error**, and it is helpful, not a failure.

## 4. How it works

| Piece | Example | Meaning |
|-------|---------|---------|
| Function call | `print(...)` | Ask Python to run a built-in action. The `( )` hold what you give it. |
| String | `"Hello"` | Text. Must be inside quotes (`"..."` or `'...'`). |
| Number | `15` | No quotes. Python treats it as a number. |
| Comment | `# note` | Ignored by Python. Notes for humans. |
| Argument | `sep="-"` | An option you pass to a function to change its behaviour. |

Case matters: `print` works, `Print` does not.

## 5. Code walkthrough, block by block

### Block 1: the simplest program

```python
print("Hello, Python!")
```

**What it does:** calls `print` and gives it one string. Python writes `Hello, Python!` and moves to a new line.
**Why the quotes?** Without them Python would think `Hello` is a name it should already know, and raise an error.

### Block 2: printing several things

```python
print("Name: Ram")
print("Role:", "Engineer")
print("Years of experience:", 15)
```

**What it does:** three separate instructions, run in order, so you get three lines.
Passing two items separated by a comma prints both with a space between.
`15` has no quotes because it is a number. Try `print("15" + 1)` later and see what happens (Day 2 explains).

### Block 3: controlling print

```python
print("A", "B", "C", sep="-")
print("No newline here...", end=" ")
print("...so this continues the same line")
```

**What it does:**
- `sep="-"` changes the separator from a space to `-`, giving `A-B-C`.
- `end=" "` changes what print writes at the end. By default it is a new line. Here it is a space, so the next `print` continues on the same line.

These are **keyword arguments**: `name=value`. You will see this pattern everywhere in Python.

### Block 4: a program with a `main()` function

```python
def main():
    print("Name: Ram")
    print("City: Chennai")

if __name__ == "__main__":
    main()
```

**What it does:**
- `def main():` defines a **function**, a named bundle of instructions. Nothing runs yet. It only stores the recipe.
- The indented lines are the body of the function. Indentation (4 spaces) is how Python knows what belongs inside.
- `if __name__ == "__main__":` means "only if this file is run directly". Then `main()` actually runs the bundle.

Your existing `day01_hello.py` stub already uses this shape. Every file in this course follows it, so learn it now even if it feels like magic. Day 14 explains functions fully, and Day 17 explains why the `if __name__` line matters.

## 6. How the blocks connect

```
Block 1  one instruction          ─┐
Block 2  many instructions, order  │ same idea: lines run top to bottom
Block 3  options on an instruction ┘ (print can be tuned with sep/end)
Block 4  wrap instructions in a function and call it
```

Blocks 1 to 3 run immediately, top to bottom. Block 4 is different: the body of `main` does **not** run when Python reads `def`. It runs only when `main()` is called on the last line. This "define first, run later" idea is the foundation of everything from Day 14 onward.

## 7. Common mistakes

| Mistake | What you see | Fix |
|---------|--------------|-----|
| `Print("hi")` | `NameError: name 'Print' is not defined` | Python is case-sensitive: `print` |
| `print("hi)` | `SyntaxError: unterminated string literal` | Close the quote |
| `print "hi"` | `SyntaxError` | Python 3 needs parentheses |
| Body not indented under `def` | `IndentationError` | Indent 4 spaces |

**Reading errors:** look at the **last line** first. It names the problem. The line above shows where.

## 8. Practice

1. Fill in `week1_basics/day01_hello.py` to print your real name, age and city on 3 lines.
2. Print a box using only `print`:
   ```
   +--------+
   | Python |
   +--------+
   ```
3. Print `1 2 3` as `1, 2, 3` using `sep`.
4. Add a `#` comment to every line of your file explaining it.
5. Break the program 3 different ways on purpose. Read each error.

## 9. Self-check

- What does Python do when it reaches a `def` line? (Does it run the body?)
- What is the difference between `"15"` and `15`?
- What do `sep` and `end` change?
- Why does indentation matter?

**Next:** Day 2 lets you store values (like your name) so you do not retype them.

# Day 4: User Input

**Time:** ~1.5 hours | **Example:** `examples/day04_input.py` | **Your practice file:** `week1_basics/day04_input.py`

---

## 1. The big idea

`input()` pauses the program, shows a prompt, waits for the user to type and press Enter, then **returns what they typed as a string**.

## 2. Why does this exist?

Until now your programs always did the same thing, because the data was written into the file. Real programs react to **different data each run**. `input()` is the first way data enters your program from outside, and it turns a script into a tool.

Every program has the same skeleton:

```
INPUT  →  PROCESS  →  OUTPUT
```

Days 1 to 3 gave you the OUTPUT and PROCESS parts. Today adds INPUT.

## 3. Simple way to understand

`input()` is a **form field** with a question printed next to it.

- The prompt is the label on the form.
- The user fills the field and presses Enter to submit.
- The answer is always handed back as **handwriting (text)**, even if they wrote `42`. If you want to do maths with it, you must **read it as a number** first, which is conversion.

## 4. How it works

```python
answer = input("Prompt text: ")
```

1. Python prints the prompt (no newline).
2. Execution **stops** until Enter.
3. Typed text is returned. You store it in a variable.

Key rule: **the result is always `str`.**

| You want | Write |
|----------|-------|
| text | `input("...")` |
| whole number | `int(input("..."))` |
| decimal | `float(input("..."))` |

## 5. Code walkthrough, block by block

### Block 1: ask for text

```python
name = input("What is your name? ")
print("Hello,", name)
```

**What it does:** shows the question, waits, stores your answer in `name`, then prints a greeting using it. Note the space at the end of the prompt string. It keeps your typing from touching the question mark.

### Block 2: input is always a string

```python
age_text = input("How old are you? ")
print(type(age_text))    # <class 'str'>
```

**What it does:** even if you type `38`, Python gives back the **text** `"38"`. Run this and check the type to convince yourself. This is where Day 2's type conversion ideas pay off.

### Block 3: convert to a number

```python
age = int(age_text)
print("Next year you will be", age + 1)
```

**What it does:** `int()` turns `"38"` into `38`, and now `+ 1` is numeric maths. **Link to Block 2:** it takes the string from Block 2 and fixes its type. If you tried `age_text + 1` you would get a `TypeError`.

### Block 4: convert immediately

```python
height = float(input("Height in metres? "))
print(f"Height in cm: {height * 100}")
```

**What it does:** nests `input()` inside `float()`. The inner call runs first (gets text), the outer one converts it. This is the way experienced Python programmers write it: you rarely need the raw string.

### Block 5: clean the input

```python
city = input("City? ").strip().title()
print(f"Welcome from {city}!")
```

**What it does:** chains string methods from Day 3. `"  chennai "` becomes `"Chennai"`. Users type messy data (extra spaces, wrong case). Cleaning it on arrival means the rest of your program can trust it.

### Block 6: input → process → output

```python
price = float(input("Price of one item: "))
qty = int(input("Quantity: "))
total = price * qty
print(f"Total: {total:.2f}")
```

**What it does:**
- **Input:** two values, converted to the right types.
- **Process:** `price * qty`.
- **Output:** an f-string. `:.2f` formats the number to 2 decimal places, which is useful for money.

This block is the template for almost every small program you will write.

## 6. How the blocks connect

```
Block 1  get text
Block 2  discover: it's a str
Block 3  fix: convert         ──► Block 4  same, shorter
Block 5  clean text (Day 3)
Block 6  put it all together: input → process → output
```

Notice that Block 3 exists **because of** Block 2. Problem, then fix. That is how you learn: hit the issue, then understand the tool.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `age = input()` then `age + 1` | `TypeError` | `age = int(input())` |
| User types `abc` for `int()` | `ValueError` crash | Day 16 (try/except) handles this |
| User types `3.5` into `int()` | `ValueError` | Use `float()`, or `int(float(x))` |
| Forgot trailing space in prompt | `Name:Ram` looks cramped | `"Name: "` |
| Empty answer | `int("")` crashes | Validate (Days 6 and 16) |

Right now your programs will crash on bad input. That is expected. Days 6 and 16 teach you to stop that.

## 8. Practice

1. Fill in `day04_input.py`: ask for name, age and city, then print one friendly sentence.
2. Ask for a temperature in Celsius and print Fahrenheit (`c * 9 / 5 + 32`).
3. Ask for two numbers and print their sum, difference, product.
4. Ask for a full name and print it back reversed order: `Last, First`.
5. Deliberately type letters into a number prompt. Read the error.

## 9. Self-check

- What type does `input()` always return?
- Why does `int(input(...))` work from the inside out?
- What is the INPUT → PROCESS → OUTPUT pattern?
- What does `.2f` do?

**Next:** Day 5: operators, the tools of the PROCESS step.

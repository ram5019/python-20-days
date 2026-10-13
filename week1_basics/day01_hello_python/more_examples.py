"""Day 1: Hello Python. 10 examples, simple to complex.

Run:  python3 week1_basics/day01_hello_python/more_examples.py

Every example has three notes:
  WHAT: what it demonstrates
  HOW : how the code works
  WHY : why it matters later
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "The simplest program")
# WHAT: print one line of text.
# HOW : print() is a built-in function; the text inside quotes is a string.
# WHY : print() is your window into the program. You will use it to debug
#       for the rest of your career.
print("Hello, Python!")

# ---------------------------------------------------------------
show(2, "Several values in one print")
# WHAT: print text and a number together.
# HOW : commas separate the values; print puts one space between them.
#       The number 15 has no quotes, so Python treats it as a number.
# WHY : you rarely print only fixed text; usually text plus data.
print("Servers online:", 15)
print("Temperature:", 36.6, "C")

# ---------------------------------------------------------------
show(3, "Changing the separator with sep=")
# WHAT: control what goes between the values.
# HOW : sep is a keyword argument (name=value). The default is one space.
# WHY : keyword arguments appear everywhere in Python; this is your first one.
print("2026", "10", "13", sep="-")
print("a", "b", "c", sep="")

# ---------------------------------------------------------------
show(4, "Staying on the same line with end=")
# WHAT: print several things on one line.
# HOW : print normally ends with a newline; end=" " replaces it with a space.
# WHY : lets you build one line from many prints (e.g. inside loops, Day 8).
print("Loading", end=" ")
print("...", end=" ")
print("done")

# ---------------------------------------------------------------
show(5, "Special characters: \\n, \\t and quotes")
# WHAT: put a new line or a tab inside a string.
# HOW : a backslash starts an escape sequence: \n = new line, \t = tab.
#       To use a quote inside text, use the other kind of quote around it.
# WHY : you will format reports and handle text with quotes constantly.
print("Line one\nLine two")
print("Name\tAge")
print("Ana\t30")
print("She said: 'hello'")
print('He said: "hi"')

# ---------------------------------------------------------------
show(6, "Multi-line text with triple quotes")
# WHAT: one string that spans several lines.
# HOW : triple quotes keep the line breaks exactly as typed.
# WHY : handy for messages, help text and SQL later on.
message = """Dear user,
Your report is ready.
Regards"""
print(message)

# ---------------------------------------------------------------
show(7, "Drawing with repetition: string * number")
# WHAT: print a banner by repeating a character.
# HOW : "=" * 20 repeats the string 20 times. Multiplying a string repeats it.
# WHY : a first taste of "operators behave differently on different types".
print("=" * 20)
print("  REPORT")
print("=" * 20)

# ---------------------------------------------------------------
show(8, "A small aligned table")
# WHAT: print rows that line up in columns.
# HOW : \t jumps to the next tab stop, so columns align.
# WHY : readable output matters; real tools print tables all the time.
print("Item\tQty\tPrice")
print("Pen\t10\t1.50")
print("Book\t2\t12.00")

# ---------------------------------------------------------------
show(9, "Putting code in a function")
# WHAT: wrap prints in a function and call it twice.
# HOW : def stores the instructions; nothing runs until the function is called.
# WHY : "define first, run later" is the foundation of Day 14 (functions).
def print_card():
    print("+--------+")
    print("| Python |")
    print("+--------+")


print_card()
print_card()

# ---------------------------------------------------------------
show(10, "Reading an error on purpose, then a complete mini program")
# WHAT: cause a NameError safely, read it, then run a small main().
# HOW : try/except catches the error so the program keeps going (Day 16).
#       main() plus the __name__ check is the shape of every script in this course.
# WHY : errors are information. Reading them is the most important beginner skill.
try:
    print(undefined_name)           # we never created this name
except NameError as error:
    print("Python said:", error)


def main():
    print("Name: Sam")
    print("Age:", 30)
    print("City: Paris")


if __name__ == "__main__":
    main()

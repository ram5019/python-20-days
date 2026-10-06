"""Day 3 example: strings.

Run:  python3 learning-path/examples/day03_strings.py
"""

# BLOCK 1: create and join strings
first = "Ramakrishna"
last = "Subbarao"
full = first + " " + last
print(full)

# BLOCK 2: f-strings (insert variables into text)
age = 38
print(f"{first} is {age} years old")

# BLOCK 3: indexing and slicing
word = "Python"
print(word[0])        # P
print(word[-1])       # n
print(word[0:3])      # Pyt
print(word[::-1])     # nohtyP (reversed)

# BLOCK 4: string methods
message = "  Hello, World  "
print(message.strip())        # remove outer spaces
print(message.lower())
print(message.upper())
print(message.replace("World", "Python"))
print("a,b,c".split(","))     # ['a', 'b', 'c']

# BLOCK 5: checking inside strings
email = "ram@weka.io"
print("@" in email)           # True
print(email.endswith(".io"))  # True
print(len(email))             # 11

# BLOCK 6: strings are immutable
word = "Python"
new_word = word.upper()
print(word, new_word)         # Python PYTHON (original unchanged)

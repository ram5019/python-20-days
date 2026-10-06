"""Day 1 example: Hello Python, print(), comments, running a script.

Run:  python3 learning-path/examples/day01_hello.py
"""

# BLOCK 1: the simplest program
print("Hello, Python!")

# BLOCK 2: print several things
print("Name: Ram")
print("Role:", "Engineer")          # comma puts a space between items
print("Years of experience:", 15)   # numbers need no quotes

# BLOCK 3: control how print behaves
print("A", "B", "C", sep="-")       # separator between items
print("No newline here...", end=" ")
print("...so this continues the same line")

# BLOCK 4: a program is a function plus an entry point
def main():
    print("Name: Ram")
    print("City: Chennai")

if __name__ == "__main__":
    main()

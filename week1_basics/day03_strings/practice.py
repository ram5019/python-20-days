"""Day 3 — Strings.
Task: Print length and reverse of a sentence.
"""

def main():
    s = input("Enter a sentence: ")
    print("Length:", len(s))
    print("Reverse:", s[::-1])

if __name__ == "__main__":
    main()
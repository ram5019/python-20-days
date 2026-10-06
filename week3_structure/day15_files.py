"""Day 15 — File Handling.
Task: Save a shopping list, then read it back.
"""

def main():
    items = ["milk", "bread", "eggs"]
    with open("shop.txt", "w") as f:
        f.write("\n".join(items))

    with open("shop.txt") as f:
        print(f.read())

if __name__ == "__main__":
    main()
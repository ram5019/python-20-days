"""Day 13 — Dictionaries.
Task: Store 3 friends' phone numbers, look one up.
"""

def main():
    friends = {
        "Ravi": "9999911111",
        "Asha": "8888822222",
        "Sam":  "7777733333",
    }
    name = input("Search name: ")
    print(friends.get(name, "Not found"))

if __name__ == "__main__":
    main()
"""Day 10 — Lists.
Task: Make a to-do list.
"""

def main():
    tasks = []
    for i in range(3):
        tasks.append(input(f"Task {i+1}: "))
    print("Your list:", tasks)

if __name__ == "__main__":
    main()
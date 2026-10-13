"""Day 11 — List Methods.
Task: Find largest number without max().
"""

def main():
    nums = [5, 2, 9, 1, 7]
    largest = nums[0]
    for n in nums:
        if n > largest:
            largest = n
    print("Largest:", largest)

if __name__ == "__main__":
    main()
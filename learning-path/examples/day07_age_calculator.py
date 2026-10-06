"""Day 7 example: Age calculator (mini project combining Days 1-6).

Run:  python3 learning-path/examples/day07_age_calculator.py
"""

from datetime import datetime

# BLOCK 1: INPUT (Day 4): get and convert
def get_birth_year():
    text = input("Birth year (e.g. 1988): ").strip()
    return int(text)

# BLOCK 2: PROCESS (Day 5): calculate
def calculate_age(birth_year, current_year):
    return current_year - birth_year

# BLOCK 3: DECIDE (Day 6): classify
def life_stage(age):
    if age < 0:
        return "not born yet"
    elif age < 13:
        return "child"
    elif age < 20:
        return "teenager"
    elif age < 60:
        return "adult"
    else:
        return "senior"

# BLOCK 4: OUTPUT (Days 1-3): format and print
def show_result(name, age, stage):
    print(f"\nHello, {name.title()}!")
    print(f"You are about {age} years old ({stage}).")
    print(f"In 10 years you will be {age + 10}.")

# BLOCK 5: wire everything together
def main():
    name = input("Your name: ").strip()
    birth_year = get_birth_year()
    current_year = datetime.now().year

    if birth_year > current_year:
        print("That year is in the future!")
        return

    age = calculate_age(birth_year, current_year)
    stage = life_stage(age)
    show_result(name, age, stage)

if __name__ == "__main__":
    main()

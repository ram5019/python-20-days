"""Day 13: Dictionaries. 10 examples, simple to complex.

Run:  python3 week2_logic/day13_dictionaries/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Create a dictionary and read from it")
# WHAT: store values under names (keys).
# HOW : {key: value}. Look up with d[key].
# WHY : self-describing data: person["city"] beats person[2].
person = {"name": "Asha", "age": 28, "city": "Paris"}
print(person["name"], person["city"])
print(len(person))

# ---------------------------------------------------------------
show(2, "Add, update and delete")
# WHAT: change a dictionary.
# HOW : assigning to a key adds it if new, updates it if it exists.
#       del removes a pair; pop removes AND returns the value.
# WHY : dictionaries are mutable, like lists.
person["age"] = 29
person["job"] = "Engineer"
del person["city"]
removed = person.pop("job")
print(person, "| popped:", removed)

# ---------------------------------------------------------------
show(3, "Safe lookups")
# WHAT: avoid KeyError for missing keys.
# HOW : .get(key, default) returns the default instead of crashing;
#       `in` checks KEYS.
# WHY : real data often lacks fields.
print(person.get("phone"))
print(person.get("phone", "unknown"))
print("name" in person, "phone" in person)
try:
    print(person["phone"])
except KeyError as error:
    print("KeyError for", error)

# ---------------------------------------------------------------
show(4, "Looping: keys, values, items")
# WHAT: three ways to visit a dictionary.
# HOW : for k in d -> keys; d.values(); d.items() gives (key, value) pairs.
# WHY : .items() with unpacking is the form you will use most.
stock = {"apples": 5, "pears": 0, "plums": 12}
for key in stock:
    print("key:", key)
for qty in stock.values():
    print("value:", qty)
for item, qty in stock.items():
    print(f"{item:<7} {qty:>3}")

# ---------------------------------------------------------------
show(5, "Counting things")
# WHAT: how many times does each word or letter appear?
# HOW : counts.get(x, 0) + 1 starts from 0 for new keys.
# WHY : the most common dictionary recipe: logs, votes, word frequency.
text = "to be or not to be"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
print(counts)
letters = {}
for ch in "banana":
    letters[ch] = letters.get(ch, 0) + 1
print(letters)

# ---------------------------------------------------------------
show(6, "Grouping into lists")
# WHAT: sort items into buckets.
# HOW : each value is a list; setdefault creates it on first use.
# WHY : group by category, by first letter, by status.
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
groups = {}
for w in words:
    groups.setdefault(w[0], []).append(w)
print(groups)

# ---------------------------------------------------------------
show(7, "Nested dictionaries")
# WHAT: a dictionary of dictionaries.
# HOW : read with two keys: d["n1"]["status"].
# WHY : configuration files and JSON look like this.
cluster = {
    "n1": {"status": "up", "cpu": 35},
    "n2": {"status": "down", "cpu": 0},
    "n3": {"status": "up", "cpu": 91},
}
print(cluster["n3"]["cpu"])
cluster["n2"]["status"] = "up"
for name, info in cluster.items():
    print(name, info["status"], info["cpu"])

# ---------------------------------------------------------------
show(8, "A list of dictionaries is a table")
# WHAT: each dict is a row; each key is a column.
# HOW : loop for filtering; sorted(..., key=lambda ...) for ordering;
#       max(..., key=...) for the best row.
# WHY : the shape of almost all real data (CSV rows, API results).
students = [
    {"name": "Asha", "marks": 88},
    {"name": "Ravi", "marks": 72},
    {"name": "Meena", "marks": 95},
]
print([s["name"] for s in students if s["marks"] >= 80])
for s in sorted(students, key=lambda s: s["marks"], reverse=True):
    print(s["name"], s["marks"])
top = max(students, key=lambda s: s["marks"])
print("Topper:", top["name"])
print("Average:", sum(s["marks"] for s in students) / len(students))

# ---------------------------------------------------------------
show(9, "Dict comprehension, merging and inverting")
# WHAT: build and combine dictionaries concisely.
# HOW : {k: v for ...}; a | b merges (right side wins); invert by swapping.
# WHY : transforming data between shapes.
squares = {n: n * n for n in range(1, 6)}
print(squares)
defaults = {"theme": "light", "font": 12}
user = {"font": 14}
print(defaults | user)
codes = {"FR": "France", "DE": "Germany"}
print({name: code for code, name in codes.items()})

# ---------------------------------------------------------------
show(10, "Mini program: an inventory manager")
# WHAT: a dictionary plus small functions.
# HOW : each function changes or reads the same dict; errors are reported,
#       not crashed on.
# WHY : dict + functions is the core of countless small tools.
inventory = {}


def add_item(name, qty):
    inventory[name] = inventory.get(name, 0) + qty


def remove_item(name, qty):
    if inventory.get(name, 0) < qty:
        print(f"  cannot remove {qty} {name}: only {inventory.get(name, 0)}")
        return
    inventory[name] -= qty
    if inventory[name] == 0:
        del inventory[name]


add_item("pen", 10)
add_item("book", 3)
add_item("pen", 5)
remove_item("book", 5)
remove_item("book", 3)
remove_item("pen", 4)
print(inventory)
low = [name for name, qty in inventory.items() if qty < 20]
print("Low stock:", low)

"""Day 22: lambda, map, filter. 10 examples, simple to complex.

Run:  python3 advanced/day22_lambda_map_filter/more_examples.py
"""

from functools import reduce


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "A lambda is a one-line function")
# WHAT: the same function written two ways.
# HOW : lambda parameters: expression. No return keyword, one expression only.
# WHY : handy when a function is needed for just a moment.
def double(x):
    return x * 2


double_l = lambda x: x * 2          # fine for learning; use def if you name it
print(double(4), double_l(4))
print((lambda a, b: a + b)(3, 4))   # called immediately, no name at all

# ---------------------------------------------------------------
show(2, "Functions are values: pass them around")
# WHAT: give a function to another function.
# HOW : no parentheses when passing; the receiver calls it.
# WHY : the idea behind map, filter, key=, and decorators (Day 23).
def apply(func, value):
    return func(value)


print(apply(str.upper, "hello"))
print(apply(lambda n: n ** 2, 7))
print(apply(len, [1, 2, 3]))

# ---------------------------------------------------------------
show(3, "map: apply to every item")
# WHAT: transform a whole list.
# HOW : map(func, items) returns a lazy iterator, so wrap it in list().
# WHY : the functional way to convert data.
nums = [1, 2, 3, 4]
print(list(map(lambda x: x * 10, nums)))
print(list(map(str, nums)))
print(list(map(float, ["1.5", "2", "3.25"])))
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))     # two lists

# ---------------------------------------------------------------
show(4, "filter: keep what passes a test")
# WHAT: select items.
# HOW : filter(func, items): keep items where func returns True.
# WHY : like a comprehension's if.
print(list(filter(lambda x: x % 2 == 0, range(10))))
print(list(filter(None, [0, 1, "", "a", [], [1], None])))    # drop falsy values
print(list(filter(str.isalpha, ["abc", "a1", "xyz", "9"])))

# ---------------------------------------------------------------
show(5, "key= with sorted: the most useful lambda")
# WHAT: sort by something other than the item itself.
# HOW : key=lambda item: the value to sort by.
# WHY : sorting records by a field is an everyday need.
students = [("Asha", 88), ("Ravi", 72), ("Meena", 95)]
print(sorted(students, key=lambda s: s[1]))
print(sorted(students, key=lambda s: s[1], reverse=True))
words = ["pear", "fig", "banana", "kiwi"]
print(sorted(words, key=len))
print(sorted(words, key=lambda w: (len(w), w)))       # length, then alphabetical

# ---------------------------------------------------------------
show(6, "key= with max, min and dictionaries")
# WHAT: find the record with the biggest/smallest field.
# HOW : max(items, key=...) returns the whole item, not the key value.
# WHY : "which server is busiest?", "who scored highest?".
servers = [{"name": "web01", "cpu": 40}, {"name": "db01", "cpu": 85},
           {"name": "web02", "cpu": 15}]
print(max(servers, key=lambda s: s["cpu"])["name"])
print(min(servers, key=lambda s: s["cpu"])["name"])
print([s["name"] for s in sorted(servers, key=lambda s: -s["cpu"])])

# ---------------------------------------------------------------
show(7, "reduce: fold a list into one value")
# WHAT: combine items step by step.
# HOW : reduce(func, items, start). func gets (running_result, next_item).
# WHY : the general form of sum, product and max.
print(reduce(lambda total, n: total + n, [1, 2, 3, 4], 0))
print(reduce(lambda total, n: total * n, range(1, 6), 1))
print(reduce(lambda best, n: n if n > best else best, [3, 9, 2], 0))

# ---------------------------------------------------------------
show(8, "Choosing between lambda, comprehension and def")
# WHAT: the same task three ways.
# HOW : read them side by side.
# WHY : Python style prefers comprehensions for simple map/filter,
#       and lambda mainly for key=.
data = [1, 2, 3, 4, 5, 6]
a = list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, data)))
b = [x * x for x in data if x % 2 == 0]


def squares_of_evens(items):
    result = []
    for x in items:
        if x % 2 == 0:
            result.append(x * x)
    return result


print(a, b, squares_of_evens(data))

# ---------------------------------------------------------------
show(9, "Functions that return functions (closures)")
# WHAT: build customised functions.
# HOW : the inner lambda remembers the outer variable.
# WHY : the foundation of decorators (Day 23).
def make_multiplier(n):
    return lambda x: x * n


triple = make_multiplier(3)
tax = make_multiplier(1.18)
print(triple(5), round(tax(100), 2))
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
}
for name, op in operations.items():
    print(name, op(6, 3))

# ---------------------------------------------------------------
show(10, "Mini program: a data pipeline")
# WHAT: clean, filter, transform and rank raw records.
# HOW : each step is a small function; the pipeline chains them.
# WHY : data processing is a chain of small, testable steps.
raw = ["Asha:88", " ravi : 72", "MEENA:95", "bad", "John:abc", "Li:61"]


def parse(line):
    parts = [p.strip() for p in line.split(":")]
    if len(parts) != 2 or not parts[1].isdigit():
        return None
    return parts[0].title(), int(parts[1])


parsed = list(filter(None, map(parse, raw)))
passed = filter(lambda r: r[1] >= 70, parsed)
ranked = sorted(passed, key=lambda r: r[1], reverse=True)
print(parsed)
for rank, (name, score) in enumerate(ranked, start=1):
    print(f"{rank}. {name} {score}")

"""Day 11: List methods. 10 examples, simple to complex.

Run:  python3 week2_logic/day11_list_methods/more_examples.py
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "append: add to the end")
# WHAT: grow a list one item at a time.
# HOW : list.append(item) changes the list and returns None.
# WHY : the most-used list method.
tasks = ["email"]
tasks.append("review")
tasks.append("deploy")
print(tasks)

# ---------------------------------------------------------------
show(2, "insert and extend")
# WHAT: add at a chosen position; add several items.
# HOW : insert(index, item); extend(another_list) adds each item.
#       append(list) would add ONE item that is itself a list.
# WHY : knowing append vs extend avoids nested-list surprises.
tasks.insert(0, "standup")
tasks.extend(["lunch", "report"])
print(tasks)
demo = [1, 2]
demo.append([3, 4])
print(demo)
demo = [1, 2]
demo.extend([3, 4])
print(demo)

# ---------------------------------------------------------------
show(3, "Three ways to remove")
# WHAT: remove by value, by position (and get it back), or by index.
# HOW : remove(value); pop(index) RETURNS the item; del list[index].
# WHY : pop is how you take "the next job" off a queue or stack.
tasks.remove("lunch")
last = tasks.pop()
first = tasks.pop(0)
print("popped:", last, "and", first)
del tasks[0]
print(tasks)

# ---------------------------------------------------------------
show(4, "Search and count")
# WHAT: find things without a loop.
# HOW : in, index, count. Check with `in` BEFORE index/remove to avoid errors.
# WHY : safe lookups.
nums = [5, 3, 8, 3, 1]
print(nums.index(8), nums.count(3), 8 in nums)
if 99 in nums:
    nums.remove(99)
else:
    print("99 is not in the list, nothing to remove")

# ---------------------------------------------------------------
show(5, "sort() versus sorted()")
# WHAT: two ways to order a list.
# HOW : .sort() reorders the SAME list and returns None;
#       sorted() leaves the original alone and returns a new list.
# WHY : choose depending on whether you need the old order.
values = [3, 1, 2]
print(sorted(values), values)
values.sort(reverse=True)
print(values)
words = ["banana", "Apple", "cherry"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=len))

# ---------------------------------------------------------------
show(6, "The classic bug: x = x.sort()")
# WHAT: see what happens when you store the result of sort().
# HOW : sort() returns None, so you replace your list with None.
# WHY : one of the most common beginner mistakes.
data = [3, 1, 2]
result = data.sort()
print("data:", data, "| result:", result)

# ---------------------------------------------------------------
show(7, "Build a list in a loop and filter into a new one")
# WHAT: loop, test, collect.
# HOW : start with [], append what you want.
# WHY : the pattern behind most data processing.
squares = []
for n in range(1, 8):
    squares.append(n * n)
print(squares)
scores = [45, 82, 67, 91, 30]
passed = []
for s in scores:
    if s >= 50:
        passed.append(s)
print(passed)

# ---------------------------------------------------------------
show(8, "A stack and a queue")
# WHAT: two classic structures built from a list.
# HOW : stack = last in, first out: append + pop().
#       queue = first in, first out: append + pop(0).
# WHY : undo history is a stack; a print queue is a queue.
stack = []
for page in ["home", "search", "result"]:
    stack.append(page)
print("back button visits:", stack.pop(), stack.pop())
queue = ["job1", "job2", "job3"]
while queue:
    print("processing", queue.pop(0))

# ---------------------------------------------------------------
show(9, "Remove duplicates but keep the order")
# WHAT: unique items in their original order.
# HOW : keep a "seen" list; only append items not yet seen.
# WHY : clean data. (Day 12 shows an even shorter way with sets.)
raw = ["a", "b", "a", "c", "b", "d"]
unique = []
for item in raw:
    if item not in unique:
        unique.append(item)
print(unique)

# ---------------------------------------------------------------
show(10, "Mini program: a to-do manager")
# WHAT: a small program using most methods.
# HOW : functions take the list, change it, and report.
# WHY : lists + methods + functions = real programs.
def add(todo, task):
    if task in todo:
        print(f"  '{task}' already exists")
    else:
        todo.append(task)


def complete(todo, task, done):
    if task in todo:
        todo.remove(task)
        done.append(task)
    else:
        print(f"  '{task}' not found")


todo, done = [], []
for t in ["write report", "email Ana", "write report", "fix bug"]:
    add(todo, t)
complete(todo, "email Ana", done)
complete(todo, "call bank", done)
todo.sort()
print("To do:", todo)
print("Done :", done)
print(f"Progress: {len(done)}/{len(done) + len(todo)}")

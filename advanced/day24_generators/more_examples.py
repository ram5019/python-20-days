"""Day 24: Generators. 10 examples, simple to complex.

Run:  python3 advanced/day24_generators/more_examples.py
"""

import itertools
import sys
import tempfile
from pathlib import Path


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "yield: a function that pauses")
# WHAT: produce values one at a time.
# HOW : yield hands back a value and PAUSES; the next request resumes after it.
# WHY : you get items on demand instead of building a whole list first.
def count_up(limit):
    n = 1
    while n <= limit:
        yield n
        n += 1


for x in count_up(3):
    print(x)

# ---------------------------------------------------------------
show(2, "Driving a generator by hand with next()")
# WHAT: see what a for loop does behind the scenes.
# HOW : calling the function builds a generator object; next() runs it to
#       the following yield; StopIteration signals the end.
# WHY : makes the pause/resume idea concrete.
gen = count_up(2)
print(type(gen).__name__)
print(next(gen), next(gen))
try:
    next(gen)
except StopIteration:
    print("exhausted")

# ---------------------------------------------------------------
show(3, "Generator expressions: (x for x in ...)")
# WHAT: a comprehension that does not build a list.
# HOW : parentheses instead of square brackets.
# WHY : constant memory, however large the range.
squares_list = [n * n for n in range(1_000_000)]
squares_gen = (n * n for n in range(1_000_000))
print("list is bigger than generator:", sys.getsizeof(squares_list) > sys.getsizeof(squares_gen))
print(sum(squares_gen))
print(sum(n for n in range(10) if n % 2))          # no extra brackets needed

# ---------------------------------------------------------------
show(4, "A generator is used up once")
# WHAT: the classic surprise.
# HOW : after you read it, it is empty; recreate it or store a list.
# WHY : a frequent source of "my loop did nothing the second time".
g = (n for n in range(3))
print(list(g))
print(list(g))

# ---------------------------------------------------------------
show(5, "An infinite sequence")
# WHAT: Fibonacci numbers without an end.
# HOW : while True with yield; take only as many as you ask for.
# WHY : impossible with a list; trivial with a generator.
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()
print([next(fib) for _ in range(10)])
print(list(itertools.islice(fibonacci(), 5, 10)))           # items 5..9

# ---------------------------------------------------------------
show(6, "Reading a big file lazily")
# WHAT: process a file line by line without loading it.
# HOW : a file object is already a lazy iterator; wrap it in a generator
#       that filters.
# WHY : a 20 GB log fits through a few KB of memory.
def error_lines(path):
    with open(path) as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()


with tempfile.TemporaryDirectory() as folder:
    log = Path(folder) / "app.log"
    log.write_text("".join(f"10:{i:02d} {'ERROR' if i % 3 == 0 else 'INFO'} event {i}\n"
                           for i in range(12)))
    print(list(error_lines(log)))
    print("first error only:", next(error_lines(log)))

# ---------------------------------------------------------------
show(7, "Pipelines: generators feeding generators")
# WHAT: chain small stages.
# HOW : each stage consumes the previous one lazily, so ONE item flows
#       through all stages before the next starts.
# WHY : memory-light data processing with readable stages.
def numbers():
    yield from range(1, 11)


def squares(source):
    for n in source:
        yield n * n


def only_even(source):
    for n in source:
        if n % 2 == 0:
            yield n


print(list(only_even(squares(numbers()))))

# ---------------------------------------------------------------
show(8, "Batching: process a stream in chunks")
# WHAT: yield lists of N items.
# HOW : collect into a buffer; yield when full; flush the remainder.
# WHY : bulk inserts, API calls and file writes work better in batches.
def batches(items, size):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


print(list(batches(range(1, 11), 4)))

# ---------------------------------------------------------------
show(9, "Two-way generators and itertools helpers")
# WHAT: send values INTO a generator; use ready-made lazy tools.
# HOW : .send(value) resumes a generator and gives it a value;
#       itertools provides count, cycle, chain, takewhile...
# WHY : running averages, coroutines; and you rarely need to write your own
#       lazy helper.
def running_average():
    total, count, average = 0.0, 0, None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count


avg = running_average()
next(avg)                                    # prime it
print([round(avg.send(v), 2) for v in (10, 20, 60)])
print(list(itertools.islice(itertools.cycle("ab"), 5)))
print(list(itertools.chain([1, 2], (3,), "x")))
print(list(itertools.takewhile(lambda n: n < 20, (n * n for n in itertools.count(1)))))

# ---------------------------------------------------------------
show(10, "Mini program: a lazy log analysis pipeline")
# WHAT: parse, filter and count a stream of log lines in one pass.
# HOW : generators for each step; a Counter at the end consumes the stream.
# WHY : the same code works for 12 lines or 12 million.
from collections import Counter


def read_lines(lines):
    for line in lines:
        yield line.strip()


def parse(lines):
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) == 3:
            yield {"time": parts[0], "level": parts[1], "msg": parts[2]}


def only(level, records):
    return (r for r in records if r["level"] == level)


raw = ["10:00 INFO start", "10:01 ERROR disk full", "garbage", "10:02 ERROR disk full",
       "10:03 WARN slow", "10:04 ERROR timeout"]
records = parse(read_lines(raw))
errors = only("ERROR", records)
print(Counter(r["msg"] for r in errors).most_common())

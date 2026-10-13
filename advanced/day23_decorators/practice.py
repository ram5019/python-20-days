"""Day 23 — Decorators."""

import time

def timer(func):
    def wrap(*a, **k):
        t = time.time()
        r = func(*a, **k)
        print(f"Took {time.time() - t:.4f}s")
        return r
    return wrap

@timer
def slow():
    time.sleep(1)

def main():
    slow()

if __name__ == "__main__":
    main()
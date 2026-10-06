"""Day 17 — Modules & Libraries.
Task: Roll two dice 10 times using random.
"""

import math
import random
from datetime import datetime

def main():
    print("sqrt(16) =", math.sqrt(16))
    print("Year:", datetime.now().year)

    for _ in range(10):
        print(random.randint(1, 6), random.randint(1, 6))

if __name__ == "__main__":
    main()
"""Day 17 example: modules and imports.

Run:  python3 learning-path/examples/day17_modules.py
(mytools.py in the same folder is imported below.)
"""

# BLOCK 1: import a whole standard-library module
import math
print(math.sqrt(16))                 # 4.0
print(math.pi)
print(math.ceil(4.1), math.floor(4.9))   # 5 4

# BLOCK 2: import specific names
from random import randint, choice
print(randint(1, 6))                 # random die roll
print(choice(["red", "green", "blue"]))

# BLOCK 3: import with a nickname
import datetime as dt
print(dt.date.today())

# BLOCK 4: more useful standard-library modules
import os
import sys
from collections import Counter

print(os.getcwd())                   # current folder
print(sys.version.split()[0])        # Python version
print(Counter("mississippi"))        # counts letters automatically

# BLOCK 5: import YOUR OWN module
import mytools
print(mytools.circle_area(3))
print(mytools.shout("modules work"))

# BLOCK 6: see what a module offers
print([name for name in dir(math) if not name.startswith("_")][:8])
# help(math.sqrt)                    # uncomment for documentation

# BLOCK 7: __name__ in action
print("This file's __name__ is:", __name__)   # "__main__" when run directly
print("mytools' __name__ is:", mytools.__name__)  # "mytools" when imported

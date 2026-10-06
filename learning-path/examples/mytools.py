"""mytools.py: a tiny module used by day17_modules.py.

A module is simply a .py file whose functions/variables can be imported.
"""

PI = 3.14159


def circle_area(radius):
    """Return the area of a circle."""
    return PI * radius ** 2


def shout(text):
    """Return text in uppercase with an exclamation mark."""
    return text.upper() + "!"


# This block runs ONLY when you execute mytools.py directly,
# NOT when another file imports it.
if __name__ == "__main__":
    print("Testing mytools directly")
    print(circle_area(2))
    print(shout("hello"))

"""Day 18: Classes and objects (OOP). 10 examples, simple to complex.

Run:  python3 week3_structure/day18_oop/more_examples.py
"""

from dataclasses import dataclass, field


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "The smallest class")
# WHAT: a blueprint with no behaviour yet.
# HOW : class defines it; Point() builds an object; attributes are set with
#       a dot.
# WHY : your own type, like int or str but designed by you.
class Point:
    pass


p = Point()
p.x = 3
p.y = 4
print(p.x, p.y, type(p).__name__)

# ---------------------------------------------------------------
show(2, "__init__ and methods")
# WHAT: set up each object's data and give it behaviour.
# HOW : __init__ runs automatically on creation; `self` is "this object".
#       Methods are functions inside the class that take self first.
# WHY : bundles data with the functions that use it.
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


r = Rectangle(3, 5)
print(r.width, r.area(), r.perimeter())

# ---------------------------------------------------------------
show(3, "Many objects, each with its own data")
# WHAT: one blueprint, independent objects.
# HOW : changing one object never touches another.
# WHY : model many real things (students, orders, nodes) with one class.
class Student:
    def __init__(self, name):
        self.name = name
        self.marks = []

    def add_mark(self, mark):
        self.marks.append(mark)

    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0


asha, ravi = Student("Asha"), Student("Ravi")
asha.add_mark(90)
asha.add_mark(80)
ravi.add_mark(60)
print(asha.name, asha.average(), "|", ravi.name, ravi.average())

# ---------------------------------------------------------------
show(4, "__str__ and __repr__: how an object prints")
# WHAT: readable output for people and for debugging.
# HOW : __str__ is used by print(); __repr__ shows in lists and the REPL.
# WHY : without them you get "<object at 0x...>", which tells nobody anything.
class Book:
    def __init__(self, title, author):
        self.title, self.author = title, author

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def __repr__(self):
        return f"Book({self.title!r}, {self.author!r})"


b = Book("Dune", "Frank Herbert")
print(b)
print([b])

# ---------------------------------------------------------------
show(5, "Class attributes versus instance attributes")
# WHAT: data shared by all objects versus data owned by one.
# HOW : an attribute defined in the class body is shared; self.x is per object.
# WHY : counters and constants belong to the class; names to the object.
class Counter:
    created = 0                          # shared by every Counter

    def __init__(self):
        self.value = 0                   # each Counter has its own
        Counter.created += 1

    def increment(self):
        self.value += 1


c1, c2 = Counter(), Counter()
c1.increment()
c1.increment()
c2.increment()
print(c1.value, c2.value, "created:", Counter.created)

# ---------------------------------------------------------------
show(6, "Encapsulation: the object protects its own rules")
# WHAT: a bank account that refuses bad operations.
# HOW : methods check the rules and raise errors (Day 16).
# WHY : the rules live in ONE place, not scattered through your program.
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount


acct = BankAccount("Sam", 100)
acct.deposit(50)
acct.withdraw(30)
print(acct.balance)
try:
    acct.withdraw(500)
except ValueError as e:
    print("Declined:", e)

# ---------------------------------------------------------------
show(7, "@property: computed attributes and validation")
# WHAT: an attribute that is really a calculation, or a checked setter.
# HOW : @property makes a method read like an attribute; a setter can
#       validate assignments.
# WHY : lets you change the internals later without changing how callers
#       use the object.
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value


t = Temperature(100)
print(t.celsius, t.fahrenheit)
t.celsius = 0
print(t.fahrenheit)
try:
    t.celsius = -300
except ValueError as e:
    print("Rejected:", e)

# ---------------------------------------------------------------
show(8, "Inheritance: specialise an existing class")
# WHAT: a Dog "is an" Animal.
# HOW : class Dog(Animal) inherits everything; override what differs;
#       super() calls the parent's version.
# WHY : reuse shared code; extend instead of copy-pasting.
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def intro(self):
        return f"{self.name} says {self.speak()}"


class Dog(Animal):
    def speak(self):
        return "Woof"


class Puppy(Dog):
    def __init__(self, name, age_months):
        super().__init__(name)
        self.age_months = age_months

    def speak(self):
        return super().speak() + " (squeaky)"


for pet in (Animal("Generic"), Dog("Rex"), Puppy("Bit", 3)):
    print(pet.intro())

# ---------------------------------------------------------------
show(9, "Composition: an object that HAS other objects")
# WHAT: a Cluster holds a list of Node objects.
# HOW : the cluster stores nodes in a list and uses their methods.
# WHY : "has a" is often better than "is a"; most real models use it.
class Node:
    def __init__(self, name, cpu, up=True):
        self.name, self.cpu, self.up = name, cpu, up

    def is_hot(self):
        return self.up and self.cpu > 80


class Cluster:
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def down_nodes(self):
        return [n.name for n in self.nodes if not n.up]

    def hot_nodes(self):
        return [n.name for n in self.nodes if n.is_hot()]

    def __len__(self):
        return len(self.nodes)


cluster = Cluster("demo")
for node in (Node("n1", 35), Node("n2", 0, up=False), Node("n3", 91)):
    cluster.add(node)
print(len(cluster), "nodes | down:", cluster.down_nodes(), "| hot:", cluster.hot_nodes())

# ---------------------------------------------------------------
show(10, "Mini program: a shopping cart with @dataclass")
# WHAT: less boilerplate for classes that mostly hold data.
# HOW : @dataclass writes __init__, __repr__ and __eq__ for you from the
#       annotated fields; field(default_factory=list) gives each cart its own list.
# WHY : modern Python uses dataclasses for records; methods add behaviour.
@dataclass
class Item:
    name: str
    price: float
    qty: int = 1

    def total(self):
        return self.price * self.qty


@dataclass
class Cart:
    items: list = field(default_factory=list)

    def add(self, item):
        self.items.append(item)

    def total(self):
        return sum(i.total() for i in self.items)

    def cheapest(self):
        return min(self.items, key=lambda i: i.price) if self.items else None


cart = Cart()
cart.add(Item("pen", 1.5, 10))
cart.add(Item("notebook", 4.0, 2))
cart.add(Item("bag", 25.0))
print(cart.items[0])
print(f"Total: {cart.total():.2f}")
print("Cheapest:", cart.cheapest().name)
print(Item("pen", 1.5, 10) == cart.items[0])

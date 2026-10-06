# Day 18: Classes and Objects (OOP)

**Time:** ~3 hours | **Example:** `examples/day18_oop.py` | **Your practice file:** `week3_structure/day18_oop.py`

---

## 1. The big idea

A **class** is a **blueprint** that bundles **data** (attributes) and **behaviour** (methods) into one unit. An **object** (or instance) is one actual thing built from that blueprint.

```python
class Student:          # blueprint
    ...
asha = Student("Asha")  # object made from the blueprint
```

## 2. Why does this exist?

You already have two tools: dictionaries hold **data** (Day 13) and functions hold **behaviour** (Day 14). But they live apart. A dict `{"name": "Asha", "marks": [88, 92]}` does not know how to compute its own average, and any code can put nonsense into it.

A class **keeps related data and functions together** and lets the object **protect its own rules** ("balance cannot go negative"). Big programs are organised around such objects: a Cluster, a Customer, a Ticket, a Connection.

## 3. Simple way to understand

A **cookie cutter and cookies**.

- The **class** is the cutter: it defines the shape (what a cookie has and can do).
- Each **object** is one cookie. Every cookie has the same shape but its **own** chocolate chips and its own bite marks.

Or a **car factory**: one design (class), many cars (objects). Painting one car red does not repaint the others.

| Word | Meaning | Example |
|------|---------|---------|
| class | blueprint | `Student` |
| object / instance | one real thing | `asha`, `ravi` |
| attribute | data the object holds | `asha.name` |
| method | function that belongs to the object | `asha.add_mark(90)` |
| `self` | "this particular object" | first parameter of every method |

## 4. How it works

```python
class ClassName:
    def __init__(self, param):     # constructor: runs when an object is created
        self.attr = param          # store data on THIS object

    def method(self, x):           # behaviour
        return self.attr + x
```

1. `ClassName(5)` creates a new empty object.
2. Python automatically calls `__init__` with that object as `self` and `5` as `param`.
3. `obj.method(3)` is really `ClassName.method(obj, 3)`. That is why `self` is always the first parameter: it is how the method knows **which** object it is working on.

Class names use `CamelCase`; methods and attributes use `snake_case`.

## 5. Code walkthrough, block by block

### Block 1: the problem

```python
student_dict = {"name": "Asha", "marks": [88, 92]}
```

**What it does:** this is just a reminder of where you started. It stores data fine, but there is no place to put `average()` and nothing stops someone typing `student_dict["marks"] = "banana"`.

### Block 2: a minimal class

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.marks = []

    def add_mark(self, mark):
        self.marks.append(mark)

    def average(self):
        if not self.marks:
            return 0
        return sum(self.marks) / len(self.marks)
```

**What it does:**
- `__init__` is the **constructor**. It sets up the starting data. `self.name = name` means "store the given name **on this object**". `self.marks = []` gives every student a fresh, private list.
- `add_mark` and `average` are **methods**: ordinary Day 14 functions, but defined inside the class and taking `self`. They read and change the object's own data through `self.marks`.
- `average` has the same empty-list guard you wrote on Day 14.

Nothing runs yet. This is only the **blueprint**, just as `def` only stored a recipe on Day 1.

### Block 3: creating objects

```python
asha = Student("Asha")
ravi = Student("Ravi")

asha.add_mark(88)
asha.add_mark(92)
ravi.add_mark(70)

print(asha.average())   # 90.0
print(ravi.average())   # 70.0
```

**What it does:** `Student("Asha")` builds an object and runs `__init__`. Two objects now exist, each with its **own** `name` and `marks`. Calling `asha.add_mark(88)` changes only Asha's list, so Ravi's average is unaffected. This is the central benefit: **one blueprint, many independent objects**.

Note you never typed `self` in the calls. Python passes it for you (the object before the dot).

### Block 4: `__str__`

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"'{self.title}' by {self.author}"

print(b)   # 'Dune' by Frank Herbert
```

**What it does:** methods with double underscores (**dunder methods**) are hooks Python calls automatically. `print(b)` calls `b.__str__()` to find out how to display the object. Without it you would see something like `<__main__.Book object at 0x10...>`. It uses an f-string (Day 3) and `return` (Day 14).

### Block 5: an object that protects its rules

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        ...
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

**What it does:** the rules live **inside** the object. Whoever uses `BankAccount` cannot forget to check the balance, because `withdraw` does it. It combines:
- `balance=0` default argument (Day 14),
- `raise ValueError` (Day 16),
- `+=` and `-=` (Day 5),
- `if` checks (Day 6).

The caller handles the failure with `try/except ValueError`, which is exactly Day 16 Block 3. This is called **encapsulation**: data and the rules about that data stay together.

### Block 6: inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "Woof"
```

**What it does:** `class Dog(Animal)` means "a Dog **is an** Animal". Dog automatically gets `__init__` and `name` from Animal, so there is no need to rewrite them. It **overrides** `speak` with its own version. The final loop calls `pet.speak()` on different kinds of animals, and each one responds in its own way, even though the loop code is identical. That is **polymorphism**: same call, different behaviour depending on the object.

Use inheritance when there is a true "is a" relationship. If not, prefer simply holding another object inside (e.g. a `Cluster` *has* a list of `Node`s).

## 6. How the blocks connect

```
Block 1  the limits of dicts + functions
Block 2  class = data + methods in one place    (blueprint)
Block 3  objects = independent copies of it
Block 4  control how an object displays          (__str__)
Block 5  objects enforce their own rules         (encapsulation)
Block 6  reuse and specialise classes            (inheritance)
```

How it ties to earlier days:

| New idea | Built from |
|----------|-----------|
| attributes | variables (Day 2) and dict fields (Day 13) |
| methods | functions (Day 14) |
| `__init__` | a function that runs automatically on creation |
| validation in methods | `if` + `raise` (Days 6 and 16) |
| class definition vs object creation | "define first, run later" from Day 1 |

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Forgetting `self` in a method's parameters | `TypeError: takes 1 positional argument but 2 were given` | first parameter is `self` |
| `name = name` instead of `self.name = name` | attribute never saved | use `self.` |
| Calling the class's method without an object: `Student.average()` | `TypeError` | `asha.average()` |
| Shared mutable class attribute (`marks = []` at class level) | all objects share one list | create it in `__init__` |
| Misspelling `__init__` | no constructor runs | double underscores both sides |
| Using inheritance for everything | tangled code | only for true "is a" cases |
| Not calling `super().__init__()` in a child that defines its own `__init__` | parent attributes missing | call it |

## 8. Practice

1. Fill in `day18_oop.py`: create a `Person` class with `name`, `age` and a `greet()` method.
2. Create a `Rectangle(width, height)` with `area()` and `perimeter()` methods and a nice `__str__`.
3. Extend `BankAccount` with a `history` list that records every deposit and withdrawal, plus a `show_history()` method.
4. Create `Node(name, status)` and `Cluster(name)` where the cluster holds a list of nodes, with `add_node()` and `unhealthy_nodes()`. This is a good model for your own work.
5. Make `Circle` and `Square` classes that both have `area()`. Put them in one list and loop over them.
6. Reproduce the "forgot `self`" error and read the message.

## 9. Self-check

- What is the difference between a class and an object?
- What does `self` refer to?
- When does `__init__` run?
- Why is putting `balance` rules inside `BankAccount` better than checking them in outside code?
- What does `class Dog(Animal)` mean?

**Next:** Day 19: turn your dictionaries, lists and objects into **text** that can be saved and shared. That text format is JSON.

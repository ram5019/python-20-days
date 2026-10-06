"""Day 18 example: classes and objects (OOP basics).

Run:  python3 learning-path/examples/day18_oop.py
"""

# BLOCK 1: the problem with plain dicts
student_dict = {"name": "Asha", "marks": [88, 92]}
# any function can modify it; no built-in behaviour attached

# BLOCK 2: a minimal class
class Student:
    def __init__(self, name):
        self.name = name              # attribute: data
        self.marks = []               # each student gets its own list

    def add_mark(self, mark):         # method: behaviour
        self.marks.append(mark)

    def average(self):
        if not self.marks:
            return 0
        return sum(self.marks) / len(self.marks)

# BLOCK 3: create objects (instances)
asha = Student("Asha")
ravi = Student("Ravi")

asha.add_mark(88)
asha.add_mark(92)
ravi.add_mark(70)

print(asha.name, asha.marks)          # Asha [88, 92]
print(asha.average())                 # 90.0
print(ravi.average())                 # 70.0  (independent of asha)

# BLOCK 4: __str__ controls how an object prints
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"'{self.title}' by {self.author}"

b = Book("Dune", "Frank Herbert")
print(b)                              # 'Dune' by Frank Herbert

# BLOCK 5: an object that protects its own rules
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

acct = BankAccount("Ram", 100)
acct.deposit(50)
acct.withdraw(30)
print(acct.balance)                   # 120
try:
    acct.withdraw(1000)
except ValueError as e:
    print("Error:", e)

# BLOCK 6: inheritance (a specialised class)
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):                    # Dog IS an Animal
    def speak(self):                  # override
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

for pet in [Dog("Rex"), Cat("Tom"), Animal("Generic")]:
    print(pet.name, "says", pet.speak())

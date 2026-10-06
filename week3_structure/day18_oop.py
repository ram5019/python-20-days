class Student:
    def __init__(s,n,m): s.n, s.m = n, m
    def grade(s): return "A" if s.m>=90 else "B" if s.m>=60 else "C"
print(Student("Ravi",85).grade())

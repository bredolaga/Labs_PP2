class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
s1 = Student("Zhanelya", 18)
print(s1.name)
print(s1.age)

class Person:
    def __init__(self, name, age="None"):
        self.name = name
        self.age = age
p1 = Person("Zhanelya")
p2 = Person ("Anna", 22)
print(p1.name, p1.age)
print(p2.name, p2.age)

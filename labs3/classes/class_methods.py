class Person:
  def __init__(self, name):
    self.name = name
  def greet(self):
    print("Hello, my name is " + self.name)
p1 = Person("Anvar")
p1.greet()

class Student:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def greet(self):
    self.age += 1
    return f"{self.name} is {self.age} years old"
s1 = Student("Ivan", 17)
print(s1.greet())

class People:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def __str__(self):
    return f"Name is {self.name} and age is {self.age}"
p2 = People("Ivan", 17)
print(p2)

class Person:
  def __init__(self, name):
    self.name = name
  def greet(self):
    print("Hello!")
p1 = Person("Anvar")
del Person.greet

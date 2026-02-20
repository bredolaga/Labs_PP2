class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
s1 = Student("Ivan", 18)
print(s1.name)
print(s1.age)

class Person:
  def __init__(self, name):
    self.name = name

  def printname(self):
    print(self.name)

p1 = Person("Tobias")
p2 = Person("Linus")

p1.printname()
p2.printname()


class Data:
   def __init__(self, name, age, school):
      self.name = name
      self.age = age
      self.school = school
   def met(self):
     print(f"{self.school} {self.age} {self.name}")
d1 = Data("Ivan", 18, "SITE")
d1.met()

class Lol:
   def __init__(self, name):
      self.name = name
   def greet(self):
      return "Hello, " + self.name
   def greeeet(self):
      mess = self.greet()
      print(mess + ", welcome")
n1 = Lol("Ivan")
n1.greeeet()

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Tobias", 25)
print(p1.age)
p1.age = 26
print(p1.age)

class Person:
  lastname = ""
  def __init__(self, name):
    self.name = name
p1 = Person("Linus")
p2 = Person("Emil")
Person.lastname = "Refsnes"
print(p1.lastname)
print(p2.lastname)

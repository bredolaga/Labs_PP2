class Person:
  def __init__(self, name, age):
    self.firstname = name
    self.age = age
  def printname(self):
    print(self.firstname, self.age)
x = Person("Ivan", 17)
x.printname()

class Student(Person):
    pass
x = Student("Mike", "Olsen")
x.printname()

class Student(Person):
    def __init__(self, name, age):
        Person.__init__(self, name, age)

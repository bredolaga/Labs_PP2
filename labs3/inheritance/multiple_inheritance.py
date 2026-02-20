class Person:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print("My name is", self.name)


class Student:
    def study(self):
        print("I am studying")


class WorkingStudent(Person, Student):
    def work(self):
        print("I am working")

x = WorkingStudent("Ivan")
x.introduce()
x.study()
x.work()

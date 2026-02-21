def names_func(*students):
    print("The smartest student is " + students[0]) 
names_func("Zhanelya", "Ivan", "Maksat")

def func(**data): 
    print(data["name"] + ", her age " + data["age"])
func(name = "Milana", age = "18")

def union(name, *education, **other):
    print("Name: ", name)
    print("Education: ", education)
    print("Other:, ", other)
union("Milana", "Average", "Higher", age = 30, city = "Almaty")

def function(a, b, c):
    return a + b + c
number = [5, 10, 15]
result = function(*number)
print(result)

def fun(name, surname):
    print("Hello,", name, surname)
person = {"name": "Ivan", "surname": "Sokolovskiy"}
fun(**person)

    

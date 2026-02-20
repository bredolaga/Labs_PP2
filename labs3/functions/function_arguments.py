def func(user = "guest"): 
    print("Hello, " + user)
func("Ivan")
func()

def function(name, age):
    print("My name is "+ name)
    print("I am " + name + " and I am " + age)
function("Ivan", "17")

def fn(schools): 
    for sc in schools:
        print(sc)
my_schools = ["SITE", "SEPI", "SCE"]
fn(my_schools)

def myfn(data): 
    print("School", data["school"])
    print("Year", data["year"])
my_data = {"name": "Ivan", "school": "SITE", "year": "2025"}
myfn(my_data)

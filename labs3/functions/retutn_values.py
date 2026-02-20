def sq(a, b):
    return a*a + b*b
print(sq(2, 3))

def func():
    return["SITE", "SEPI", 'SCE']
schools = func()
print(schools[1])

def myfn(name, /):
    print("Hello", name)
myfn("Ivan")   

def my_function(*, name):
  print("Hello", name)
my_function(name = "Ivan")

def fnc(a, b, /, *, c, d):
  return a + b + c + d
result = fnc(5, 10, c = 15, d = 20)
print(result)

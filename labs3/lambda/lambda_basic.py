x = lambda a : a + 10 
print(x(5))

add10 = lambda a: a + 10
print(add10(5)) 

multiply = lambda x, y: x * y
print(multiply(3, 4)) 

def myfunc(n):
  return lambda a : a * n
mydoubler = myfunc(2)
print(mydoubler(11))

func = lambda a, b: a*b
print(func(3,4))

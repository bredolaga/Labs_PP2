from functools import reduce as d
import operator
a = [1,2,3,4,5]
c = d(lambda x,y: x*y,a)
b = d(lambda x,y : x if x > y else y,a)
a = d(lambda x ,y : x+y ,a)
print(f" the sum is {a}")
print(f" the largest number is {b}")
print(f" the factorial is {c}")
example = ( d(operator.add,["Cat","Dog","Crow","Cheetah"]))
print(example)
a = [1,2,3,4,5]
a = map( lambda x : x*x , a) 
print(list(a))
a = [1,2,3,4,5] 
a = filter(lambda x:x%2,a)
print(list(a))
a = [1,2,3,4,5]
a = list(filter(lambda x : x%2 == 0 , a))
print(a)

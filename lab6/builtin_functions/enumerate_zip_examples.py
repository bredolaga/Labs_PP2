a = ["Jeff","Michel","Tyrell","Philip"]
b = [34,20,29,60]
c = ["software_engineer","staff","CTO","CEO"]
for x in zip(a,b,c): 
    print(x,end=' ')
a = sorted( a, key = len )
print()
for x in enumerate(a): 
    print(x,end=" ")

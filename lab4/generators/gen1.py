def square_generator(n):
    for i in range(n + 1):
        yield i * i

for value in square_generator(5):
    print(value)

numbers = [1, 2, 3, 4, 5, 6, 7, 8] 
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

number = [10, 20, 30, 40, 50]
big = list(filter(lambda x: x >= 40, number))
print(big)

numb = [80, 40, 20, 60]
small = list(filter(lambda x: x < 80, numb))
print(small)

nb = [10, 11, 12, 13, 14, 15]
even = list(filter(lambda x: x % 2 ==0, nb))
print(even)

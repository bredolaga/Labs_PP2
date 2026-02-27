def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter a number: "))
nums = even_numbers(n)
for i in nums:
    print(i, end = ",")

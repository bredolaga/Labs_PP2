students = [("Emil", 25), ("Ivan", 17), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

schools = [("SEPI", "700"), ("SITE", "1100"), ("SCE", "60")]
amount_of_student = sorted(schools, key=lambda x: int(x[1]))
print(amount_of_student)

numbers = [3, 10, 6, 17, 92, 5]
sorted_numbers = sorted(numbers, key=lambda x: x)
print(sorted_numbers)

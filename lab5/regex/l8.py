import re

text = input()
print(re.split(r"(?=[A-Z])", text))

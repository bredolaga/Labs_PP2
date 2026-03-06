import re

text = input()
print(re.findall(r"[A-Z][a-z]+", text))

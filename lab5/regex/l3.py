import re

text = input()
print(re.findall(r"[a-z]+_[a-z]+", text))

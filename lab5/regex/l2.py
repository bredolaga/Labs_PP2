import re

text = input()
print(bool(re.search(r"ab{2,3}", text)))

import re

text = input()
print(bool(re.search(r"ab*", text)))

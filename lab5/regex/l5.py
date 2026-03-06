import re

text = input()
print(bool(re.search(r"a.*b", text)))

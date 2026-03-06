import re

text = input()
print(re.sub(r"([A-Z])", r"_\1", text).lower())

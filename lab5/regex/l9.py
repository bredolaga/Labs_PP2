import re

text = input()
print(re.sub(r"([A-Z])", r" \1", text).strip())

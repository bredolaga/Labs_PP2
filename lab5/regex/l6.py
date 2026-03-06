import re

text = input()
print(re.sub(r"[ ,.]", ":", text))

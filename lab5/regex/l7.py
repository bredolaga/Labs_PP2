import re

text = input()

def func(match):
    return match.group(1).upper()

print(re.sub(r"_([a-z])", func, text))

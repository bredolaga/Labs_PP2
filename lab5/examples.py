import re

text = "My phone is 12345 and my code is 678."

match = re.search(r"\d+", text)
print(match.group())

numbers = re.findall(r"\d+", text)
print(numbers)

parts = re.split(r"\s+", "one   two  three")
print(parts)

result = re.sub(r"\d+", "NUMBER", text)
print(result)

m = re.match(r"My", text)
print(m.group() if m else "No match")

print(re.fullmatch(r"\d+", "12345"))
print(re.fullmatch(r"\d+", "123a45"))

pattern = re.compile(r"\b\w+\b")
words = pattern.findall("Hello world 123")
print(words)

print(re.findall(r"a.c", "abc axc a-c"))

print(re.findall(r"\d{2,4}", "1 12 123 12345"))

print(re.findall(r"\d", "a1b2c3"))
print(re.findall(r"\w+", "hello_123 !!!"))
print(re.findall(r"\s", "a b\tc"))

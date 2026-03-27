with open("text.txt", "w") as text:
    text.write("new line")
with open("text.txt", "a") as text:
    text.write("new line2\n")

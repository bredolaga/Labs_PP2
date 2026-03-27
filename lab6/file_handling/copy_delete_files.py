import shutil
import os

# copy
shutil.copy("text.txt", "copy.txt")

# read
with open("copy.txt") as f:
    print(f.read())

# delete
os.remove("copy.txt")

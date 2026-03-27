import os 
import shutil
if not os.path.exists("new_folder"):
    os.mkdir("new_folder")
    os.mkdir("new_folder/nested_folder")
with open("new_file.txt" , 'x' ) as f:
    pass 
with open("new_file.txt" , 'a' ) as f: 
    f.write("This is a new file inside of a new directory")
print( os.getcwd() )
shutil.move('new_file.txt',"/home/morjinka/Projects/pp2/pp2-2/Labs_PP2/lab6/directory_management/")
with open("new_file2.txt" , 'x' ) as f:
    pass 
shutil.move("new_file2.txt","nested_folder/")

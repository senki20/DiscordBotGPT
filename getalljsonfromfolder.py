import os

def find():
    files=[]
    for file in os.listdir("./History"):
        files.append(file)
    print(files)
    return files
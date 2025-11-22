'''
see these three files for calling txt files as a module 
you can make file helper modules.
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/file_tools_use.py
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/file_tools.py
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/notes.txt



'''
# to create a file
with open("Nov2025/Lessons/log.txt", "w") as f:
    f.write("Hello file!\n")
    f.write("Line #2\n")

# to append a file
with open("Nov2025/Lessons/log.txt", "a") as f:
    f.write("Appended line\n")
    
# to read the file
with open("Nov2025/Lessons/log.txt", "r") as f:
    data = f.read()
    print(data)

# read file line by line
with open("Nov2025/Lessons/log.txt") as f:
    for line in f:
        print("LINE:", line.strip())

# make file helper modules
# filename='/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Lessons/filePractice_1.txt'
filename='/Nov2025/Lessons/filePractice_1.txt'
text='this is my trial file'
def save(filename, text):
    with open(filename, "a") as f:
        f.write(text + "\n")

def load(filename):
    with open(filename) as f:
        return f.read()



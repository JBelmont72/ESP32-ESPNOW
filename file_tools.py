'''
'''
filename1='/file_tools_use.txt'

def save1(filename, text):
    with open(filename, "a") as f:
        f.write(text + "\n")
    with open(filename, "a") as f:
        f.write("Appended line\n")

def save(filename1, text):
    # to create a file
    with open(filename1, "w") as f:
        f.write("Hello file!\n")
        f.write("Line #2\n")
    with open(filename1, "a") as f:
        f.write(text + "\n")


def load(filename):
    with open(filename) as f:
        return f.read()

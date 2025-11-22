'''uses math_tools.py
'''
import math_tools

print("Triple of 3 is:", math_tools.triple(3))
print("Square of 4 is:", math_tools.square(4))
print("Cube of 2 is:", math_tools.cube(2))
try:
     while True:
         text=str(input('text entered'))
         print('')
         print(math_tools.shout(text))
         print(math_tools.whisper(text))
         print(f'I said {math_tools.whisper(text)}')
except KeyboardInterrupt:
    print('exit')
    
    
# import file_tools

# file_tools.save("notes.txt", "My first saved note!")
# print(file_tools.load("notes.txt"))
# import file_tools
import filePractice
filePractice.save("Nov2025/Lessons/notes.txt", "My first saved note!")
print(filePractice.load("Nov2025/Lessons/notes.txt"))

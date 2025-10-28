# program_two.py slow blinking on board led for using main.py that is controllable
# program_one.py is the companion program  
'''
>>> import os
>>> os.listdir()
['Program_1.py']
>>> os.rename('Program_1.py' ,  'Prog_1.py')
>>> os.listdir()
['Prog_1.py']
>>> os.getcwd()
'/'
>>> os.remove('Prog_1.py')
>>> os.mkdir('lib')
>>> os.remove('lib')
>>> os.chdir('my_folder')
>>> os.getcwd()
'/my_folder'

'''

import utime
import sys
from machine import Pin,Timer
#led =Pin("LED",Pin.OUT)
led=Pin(12,Pin.OUT)
rled=Pin(13,Pin.OUT)
print("Program Two is running!")
tim=Timer(3)
def tick(timer):
    global led, rled
    led.toggle()
try:
    for i in range(10):
        print(f"Program Two: {i}")
        led.toggle()
        rled.toggle()
        utime.sleep(0.4)
    #tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
    print("Program One finished.")
except KeyboardInterrupt:
    print('exiting')
    sys.exit()


'''
from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
'''
'''

import time
from machine import Pin

led = Pin(12, Pin.OUT)
rled = Pin(13, Pin.OUT)

print("Program Two is running!")

for i in range(10):
    print(f"Program Two: {i}")
    led.value(not led.value())
    rled.value(not rled.value())
    time.sleep(0.4)

print("Program Two finished.")
'''
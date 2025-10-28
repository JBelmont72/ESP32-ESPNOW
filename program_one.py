# program 1 for using main.py that is controllable
# program_one.py 
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
'''
import utime		## pico version
import sys
from machine import Pin,Timer
#led =Pin("LED",Pin.OUT)
led=Pin(12,Pin.OUT)
rled=Pin(13,Pin.OUT)
print("Program One is running!")
tim=Timer()
def tick(timer):
    global led, rled
    led.toggle()
try:
    for i in range(6):
        print(f"Program One: {i}")
        led.toggle()
        rled.toggle()
        utime.sleep(1)
    #tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
    print("Program One finished.")
except KeyboardInterrupt:
    print('exiting')
    sys.exit()
'''
'''
from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
'''

import time
import sys
from machine import Pin, Timer

# ====== Pin Configuration ======
# ESP32 boards don’t have a built-in "LED" name like the Pico.
# You can use GPIO2 or GPIO12 for an onboard LED (if present),
# or connect external LEDs with resistors.
led = Pin(12, Pin.OUT)   # main LED
rled = Pin(13, Pin.OUT)  # secondary LED

print("ESP32 Program One is running!")

# ====== Timer Setup ======
tim = Timer(0)  # use timer ID 0

def tick(timer):
    """Toggle LED periodically if enabled."""
    led.toggle()

try:
    for i in range(6):
        print(f"Program One: {i}")
        led.toggle()
        rled.toggle()
        time.sleep(1)

    # Example of enabling the timer (uncomment to use)
    # tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

    print("Program One finished.")

except KeyboardInterrupt:
    print("Exiting program.")
    tim.deinit()  # stop the timer if running
    sys.exit()


'''
import time
from machine import Pin

led = Pin(12, Pin.OUT)
rled = Pin(13, Pin.OUT)

print("Program One is running!")

for i in range(6):
    print(f"Program One: {i}")
    led.value(not led.value())
    rled.value(not rled.value())
    time.sleep(1)

print("Program One finished.")
'''


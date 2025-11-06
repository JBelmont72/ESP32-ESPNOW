from machine import Pin
from time import sleep
import sys
pin=33 
But=Pin(pin,Pin.IN, Pin.PULL_DOWN)
try:
    while True:
        butVal =But.value()
        print(butVal)
        sleep(.3)
except KeyboardInterrupt:
    print('exit')
    sys.exit()



import sys
import uasyncio as asyncio
from machine import Pin, ADC
import sys
from time import sleep
pin=22
gLed=Pin(pin,Pin.OUT)
gLed.value(0)
ypin=23
yLed=Pin(ypin,Pin.OUT)
yLed.value(1)
try:
    while True:
        yLed.value(1)
        gLed.value(1)
        sleep(.5)    
        yLed.value(0)
        gLed.value(0)
        sleep(.5)    
except KeyboardInterrupt:
    print('exit')
    sys.exit()
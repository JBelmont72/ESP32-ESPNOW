'''

only for rp2040 with threads
'''
from machine import Pin
import utime
import _thread

button = Pin(4, Pin.IN)
led = Pin(23, Pin.OUT)

global button_pressed
button_pressed = False

def read_button():
    global button_pressed
    while True:
        if button.value() == 1:
            button_pressed = not button_pressed
            utime.sleep(0.5)

_thread.start_new_thread(read_button, ())

while True:
    if button_pressed == True:
        led.value(1)
    else:
        led.value(0)
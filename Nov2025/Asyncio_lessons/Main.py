# main.py using button press on GPIO 4  
 
from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import sys
import Blink_LED

# Configuration 
BUTTON_PIN = 4
TIMEOUT_MS = 1000  # 1 second

# Setup
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

# Startup message
print("Waiting for button press...")

start = ticks_ms()
while ticks_diff(ticks_ms(), start) < TIMEOUT_MS:
    if  button.value():  # Active-high: pressed
        print("Button pressed — running Blink_LED")
        Blink_LED.Blink_LED()
        break
    sleep(1.0)

print("No button press — exiting safely")
sys.exit()

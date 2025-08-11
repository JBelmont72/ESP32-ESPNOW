def main():
    print("Hello from micropython-esp32-esp8266!")


if __name__ == "__main__":
    main()


'''
# main.py using button press on GPIO 4 

from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import sys
import Blink_LED

# Configuration 
BUTTON_PIN = 4 #  to GROUND SO Pin.PULL_UP =1 when not pressed
TIMEOUT_MS = 1000  # 1 second

# Setup
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
ON_BOARD_PIN = 2
led_pin = Pin(ON_BOARD_PIN, Pin.OUT)

butVal=button.value()
print(f'butVal: {butVal}')
# Startup message
print("Waiting for button press...")
i=0
start = ticks_ms()
while ticks_diff(ticks_ms(), start) < TIMEOUT_MS:
    if not button.value():  # Active-low: pressed
        print("Button pressed — running Blink_LED")
        Blink_LED.main()
        for i in range(0,5,1):
            led_pin.value(not led_pin.value())
            sleep_ms(400)
            
        break
    sleep(0.05)

print("No button press — exiting safely")
sys.exit()

'''
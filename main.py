#
# cha t with excellent inof https://www.google.com/search?aep=28&udm=50&csuir=1&mstk=AUtExfAhlGsT8m2SxdQNDZld8S3xPp1H-rMafsi-ER6OXIt8lFx3ahT2PiPpLOyTb_J_SkqWxRPniMAY0k8ZJWU8G1Mk-0rHqqjv5eV4ZzAJI-NMYPG3LTSzsuYysnfGTG8xJTXb7OdncTu_VaAL7PFx3_N2DNBr5fblN1U&q=main.py+pico+that+does+not+continuously+import+another+program+but+gies+tio+except%3A+pass+unless+a+button+is+pressed.+short+press+for+one+program+and+ling+press+fir+a+second+program+to+be+imported+button+with+a+long+press+of+4+seconds&oq=&gs_lcrp=EgZjaHJvbWUqDwgCECMYJxjqAhjwBRieBjIPCAAQIxgnGOoCGIAEGIoFMgkIARAjGCcY6gIyDwgCECMYJxjqAhjwBRieBjIPCAMQIxgnGOoCGIAEGIoFMg8IBBAjGCcY6gIYgAQYigUyDwgFECMYJxjqAhjwBRieBjIVCAYQABhCGLQCGOoCGNsFGPAFGJ4GMhUIBxAAGEIYtAIY6gIY2wUY8AUYngbSAQsyNjMyMjA4ajBqN6gCCLACAfEF5HedkkP7ppHxBeR3nZJD-6aR&sourceid=chrome&ie=UTF-8&mtid=qCjtaMOZIN2h5NoP3qzYiA4
# 
# def main():
#     print("Hello from micropython-esp32-esp8266!")


# if __name__ == "__main__":
#     main()


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
'''
# main.py (Final Robust Version) 24 october 2025  will use with dfplayer and keypad
import machine
import utime

# Define button GPIO pin and duration thresholds
BUTTON_PIN = 15
LONG_PRESS_TIME_MS = 4000
DEBOUNCE_DELAY_MS = 50

# Setup the button pin with an internal pull-up resistor
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Global variables for state and timer
press_start_time = 0
debounce_timer = machine.Timer(-1)
press_handled = False

def run_program():
    """Import and run the correct program based on press duration."""
    global press_start_time
    
    # Calculate press duration
    press_duration = utime.ticks_diff(utime.ticks_ms(), press_start_time)
    press_start_time = 0 # Reset the timer
    
    if press_duration >= LONG_PRESS_TIME_MS:
        print("Long press detected. Importing program_two.")
        import program_two
    elif press_duration > DEBOUNCE_DELAY_MS:
        print("Short press detected. Importing program_one.")
        import program_one
        
    # After execution, perform a soft reboot
    print("Soft rebooting...")
    machine.reset()

def button_interrupt_handler(pin):
    """ISR for button state change."""
    global press_start_time, press_handled
    
    if not pin.value():
        # Button pressed
        if not press_handled:
            press_start_time = utime.ticks_ms()
            press_handled = True
    else:
        # Button released
        if press_handled:
            debounce_timer.init(period=DEBOUNCE_DELAY_MS, mode=machine.Timer.ONE_SHOT, callback=lambda t: run_program())
            press_handled = False


# Configure the interrupt
button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=button_interrupt_handler)

print("Pico is ready. Press and hold the button for 4 seconds for program two.")
print("Press the button briefly for program one.")

# Main program loop - mostly idle
while True:
    utime.sleep(1)

'''
'''25 october 2025 this works on prgram_one.py and program_two.py in obsidian 'Main' along with main_long_short.py and main_template.py

https://chatgpt.com/c/68fd3220-3c48-8332-b5c5-bb603338dde7
if button is to ground will need to flip the logic
if not val and not pressed:   # pressed

elif val and pressed:         # released


for button to vcc:  DOWN HOT Zero! for button
from machine import Pin
import time

button = Pin(26, Pin.IN, Pin.PULL_DOWN)
while True:
    print(button.value())
    time.sleep(0.2)
0 when not pressed. 1 when pressed

if connected to ground then Pin.PULL_UP
and 1 when not pressed and 0 when presed
'''

import machine
import utime
import sys

# === CONFIGURATION ===
BUTTON_PIN = 14            # active HIGH button to 3.3V
LONG_PRESS_TIME_MS = 4000  # 4 seconds threshold
DEBOUNCE_MS = 50

button = machine.Pin(BUTTON_PIN, machine.Pin.IN,machine.Pin.PULL_DOWN)  # no pull-up on GPIO26, Down Hot Zero!

press_start = None
press_end = None
pressed = False

print("\nPress the button to select a program...")
print("→ Short press = program_one.py")
print("→ Long press  = program_two.py\n")

while True:
    val = button.value()

    if val and not pressed:  # button just pressed (1)
        pressed = True
        press_start = utime.ticks_ms()

    elif not val and pressed:  # button just released (0)
        press_end = utime.ticks_ms()
        pressed = False

        press_duration = utime.ticks_diff(press_end, press_start)
        press_start = None
        press_end = None

        # Handle the press type
        if press_duration < DEBOUNCE_MS:
            print("Ignored noise press.")
        elif press_duration < LONG_PRESS_TIME_MS:
            print(f"Short press detected ({press_duration/1000:.2f}s).")
            print("\nRunning program_one.py ...")
            import program_one
        else:
            print(f"Long press detected ({press_duration/1000:.2f}s).")
            print("\nRunning program_two.py ...")
            import program_two

        print("Returning to selector in 3 s...\n")
        utime.sleep(3)
        machine.reset()

    utime.sleep_ms(20)


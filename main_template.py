''' in obsidian as file 'Main' also in micropython_programs,
main_template.py
my main.py i will save as main_template.py with flashing onboard LED and pushbutton on pin 4 butVal 1 when not pushed


github location /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Main.py
chat with excellent info https://www.google.com/search?aep=28&udm=50&csuir=1&mstk=AUtExfAhlGsT8m2SxdQNDZld8S3xPp1H-rMafsi-ER6OXIt8lFx3ahT2PiPpLOyTb_J_SkqWxRPniMAY0k8ZJWU8G1Mk-0rHqqjv5eV4ZzAJI-NMYPG3LTSzsuYysnfGTG8xJTXb7OdncTu_VaAL7PFx3_N2DNBr5fblN1U&q=main.py+pico+that+does+not+continuously+import+another+program+but+gies+tio+except%3A+pass+unless+a+button+is+pressed.+short+press+for+one+program+and+ling+press+fir+a+second+program+to+be+imported+button+with+a+long+press+of+4+seconds&oq=&gs_lcrp=EgZjaHJvbWUqDwgCECMYJxjqAhjwBRieBjIPCAAQIxgnGOoCGIAEGIoFMgkIARAjGCcY6gIyDwgCECMYJxjqAhjwBRieBjIPCAMQIxgnGOoCGIAEGIoFMg8IBBAjGCcY6gIYgAQYigUyDwgFECMYJxjqAhjwBRieBjIVCAYQABhCGLQCGOoCGNsFGPAFGJ4GMhUIBxAAGEIYtAIY6gIY2wUY8AUYngbSAQsyNjMyMjA4ajBqN6gCCLACAfEF5HedkkP7ppHxBeR3nZJD-6aR&sourceid=chrome&ie=UTF-8&mtid=qCjtaMOZIN2h5NoP3qzYiA4
'''
# main.py using button press on GPIO 4 
'''
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
# github location /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/espnow/Kuzchie_espnow/main.py
# main.py — Role switcher for ESP32 ESP-NOW for both receiver.y and transmitter.py
from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import sys

import transmitter
import receiver

# ===== CONFIG =====
BUTTON_PIN = 4         # Button to GND, uses internal pull-up
BUTTON_TIMEOUT_MS = 2000  # Wait 2s for press
# ==================

def choose_role():
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

    print("Press button within 2 seconds to run as TRANSMITTER...")
    start = ticks_ms()
    while ticks_diff(ticks_ms(), start) < BUTTON_TIMEOUT_MS:
        if not button.value():  # Button pressed (active low)
            return "transmitter"
        sleep(0.05)
    return "receiver"

def main():
    role = choose_role()
    print(f"Selected role: {role.upper()}")

    if role == "transmitter":
        transmitter.main()
    else:
        receiver.main()

if __name__ == "__main__":
    main()
'''

'''
# def main():
#     print("Hello from micropython-esp32-esp8266!")


# if __name__ == "__main__":
#     main()


'''
# main.py using button press on GPIO 4 
'''
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
https://www.google.com/search?aep=28&udm=50&csuir=1&mstk=AUtExfAhlGsT8m2SxdQNDZld8S3xPp1H-rMafsi-ER6OXIt8lFx3ahT2PiPpLOyTb_J_SkqWxRPniMAY0k8ZJWU8G1Mk-0rHqqjv5eV4ZzAJI-NMYPG3LTSzsuYysnfGTG8xJTXb7OdncTu_VaAL7PFx3_N2DNBr5fblN1U&q=main.py+pico+that+does+not+continuously+import+another+program+but+gies+tio+except%3A+pass+unless+a+button+is+pressed.+short+press+for+one+program+and+ling+press+fir+a+second+program+to+be+imported+button+with+a+long+press+of+4+seconds&oq=&gs_lcrp=EgZjaHJvbWUqDwgCECMYJxjqAhjwBRieBjIPCAAQIxgnGOoCGIAEGIoFMgkIARAjGCcY6gIyDwgCECMYJxjqAhjwBRieBjIPCAMQIxgnGOoCGIAEGIoFMg8IBBAjGCcY6gIYgAQYigUyDwgFECMYJxjqAhjwBRieBjIVCAYQABhCGLQCGOoCGNsFGPAFGJ4GMhUIBxAAGEIYtAIY6gIY2wUY8AUYngbSAQsyNjMyMjA4ajBqN6gCCLACAfEF5HedkkP7ppHxBeR3nZJD-6aR&sourceid=chrome&ie=UTF-8&mtid=qCjtaMOZIN2h5NoP3qzYiA4
Timer based debouncing: more reliable because the interrupt handler is kept extremely simple, and all the timing logic is managed by a hardware timer, which is less prone to missing events or race conditions
Below works great -version with timer
# /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Main.py
# main.py (Final Robust Version) 24 october 2025  will use with dfplayer and keypad
'''
import machine
import utime

#onboard_led = machine.Pin("LED", machine.Pin.OUT) # for Pico
onboard_led = machine.Pin(2, machine.Pin.OUT)	# for esp32
def button_interrupt_handler(pin):
    onboard_led.toggle()



# Define button GPIO pin and duration thresholds
BUTTON_PIN = 26
LONG_PRESS_TIME_MS = 4000
DEBOUNCE_DELAY_MS = 50

# Setup the button pin with an internal pull-down resistor, connect to Hot, the resting value is 0, down-hot-zero!! 
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Global variables for state and timer
press_start_time = 0
#debounce_timer = machine.Timer(-1)
debounce_timer = machine.Timer(3)
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
    onboard_led.toggle()
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
butVal = button.value()
print('butVal:  ',butVal)

# Main program loop - mostly idle
while True:
    utime.sleep(1)


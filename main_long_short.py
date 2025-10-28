'''
This is in ESP32-NOW, MicropythonPrograms and obsidian tag #main   File 'Main'
robust main.py
chat with excellent discussion and linkk https://www.google.com/search?aep=28&udm=50&csuir=1&mstk=AUtExfAhlGsT8m2SxdQNDZld8S3xPp1H-rMafsi-ER6OXIt8lFx3ahT2PiPpLOyTb_J_SkqWxRPniMAY0k8ZJWU8G1Mk-0rHqqjv5eV4ZzAJI-NMYPG3LTSzsuYysnfGTG8xJTXb7OdncTu_VaAL7PFx3_N2DNBr5fblN1U&q=main.py+pico+that+does+not+continuously+import+another+program+but+gies+tio+except%3A+pass+unless+a+button+is+pressed.+short+press+for+one+program+and+ling+press+fir+a+second+program+to+be+imported+button+with+a+long+press+of+4+seconds&oq=&gs_lcrp=EgZjaHJvbWUqDwgCECMYJxjqAhjwBRieBjIPCAAQIxgnGOoCGIAEGIoFMgkIARAjGCcY6gIyDwgCECMYJxjqAhjwBRieBjIPCAMQIxgnGOoCGIAEGIoFMg8IBBAjGCcY6gIYgAQYigUyDwgFECMYJxjqAhjwBRieBjIVCAYQABhCGLQCGOoCGNsFGPAFGJ4GMhUIBxAAGEIYtAIY6gIY2wUY8AUYngbSAQsyNjMyMjA4ajBqN6gCCLACAfEF5HedkkP7ppHxBeR3nZJD-6aR&sourceid=chrome&ie=UTF-8&mtid=qCjtaMOZIN2h5NoP3qzYiA4

https://www.google.com/search?aep=28&udm=50&csuir=1&mstk=AUtExfAhlGsT8m2SxdQNDZld8S3xPp1H-rMafsi-ER6OXIt8lFx3ahT2PiPpLOyTb_J_SkqWxRPniMAY0k8ZJWU8G1Mk-0rHqqjv5eV4ZzAJI-NMYPG3LTSzsuYysnfGTG8xJTXb7OdncTu_VaAL7PFx3_N2DNBr5fblN1U&q=main.py+pico+that+does+not+continuously+import+another+program+but+gies+tio+except%3A+pass+unless+a+button+is+pressed.+short+press+for+one+program+and+ling+press+fir+a+second+program+to+be+imported+button+with+a+long+press+of+4+seconds&oq=&gs_lcrp=EgZjaHJvbWUqDwgCECMYJxjqAhjwBRieBjIPCAAQIxgnGOoCGIAEGIoFMgkIARAjGCcY6gIyDwgCECMYJxjqAhjwBRieBjIPCAMQIxgnGOoCGIAEGIoFMg8IBBAjGCcY6gIYgAQYigUyDwgFECMYJxjqAhjwBRieBjIVCAYQABhCGLQCGOoCGNsFGPAFGJ4GMhUIBxAAGEIYtAIY6gIY2wUY8AUYngbSAQsyNjMyMjA4ajBqN6gCCLACAfEF5HedkkP7ppHxBeR3nZJD-6aR&sourceid=chrome&ie=UTF-8&mtid=qCjtaMOZIN2h5NoP3qzYiA4
'''


# main.py (Final Robust Version) 24 october 2025  will use with dfplayer and keypad

'''25 october 2025 this works on prgram_one.py and program_two.py

https://chatgpt.com/c/68fd3220-3c48-8332-b5c5-bb603338dde7
if button is to ground will need to flip the logic
if not val and not pressed:   # pressed

elif val and pressed:         # released


for button to vcc:
from machine import Pin
import time

button = Pin(26, Pin.IN, Pin.PULL_DOWN)
while True:
    print(button.value())
    time.sleep(0.2)
But to VCC: 0 when not pressed. 1 when pressed DOWN HOT Zero

if connected to ground then Pin.PULL_UP
and 1 when not pressed and 0 when presed
'''
'''
## current main.py 28 Oct 2025 no interrupt
import machine
import utime
import sys

# === CONFIGURATION ===
BUTTON_PIN = 26            # active HIGH button to 3.3V
LONG_PRESS_TIME_MS = 4000  # 4 seconds threshold
DEBOUNCE_MS = 50

button = machine.Pin(BUTTON_PIN, machine.Pin.IN,machine.Pin.PULL_DOWN)  # pull down on esp32, DOWN, HOT,Zero

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


'''

'''
## this works with interrupt and timer

import machine
import utime
import sys
# Define button GPIO pin and duration thresholds
BUTTON_PIN = 26
LONG_PRESS_TIME_MS = 4000
DEBOUNCE_DELAY_MS = 50

# Setup the button pin with an internal pull-up resistor
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Global variables for state and timer
press_start_time = 0
debounce_timer = machine.Timer(1)
press_handled = False
butVal=button.value()
print(butVal)
print("ESP32 is ready. Press and hold the button for 4 seconds for program two.")
print("Press the button briefly for program one.")

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


# Main program loop - mostly idle
while True:
    utime.sleep(1)
'''

import machine
import utime
#import sys

# Define button GPIO pin and duration thresholds
BUTTON_PIN = 26  # change if needed
LONG_PRESS_TIME_MS = 4000
DEBOUNCE_DELAY_MS = 50

# Setup the button pin with internal pull-up
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Global state
press_start_time = 0
debounce_timer = machine.Timer(3)
press_handled = False

print(button.value())
print("ESP32 is ready. Press and hold for 4s for program_two.py, short press for program_one.py.")

def run_program():
    """Import and run the correct program based on press duration."""
    global press_start_time

    press_duration = utime.ticks_diff(utime.ticks_ms(), press_start_time)
    press_start_time = 0

    try:
        if press_duration >= LONG_PRESS_TIME_MS:
            print("Long press detected → running program_two.py")
            import program_two
            program_two  # ensure it runs top-level code
        elif press_duration > DEBOUNCE_DELAY_MS:
            print("Short press detected → running program_one.py")
            import program_one
            program_one
        else:
            print("Ignored noise press")

        # Wait a moment before rebooting
        print("Program finished. Rebooting in 3 seconds...")
        utime.sleep(3)

    except Exception as e:
        print("Error running selected program:", e)

    finally:
        machine.reset()

def button_interrupt_handler(pin):
    """ISR for button press/release."""
    global press_start_time, press_handled
    if pin.value():	# for when button hot, zero, DOWN
#    if not pin.value():  # pressed (active LOW) # for when button to ground, up,1
        if not press_handled:	
            press_start_time = utime.ticks_ms()
            press_handled = True
    else:  # released
        if press_handled:
            debounce_timer.init(
                period=DEBOUNCE_DELAY_MS,
                mode=machine.Timer.ONE_SHOT,
                callback=lambda t: run_program()
            )
            press_handled = False

# Configure the interrupt
button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=button_interrupt_handler)

# Keep main running
while True:
    utime.sleep(1)


'''
this works great as well, button to ground

main short long button press  but on graound ,pin 4 works fine


from machine import Pin
import time
import sys

# ----------------------------
# Configuration
# ----------------------------
BUTTON_PIN = 26      # adjust for your wiring
LONG_PRESS_TIME = 2  # seconds
DEBOUNCE_TIME = 0.15 # seconds

# ----------------------------
# Setup
# ----------------------------
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
press_start = None

def wait_for_press():
    """Wait for a button press and determine if it's short or long."""
    global press_start
    print("\nPress the button to select a program...")
    print("→ Short press = program_one.py")
    print("→ Long press  = program_two.py")
    print("(Or do nothing to skip.)")

    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 6000:  # wait up to 6 seconds
        if not button.value():  # pressed
            press_start = time.ticks_ms()
            while not button.value():
                time.sleep(0.01)
            press_duration = time.ticks_diff(time.ticks_ms(), press_start) / 1000
            if press_duration >= LONG_PRESS_TIME:
                print(f"Long press detected ({press_duration:.2f}s).")
                return "long"
            elif press_duration >= DEBOUNCE_TIME:
                print(f"Short press detected ({press_duration:.2f}s).")
                return "short"
        time.sleep(0.05)
    print("No button press detected. Skipping program selection.")
    return None

def run_script(script_name):
    """Run another Python file."""
    try:
        print(f"\nRunning {script_name} ...")
        with open(script_name) as f:
            exec(f.read(), globals())
    except Exception as e:
        print(f"Error running {script_name}: {e}")
    finally:
        print(f"{script_name} finished.\n")

# ----------------------------
# Main control
# ----------------------------
choice = wait_for_press()

if choice == "short":
    run_script("program_one.py")
elif choice == "long":
    run_script("program_two.py")
else:
    print("No selection made. main.py exiting.\n")
    sys.exit()


'''
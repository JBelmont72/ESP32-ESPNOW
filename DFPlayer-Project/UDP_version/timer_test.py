'''

see main.py  and main.md for details of how the timer and button press work and irq.
note how the timer callback can either be a named function or a lambda function. 
### 1st simple program to illustrate the timer and the irq callback.   
'''
# from machine import Timer
# import utime

# # ---------- Callback that shows what the timer passes ----------
# def show_callback(timer_obj):
#     print("Callback fired! Timer object =", timer_obj)

# # ---------- Timer setup ----------
# t = Timer(1)

# print("Starting 1-second one-shot timer...")
# t.init(
#     period=6000,                 # 1 second
#     mode=Timer.ONE_SHOT,
#     callback=show_callback       #1 passes the timer object to the show_callback function##
#     #callback=lambda t: print("Lambda callback → timer:", t)  #2   
#     #callback = show_callback()  # no positional arguemtns  #`3 error`
# )

# # ---------- Keep alive ----------
# while True:
#     utime.sleep(0.1)
    
    
### 2d explanatory program to illustrate the timeing of the timer and the irq.
# ✅ **Button Timing Demonstration Program**

### 📌 Wiring
'''
* Button → **3.3V**
* Pin → **PULL_DOWN**
* Same setup as main.py program.
'''

import machine
import utime

BUTTON_PIN = 4
DEBOUNCE_MS = 50

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

press_start_time = 0
press_handled = False

debounce_timer = machine.Timer(4)

print("\n=== Button Timing Debug Demo ===\n")

# ----------------------------------------------------------
def debug_run_program():
    global press_start_time

    print("  [Timer fired] Debounce finished")

    press_duration = utime.ticks_diff(utime.ticks_ms(), press_start_time)
    print(f"  [Press duration] {press_duration} ms")

    # Reset for the next cycle
    press_start_time = 0
    print("  [Ready for next press]\n")


# ----------------------------------------------------------
def button_handler(pin):
    global press_start_time, press_handled

    if pin.value():  # Rising edge = button down
        print(">> Button PRESSED (rising edge)")
        if not press_handled:
            press_start_time = utime.ticks_ms()
            print(f"  [Start time recorded] {press_start_time} ms press_handled={press_handled}")
            press_handled = True

    else:            # Falling edge = button released
        print("<< Button RELEASED (falling edge) press_handled=", press_handled, ") ")

        if press_handled:
            print(f"  [Starting debounce timer: {DEBOUNCE_MS} ms]")
            debounce_timer.init(
                period=DEBOUNCE_MS,
                mode=machine.Timer.ONE_SHOT,
                callback=lambda t: debug_run_program()
            )
            press_handled = False


# ----------------------------------------------------------
button.irq(
    trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING,
    handler=button_handler
)

print("Press and release the button to see debug output...\n")

# Keep running
while True:
    utime.sleep(1)


'''
keypad_final.py
this eliminates ghost presses by using a count
Chat https://chatgpt.com/c/68c6e1a2-80ac-832e-9063-4c99fc53b034
'''


from machine import Pin
import time

# --- keypad setup (4x4 in your wiring) ---
rows = [Pin(r, Pin.OUT) for r in (14,27,26,25)]   # adjust GPIO pins
cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in (33,32,35,34)]

keys = [
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

last_key = None
last_time = 0
stable_count = 0
threshold = 3   # require 3 stable reads before confirming

def scan_keypad():
    global last_key, last_time, stable_count
    for i, row in enumerate(rows):
        row.value(1)                     # drive one row high
        for j, col in enumerate(cols):
            if col.value() == 1:
                key = keys[i][j]
                now = time.ticks_ms()

                if key == last_key:
                    stable_count += 1
                else:
                    stable_count = 0     # reset if different key seen
                    last_key = key
                    last_time = now

                if stable_count >= threshold:
                    stable_count = 0     # reset so we only trigger once
                    row.value(0)
                    return key
        row.value(0)
    return None


'''
import machine
import time

# Define keypad layout
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# GPIO pins
row_pins = [14,27,26,25]
col_pins = [33,32,35,34]

# Init rows/cols
rows = [machine.Pin(pin_num, machine.Pin.OUT) for pin_num in row_pins]
cols = [machine.Pin(pin_num, machine.Pin.IN, machine.Pin.PULL_DOWN) for pin_num in col_pins]

def scan_keypad():
    for i, row_pin in enumerate(rows):
        # Set all rows low
        for r in rows:
            r.value(0)
        # Drive current row high
        row_pin.value(1)

        for j, col_pin in enumerate(cols):
            if col_pin.value() == 1:
                # Debounce
                time.sleep_ms(20)
                if col_pin.value() == 1:
                    return keys[i][j]
    return None
'''
def main():
    last_key_pressed = None
    while True:
        pressed_key = scan_keypad()

        if pressed_key and pressed_key != last_key_pressed:
            print(f"Key Pressed: {pressed_key}")
            last_key_pressed = pressed_key
        elif not pressed_key and last_key_pressed:
            last_key_pressed = None

        time.sleep(0.05)  # shorter delay works fine

if __name__ == "__main__":
    main()

'''
from machine import Pin
import time

# Define rows and columns (adjust GPIO pins according to your wiring)
rows = [Pin(r, Pin.OUT) for r in (27, 26, 25, 33)]   # Row pins (OUTPUT)
cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in (37, 38, 35, 32)]  # Column pins (INPUT)

# Keypad mapping
keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

last_key = None
last_time = 0
stable_count = 0
threshold = 2  # Require 2 stable reads before confirming

def scan_keypad():
    global last_key, last_time, stable_count
    for i, row in enumerate(rows):
        row.value(1)                     # Drive this row high
        time.sleep(0.01)                 # Small delay for stabilization
        
        print(f"Scanning row {i}: HIGH")  # Debug statement
        
        for j, col in enumerate(cols):
            col_state = col.value()
            print(f"Column {j} state: {col_state}")  # Print the column state
            time.sleep(.5)
            if col_state == 1:            # If the column reads high
                key = keys[i][j]
                now = time.ticks_ms()

                if key == last_key:
                    stable_count += 1
                else:
                    stable_count = 0
                    last_key = key
                    last_time = now

                if stable_count >= threshold:
                    stable_count = 0
                    row.value(0)          # Turn off row before returning
                    print(f"Key Pressed: {key}")  # Output the detected key
                    return key
        row.value(0)                     # Turn off row after checking
    return None

# def main():
#     while True:
#         pressed_key = scan_keypad()

#         if pressed_key:
#             # Simply handling the printed output; main functionality in scan_keypad
#             time.sleep(0.1)  # Small delay to avoid multiple rapid detections

# if __name__ == "__main__":
#     main()




def test_buttons():
    for i, row in enumerate(rows):
        row.value(1)  # Drive this row high
        time.sleep(0.01)  # Small delay
        
        for j in range(4):  # Check all columns
            col_state = cols[j].value()
            print(f"Testing Row {i}, Column {j} state: {col_state}")
            
        row.value(0)  # Reset the row

def main():
    while True:
        test_buttons()
        time.sleep(1)  # Delay between tests for audience clarity

if __name__ == "__main__":
    main()
'''

# from machine import Pin
# import time

# # Define rows and columns (adjust GPIO pins according to your wiring)
# rows = [Pin(r, Pin.OUT) for r in (27, 26, 25, 33)]   # Row pins (OUTPUT)
# cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in (37, 38, 35, 32)]  # Column pins (INPUT)

# # Keypad mapping
# keys = [
#     ["1", "2", "3", "A"],
#     ["4", "5", "6", "B"],
#     ["7", "8", "9", "C"],
#     ["*", "0", "#", "D"]
# ]

# def scan_keypad():
#     for i, row in enumerate(rows):
#         row.value(1)                     # Drive this row high
#         time.sleep(0.01)                 # Small delay for stabilization
        
#         for j, col in enumerate(cols):
#             if col.value() == 1:          # If the column reads high
#                 print(f"Key Pressed: Row {i+1}, Column {j+1} -> Key: {keys[i][j]}")  # Output the detected key
#                 time.sleep(0.5)           # Debounce delay
#         row.value(0)                     # Turn off row after checking
#     return None

# def main():
#     print("Press keys to see their locations (Row, Column)...")
#     while True:
#         scan_keypad()
#         time.sleep(0.1)  # Short delay to prevent rapid looping

# if __name__ == "__main__":
#     main()




# from machine import Pin
# import time

# # Define rows and columns
# rows = [Pin(r, Pin.OUT) for r in (27, 26, 25, 33)]   # Row pins
# cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in (37, 38, 35, 32)]  # Column pins

# # Keypad mapping
# keys = [
#     ["1", "2", "3", "A"],
#     ["4", "5", "6", "B"],
#     ["7", "8", "9", "C"],
#     ["*", "0", "#", "D"]
# ]

# def scan_keypad():
#     for i, row in enumerate(rows):
#         row.value(1)                     # Drive this row high
#         time.sleep(0.01)                 # Short delay for stabilization
        
#         # Print the state of all columns in the active row
#         for j, col in enumerate(cols):
#             col_state = col.value()
#             print(f"Row {i+1}, Column {j+1} state: {col_state}")  # Print column state
            
#             if col_state == 1:            # If the column reads high
#                 key = keys[i][j]
#                 print(f"Key Pressed: Row {i+1}, Column {j+1} -> Key: {key}")  # Output the detected key
#                 time.sleep(0.5)  # Debounce delay
#         row.value(0)  # Turn off the row after checking
#     return None

# def main():
#     print("Press keys to see their locations (Row, Column)...")
#     while True:
#         scan_keypad()
#         time.sleep(1.0)  # Short delay to prevent rapid looping

# if __name__ == "__main__":
#     main()

# only my keypresses are shown

from machine import Pin
import time

# Define rows and columns (adjust GPIO pins according to your wiring)
# rows = [Pin(r, Pin.OUT) for r in (27, 26, 25, 32)]  # Row pins
rows = [Pin(r, Pin.OUT) for r in (32,25,26,27)]  # Row pins
# cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in (36,37, 38, 39)]  # Column pins
# cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in (39,38,37,36)]  # Column pins
cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in (36,37,38,39)]  # Column pins

# Keypad mapping
keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

def check_key_pressed():
    for i, row in enumerate(rows):
        row.value(1)  # Drive this row high
        time.sleep(0.01)  # Small delay for stabilization
        
        for j, col in enumerate(cols):
            if col.value() == 1:  # If the column reads high
                row.value(0)  # Turn off the row immediately
                return i, j      # Return the row and column indices
        row.value(0)  # Turn off the row after checking
    return None, None

def main():
    print("Press keys to see their locations (Row, Column)...")
    while True:
        row_index, col_index = check_key_pressed()

        if row_index is not None and col_index is not None:
            print(f"Key Pressed: Row {row_index + 1}, Column {col_index + 1} -> Key: {keys[row_index][col_index]}")
            time.sleep(0.5)  # Add a short delay to prevent repetition

if __name__ == "__main__":
    main()
'''

y Pressed: Row 1, Column 3 -> Key: 3
Key Pressed: Row 1, Column 3 -> Key: 3
Key Pressed: Row 2, Column 3 -> Key: 6
Key Pressed: Row 2, Column 3 -> Key: 6
Key Pressed: Row 1, Column 3 -> Key: 3
Key Pressed: Row 3, Column 3 -> Key: 9
Key Pressed: Row 3, Column 3 -> Key: 9
Key Pressed: Row 2, Column 3 -> Key: 6
Key Pressed: Row 1, Column 3 -> Key: 3
Key Pressed: Row 1, Column 3 -> Key: 3
Key Pressed: Row 1, Column 3 -> Key: 3
Key Pressed: Row 1, Column 3 -> Key: 3
Key Pressed: Row 1, Column 3 -> Key: 3
'''
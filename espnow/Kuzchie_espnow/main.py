'''
main.py for controlling Receiver.py and transmitter.py in JBelmont72/ESP32-ESPNOW/espnow/Kuzchie_espnow/
'''
from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import sys
import transmitter
import receiver

# ===== CONFIG =====
BUTTON_PIN = 4         # Button to GND, uses internal pull-up
BUTTON_TIMEOUT_MS = 4000  # Wait 2s for press
# ==================

def choose_role():
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
    print(f'initial butVal: {button.value()}')

    print("Press button within 2 seconds to run as TRANSMITTER...")
    start = ticks_ms()
    while ticks_diff(ticks_ms(), start) < BUTTON_TIMEOUT_MS:
        print(f"[DEBUG] Button value: {button.value()} at {ticks_diff(ticks_ms(), start)} ms")
        if not button.value():  # Button pressed (active low)
            print(f'Button pressed (active low): {button.value()}')
            return "transmitter"
        sleep(0.05)
    print("[DEBUG] Button not pressed within timeout, defaulting to receiver")
    return "receiver"

def main():
    role = choose_role()
    print(f"Selected role: {role.upper()}")

    if role == "transmitter":
        print("[DEBUG] Calling transmitter.main()")
        transmitter.main()
    else:
        print("[DEBUG] Calling receiver.main()")
        receiver.main()

if __name__ == "__main__":
    print("[DEBUG] Starting main()")
    main()

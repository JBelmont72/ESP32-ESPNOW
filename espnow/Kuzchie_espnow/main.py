'''
main.py for controlling Receiver.py and transmitter.py in JBelmont72/ESP32-ESPNOW/espnow/Kuzchie_espnow/
chat with exellent info for main.py https://www.google.com/search?aep=28&udm=50&csuir=1&mstk=AUtExfAhlGsT8m2SxdQNDZld8S3xPp1H-rMafsi-ER6OXIt8lFx3ahT2PiPpLOyTb_J_SkqWxRPniMAY0k8ZJWU8G1Mk-0rHqqjv5eV4ZzAJI-NMYPG3LTSzsuYysnfGTG8xJTXb7OdncTu_VaAL7PFx3_N2DNBr5fblN1U&q=main.py+pico+that+does+not+continuously+import+another+program+but+gies+tio+except%3A+pass+unless+a+button+is+pressed.+short+press+for+one+program+and+ling+press+fir+a+second+program+to+be+imported+button+with+a+long+press+of+4+seconds&oq=&gs_lcrp=EgZjaHJvbWUqDwgCECMYJxjqAhjwBRieBjIPCAAQIxgnGOoCGIAEGIoFMgkIARAjGCcY6gIyDwgCECMYJxjqAhjwBRieBjIPCAMQIxgnGOoCGIAEGIoFMg8IBBAjGCcY6gIYgAQYigUyDwgFECMYJxjqAhjwBRieBjIVCAYQABhCGLQCGOoCGNsFGPAFGJ4GMhUIBxAAGEIYtAIY6gIY2wUY8AUYngbSAQsyNjMyMjA4ajBqN6gCCLACAfEF5HedkkP7ppHxBeR3nZJD-6aR&sourceid=chrome&ie=UTF-8&mtid=qCjtaMOZIN2h5NoP3qzYiA4

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

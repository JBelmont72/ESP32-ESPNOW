'''
main.py to register button press to activate the esp32 with the dfplayer program
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/main.py
See main.md for details of how the timer and button press work and irq.
'''



# import machine            ## old version
# import utime
# import network
# import dfplayer_server

# # ==================== CONFIG ====================
# BUTTON_PIN = 23
# LONG_PRESS_TIME_MS = 4000
# DEBOUNCE_DELAY_MS = 50
# SSID = "NETGEAR48"
# PASSWORD = "waterypanda901"
# STATIC_IP = "10.0.0.24"
# GATEWAY = "10.0.0.1"
# SUBNET = "255.255.255.0"
# # =================================================

# button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
# press_start_time = 0
# press_handled = False
# debounce_timer = machine.Timer(3)

# print("ESP32 ready. Short press → DFPlayer UDP Server. Long press → (reserved).")

# # -------------------- WIFI --------------------
# def connect_wifi():
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, GATEWAY))
#     if not wlan.isconnected():
#         print("📡 Connecting to Wi-Fi...")
#         wlan.connect(SSID, PASSWORD)
#         for _ in range(20):
#             if wlan.isconnected():
#                 break
#             utime.sleep(0.5)
#     if wlan.isconnected():
#         print("✅ Wi-Fi connected:", wlan.ifconfig())
#         return wlan
#     else:
#         print("❌ Could not connect to Wi-Fi.")
#         return None

# # -------------------- BUTTON HANDLER --------------------
# def run_program():
#     global press_start_time
#     press_duration = utime.ticks_diff(utime.ticks_ms(), press_start_time)
#     press_start_time = 0

#     try:
#         if press_duration >= LONG_PRESS_TIME_MS:
#             print("Long press detected → reserved for future use")
#         elif press_duration > DEBOUNCE_DELAY_MS:
#             print("Short press detected → running DFPlayer UDP Server")

#             wlan = connect_wifi()
#             if wlan:
#                 print(f'ip:  {ip}')
#                 ip = STATIC_IP
#                 dfplayer_server.main()
#             else:
#                 print("Cannot run server without Wi-Fi")
#         else:
#             print("Ignored bounce or noise.")
#     except Exception as e:
#         print("Error:", e)
#     finally:
#         utime.sleep(2)
#         machine.reset()

# def button_handler(pin):
#     global press_start_time, press_handled
#     if pin.value():
#         if not press_handled:
#             press_start_time = utime.ticks_ms()
#             press_handled = True
#     else:
#         if press_handled:
#             debounce_timer.init(
#                 period=DEBOUNCE_DELAY_MS,
#                 mode=machine.Timer.ONE_SHOT,
#                 callback=lambda t: run_program()
#             )
#             press_handled = False

# button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING,
#            handler=button_handler)

# # Keep running
# while True:
#     utime.sleep(1)
'''
Below
✅ Improvements in this rework:
Preserves short/long press logic exactly like your original.
Avoids machine.reset() after button press — no more abrupt restart; server keeps running.
Keeps static IP Wi-Fi setup for DFPlayer UDP server.
Works cleanly with the new non-blocking dfplayer_server.py (LED blink, busy pin, UDP commands).
Debounce handled via hardware timer, safe and non-blocking.


'''
#####~~~~~~new version 16 nov 2025 ~~~~~~#####
'''


'''
import machine
import utime
import network
import dfplayer_server

# ==================== CONFIG ====================
BUTTON_PIN = 23
LONG_PRESS_TIME_MS = 4000
DEBOUNCE_DELAY_MS = 50

SSID = "NETGEAR48"
PASSWORD = "waterypanda901"
STATIC_IP = "10.0.0.24"
GATEWAY = "10.0.0.1"
SUBNET = "255.255.255.0"
# =================================================

# Button setup
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
press_start_time = 0
press_handled = False
debounce_timer = machine.Timer(3)

print("ESP32 ready. Short press → DFPlayer UDP Server. Long press → reserved.")

# -------------------- WIFI --------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, GATEWAY))

    if not wlan.isconnected():
        print("📡 Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            utime.sleep(0.5)

    if wlan.isconnected():
        print("✅ Wi-Fi connected:", wlan.ifconfig())
        return wlan
    else:
        print("❌ Could not connect to Wi-Fi.")
        return None

# -------------------- BUTTON HANDLER --------------------
def run_program():
    global press_start_time
    press_duration = utime.ticks_diff(utime.ticks_ms(), press_start_time)
    press_start_time = 0

    try:
        if press_duration >= LONG_PRESS_TIME_MS:
            print("Long press detected → reserved for future use")
        elif press_duration > DEBOUNCE_DELAY_MS:
            print("Short press detected → running DFPlayer UDP Server")

            wlan = connect_wifi()
            if wlan:
                # Start the non-blocking DFPlayer server
                dfplayer_server.main()
            else:
                print("Cannot run server without Wi-Fi")
        else:
            print("Ignored bounce or noise.")
    except Exception as e:
        print("Error:", e)

def button_handler(pin):
    global press_start_time, press_handled
    if pin.value():  # Button pressed
        if not press_handled:
            press_start_time = utime.ticks_ms()
            press_handled = True
    else:  # Button released
        if press_handled:
            # Schedule handling after debounce
            debounce_timer.init(
                period=DEBOUNCE_DELAY_MS,
                mode=machine.Timer.ONE_SHOT,
                callback=lambda t: run_program()
            )
            press_handled = False

# Attach IRQ to button
button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING,
           handler=button_handler)

# -------------------- MAIN LOOP --------------------
while True:
    # Nothing else to do, LED and DFPlayer handled in dfplayer_server.main()
    utime.sleep(1)


#### main.py with an exit button to go with the matching dfplayer_server.py version
'''
Features now implemented:
Short press on BUTTON_START → runs dfplayer_server.main()
Long press on BUTTON_START → reserved for future programs
Exit button (BUTTON_EXIT) → stops the DFPlayer server and returns control to main.py
Non-blocking LED and busy-pin handling inside DFPlayer server
Static IP Wi-Fi setup preserved
You can now restart DFPlayer server multiple times without resetting the ESP32

'''
'''
import machine
import utime
import network
import dfplayer_server

# ==================== CONFIG ====================
BUTTON_START = 23    # short press → start DFPlayer server
BUTTON_EXIT  = 22    # exit server and return to main.py
LONG_PRESS_TIME_MS = 4000
DEBOUNCE_DELAY_MS   = 50

SSID = "NETGEAR48"
PASSWORD = "waterypanda901"
STATIC_IP = "10.0.0.24"
GATEWAY = "10.0.0.1"
SUBNET = "255.255.255.0"
# =================================================

# Buttons
start_btn = machine.Pin(BUTTON_START, machine.Pin.IN, machine.Pin.PULL_DOWN)
exit_btn  = machine.Pin(BUTTON_EXIT,  machine.Pin.IN, machine.Pin.PULL_DOWN)

# State tracking
press_start_time = 0
press_handled = False
debounce_timer = machine.Timer(3)

print("ESP32 ready. Short press → DFPlayer UDP Server. Long press → reserved.")

# -------------------- WIFI --------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, GATEWAY))

    if not wlan.isconnected():
        print("📡 Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            utime.sleep(0.5)

    if wlan.isconnected():
        print("✅ Wi-Fi connected:", wlan.ifconfig())
        return wlan
    else:
        print("❌ Could not connect to Wi-Fi.")
        return None

# -------------------- BUTTON HANDLERS --------------------
def run_program():
    global press_start_time
    press_duration = utime.ticks_diff(utime.ticks_ms(), press_start_time)
    press_start_time = 0

    if press_duration >= LONG_PRESS_TIME_MS:
        print("Long press detected → reserved for future use")
    elif press_duration > DEBOUNCE_DELAY_MS:
        print("Short press detected → running DFPlayer UDP Server")
        wlan = connect_wifi()
        if wlan:
            dfplayer_server.main()  # Runs until exit button clears the flag
        else:
            print("Cannot run server without Wi-Fi")
    else:
        print("Ignored bounce or noise.")

def button_start_handler(pin):
    global press_start_time, press_handled
    if pin.value():  # pressed
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

def button_exit_handler(pin):
    if pin.value():  # exit button pressed
        print("Exit button pressed → stopping DFPlayer server")
        dfplayer_server.running = False  # stops main loop

# Attach IRQs
start_btn.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING,
               handler=button_start_handler)
exit_btn.irq(trigger=machine.Pin.IRQ_RISING,
              handler=button_exit_handler)

# -------------------- MAIN LOOP --------------------
while True:
    utime.sleep(1)  # main.py idle, waiting for button events
'''
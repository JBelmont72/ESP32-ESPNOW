'''
main.py to register button press to activate the esp32 with the dfplayer program
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/main.py
'''



import machine
import utime
import network
import dfplayer_server

# ==================== CONFIG ====================
BUTTON_PIN = 33
LONG_PRESS_TIME_MS = 4000
DEBOUNCE_DELAY_MS = 50
SSID = "NETGEAR48"
PASSWORD = "waterypanda901"
STATIC_IP = "10.0.0.24"
GATEWAY = "10.0.0.1"
SUBNET = "255.255.255.0"
# =================================================

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
press_start_time = 0
press_handled = False
debounce_timer = machine.Timer(3)

print("ESP32 ready. Short press → DFPlayer UDP Server. Long press → (reserved).")

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
                print(f'ip:  {ip}')
                ip = STATIC_IP
                dfplayer_server.main()
            else:
                print("Cannot run server without Wi-Fi")
        else:
            print("Ignored bounce or noise.")
    except Exception as e:
        print("Error:", e)
    finally:
        utime.sleep(2)
        machine.reset()

def button_handler(pin):
    global press_start_time, press_handled
    if pin.value():
        if not press_handled:
            press_start_time = utime.ticks_ms()
            press_handled = True
    else:
        if press_handled:
            debounce_timer.init(
                period=DEBOUNCE_DELAY_MS,
                mode=machine.Timer.ONE_SHOT,
                callback=lambda t: run_program()
            )
            press_handled = False

button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING,
           handler=button_handler)

# Keep running
while True:
    utime.sleep(1)

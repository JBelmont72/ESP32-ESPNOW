# Kuzchie_receiver.py matches up to Kuzechie_transmiter.py 
    # Kuzchie_transmitter.py esp32 with poteniometer espnow  in ESP32-ESPNOW[Github]
    # chat https://chatgpt.com/c/6895f701-c774-8331-8574-be8ffb608ed7 
    #https://www.youtube.com/watch?v=GzugxHEzB0g
    # donsky.  donskytech
# My MAC address for esp module #1  							48:e7:29:98:48:08
# My MC Address for esp module #2   						b'\xb0\xb2\x1c\xa7\xce@'       Device MAC Address: B0:B2:1C:A7:CE:40
# Mac Address for module #3 (my first)    b'\xb0\xb2\x1c\xa9:\\'  Device MAC Address: B0:B2:1C:A9:3A:5C
# Mac Address for ESP module #4          b'\xb0\xb2\x1c\xa8\x9b`'	Device MAC Address: B0:B2:1C:A8:9B:60 note the slight difference in the binary print out with the `' at end
# Mac Address for LilyTTGO number 1  MAC:                d4:d4:da:e0:8f:c4
## Mac address for LilyGo T-Display 2 MAC:               d4:d4:da:e0:2d:50
#Optional: Clean Exit on Ctrl+C
#If you want graceful exits while running the loop, wrap your while True: in a try...except KeyboardInterrupt: block for the main.py sketch at bottom
'''Summary
✔️ Your current main.py logic is solid and works great to prevent Thonny hangs.
✔️ You do not need boot.py unless doing advanced configuration.
✅ Just ensure sender.py or receiver.py has a main() function.
🆗 Button press runs the program; no press exits safely.
'''
'''

# Kuzchie_receiver.py
import network
import espnow
from machine import Pin, I2C
from time import sleep
import ssd1306

# Step 1: Set up Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Step 2: Initialize ESP-NOW
esp = espnow.ESPNow()
esp.init()

# Step 3: Set up I2C (GPIO 22 = SCL, GPIO 21 = SDA)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Step 4: Detect OLED address
oled_address = None
for addr in i2c.scan():
    if addr in [0x3C, 0x3D]:  # Common OLED addresses
        oled_address = addr
        break

if oled_address is None:
    print("OLED not found!")
    while True:
        pass

# Step 5: Initialize OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Step 6: Callback not supported in MicroPython, so use polling
esp.recv_cb(None)  # Just in case previously set
print("Receiver ready")

while True:
    host, msg = esp.recv()
    if msg:
        try:
            pot_val = int(msg.decode())
        except:
            pot_val = 0

        oled.fill(0)
        oled.text("ESP-NOW", 30, 0)
        oled.text("Receiver", 25, 18)
        oled.text(str(pot_val), 40, 40)
        oled.show()
        print(f"Received: {pot_val}")
    sleep(0.1)


import network
import espnow
import binascii # For converting MAC address to a printable format
import time

# Initialize Wi-Fi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

# Initialize ESP-NOW
e = espnow.ESPNow()
try:
    e.active(True)
except OSError as err:
    print("Failed to initialize ESP-NOW:", err)
    raise

def espnow_recv_callback(espnow_instance):
    while True:
        mac, msg = espnow_instance.recv()
        if mac is None: # Timeout, no message
            break
        print("Received from:", binascii.hexlify(mac).decode(), "Message:", msg.decode()) # Decode bytes to string
        # You can add logic here to process the received message

e.irq(espnow_recv_callback) # Register the callback

print("Waiting for messages...")
# Keep the program running to receive messages
while True:
    time.sleep(1)
 '''   
    
import network
import espnow
from machine import Pin, I2C
from time import sleep
import ssd1306

import binascii # For converting MAC address to a printable format
import time

# Initialize Wi-Fi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

# Initialize ESP-NOW
e = espnow.ESPNow()
try:
    e.active(True)
except OSError as err:
    print("Failed to initialize ESP-NOW:", err)
    raise

# Step 3: Set up I2C (GPIO 22 = SCL, GPIO 21 = SDA)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Step 4: Detect OLED address
oled_address = None
for addr in i2c.scan():
    if addr in [0x3C, 0x3D]:  # Common OLED addresses
        oled_address = addr
        break

if oled_address is None:
    print("OLED not found!")
    while True:
        pass

# Step 5: Initialize OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Step 6: Callback not supported in MicroPython, so use polling
esp.recv_cb(None)  # Just in case previously set
def espnow_recv_callback(espnow_instance):
    while True:
        mac, msg = espnow_instance.recv()
        if mac is None: # Timeout, no message
            break
        print("Received from:", binascii.hexlify(mac).decode(), "Message:", msg.decode()) # Decode bytes to string
        # You can add logic here to process the received message

e.irq(espnow_recv_callback) # Register the callback

print("Waiting for messages...")
# Keep the program running to receive message





print("Receiver ready")

while True:
    host, msg = esp.recv()
    if msg:
        try:
            pot_val = int(msg.decode())
        except:
            pot_val = 0

        oled.fill(0)
        oled.text("ESP-NOW", 30, 0)
        oled.text("Receiver", 25, 18)
        oled.text(str(pot_val), 40, 40)
        oled.show()
        print(f"Received: {pot_val}")
    sleep(0.1)
'''
main.py to launch the program with pushbuton on pin 4
# main.py - use pushbutton on GPIO 4 to run selected program
from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import sys
import sender  # or: import receiver

# Configuration
BUTTON_PIN = 4
TIMEOUT_MS = 1000  # 1 second

# Setup button
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

print("Waiting for button press...")

start = ticks_ms()
while ticks_diff(ticks_ms(), start) < TIMEOUT_MS:
    if not button.value():  # Button pressed
        print("Button pressed — running sender")  # Or "receiver"
        sender.main()  # Or receiver.main()
        break
    sleep(0.05)

print("No button press — exiting safely")
sys.exit()
'''

'''
# receiver.py
def main():
    import network
    import espnow
    from machine import Pin, I2C
    import ssd1306
    from time import sleep

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    esp = espnow.ESPNow()
    esp.init()

    i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    addr = None
    for a in i2c.scan():
        if a in [0x3C, 0x3D]:
            addr = a
            break
    if addr is None:
        print("No OLED found.")
        return

    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=addr)

    while True:
        host, msg = esp.recv()
        if msg:
            try:
                val = int(msg.decode())
            except:
                val = 0

            oled.fill(0)
            oled.text("ESP-NOW", 30, 0)
            oled.text("Receiver", 25, 18)
            oled.text(str(val), 40, 40)
            oled.show()
            print(f"Received: {val}")
        sleep(0.1)
'''
'''
#one of the above versions have .irq  whichis not supported in ESPNOW
# Removed e.active(True) (invalid for ESP-NOW).
#Used e.init() to start ESP-NOW.
#Removed e.irq() — there’s no supported IRQ-based callback in MicroPython’s espnow yet.
#Pure polling loop with e.recv().
# Why polling is used here
#Because MicroPython doesn’t register an interrupt or background listener for ESP-NOW, your code must keep calling recv() in the loop to catch messages. If you don’t, messages are dropped.
import network
import espnow
from machine import Pin, I2C
from time import sleep
import ssd1306
import binascii

# --- 1. Initialize Wi-Fi (must be in STA mode for ESP-NOW) ---
sta = network.WLAN(network.STA_IF)
sta.active(True)

# --- 2. Initialize ESP-NOW ---
e = espnow.ESPNow()
try:
    e.init()
except OSError as err:
    print("Failed to initialize ESP-NOW:", err)
    raise

# --- 3. Set up I2C (OLED) ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Detect OLED address dynamically
oled_address = None
for addr in i2c.scan():
    if addr in [0x3C, 0x3D]:
        oled_address = addr
        break
if oled_address is None:
    print("OLED not found!")
    while True:
        pass

oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# --- 4. Poll for messages ---
print("Receiver ready — polling for messages...")

while True:
    host, msg = e.recv()
    if msg:
        try:
            pot_val = int(msg.decode())
        except:
            pot_val = 0

        print("Received from:", binascii.hexlify(host).decode(), "Value:", pot_val)

        oled.fill(0)
        oled.text("ESP-NOW", 30, 0)
        oled.text("Receiver", 25, 18)
        oled.text(str(pot_val), 40, 40)
        oled.show()
    sleep(0.1)
'''
'''
complete MicroPython ESP32 ESP-NOW receiver that:
Initializes the OLED no matter what I²C address it finds (instead of only 0x3C or 0x3D).
Uses polling to check for new ESP-NOW messages.
Displays the received potentiometer value on the OLED.
Shows "No Signal" if no message has arrived for a given timeout period.
'''
import network
import espnow
from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff
import ssd1306
import binascii

# ====== CONFIG ======
NO_SIGNAL_TIMEOUT = 2000  # ms — time before showing "No Signal"
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
# ====================

# --- 1. Wi-Fi STA mode ---
sta = network.WLAN(network.STA_IF)
sta.active(True)

# --- 2. Initialize ESP-NOW ---
e = espnow.ESPNow()
try:
    e.init()
except OSError as err:
    print("Failed to initialize ESP-NOW:", err)
    raise

# --- 3. Set up I²C and OLED ---
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
scan_result = i2c.scan()

if not scan_result:
    print("No I2C devices found!")
    while True:
        pass

oled_address = scan_result[0]  # First device found
print(f"OLED found at I2C address: 0x{oled_address:02X}")

oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# --- 4. Variables for "No Signal" detection ---
last_msg_time = ticks_ms()
last_value = None

# --- 5. Main polling loop ---
print("Receiver ready — polling for messages...")

while True:
    host, msg = e.recv()
    if msg:  # If we got a message
        try:
            pot_val = int(msg.decode())
        except:
            pot_val = 0

        last_msg_time = ticks_ms()
        last_value = pot_val

        print("Received from:", binascii.hexlify(host).decode(), "Value:", pot_val)

    # --- OLED update ---
    oled.fill(0)
    oled.text("ESP-NOW", 30, 0)
    oled.text("Receiver", 25, 18)

    # If signal recent, display value
    if last_value is not None and ticks_diff(ticks_ms(), last_msg_time) < NO_SIGNAL_TIMEOUT:
        oled.text(str(last_value), 40, 40)
    else:
        oled.text("No Signal", 20, 40)

    oled.show()
    sleep(0.1)
'''
 How This Works
OLED Initialization
Scans for any I²C device and uses the first address found.
Works even if your OLED has a non-standard address.
Polling for Messages
Calls e.recv() repeatedly to check for new ESP-NOW packets.
If received, decodes and stores the value + timestamp.
"No Signal" Timeout
If no message arrives within NO_SIGNAL_TIMEOUT ms (default: 2s), OLED shows "No Signal".
Printing to REPL
Prints both sender MAC address and value to the console.
📝 Tip
To avoid Thonny lock-ups, you can still use your push-button main.py launcher to run this script only if desired:
import receiver
receiver.main()


'''

##### last updates !!!!
#Benefits of This Layout
#receiver.py is completely self-contained — just call receiver.main().
#Pushbutton logic remains in your universal main.py.
#Works with any OLED I²C address found.
#Uses polling for ESP-NOW (no unsupported callbacks in MicroPython).

import network
import espnow
from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff
import ssd1306
import binascii

# ====== CONFIG ======
NO_SIGNAL_TIMEOUT = 2000  # ms — time before showing "No Signal"
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
# ====================

def main():
    # --- 1. Wi-Fi STA mode ---
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    # --- 2. Initialize ESP-NOW ---
    e = espnow.ESPNow()
    try:
        e.init()
    except OSError as err:
        print("Failed to initialize ESP-NOW:", err)
        return

    # --- 3. Set up I²C and OLED ---
    i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
    scan_result = i2c.scan()

    if not scan_result:
        print("No I2C devices found!")
        return

    oled_address = scan_result[0]  # Use the first device found
    print(f"OLED found at I2C address: 0x{oled_address:02X}")

    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

    # --- 4. Variables for "No Signal" detection ---
    last_msg_time = ticks_ms()
    last_value = None

    # --- 5. Main polling loop ---
    print("Receiver ready — polling for messages...")

    while True:
        host, msg = e.recv()
        if msg:  # If we got a message
            try:
                pot_val = int(msg.decode())
            except:
                pot_val = 0

            last_msg_time = ticks_ms()
            last_value = pot_val

            print("Received from:", binascii.hexlify(host).decode(), "Value:", pot_val)

        # --- OLED update ---
        oled.fill(0)
        oled.text("ESP-NOW", 30, 0)
        oled.text("Receiver", 25, 18)

        if last_value is not None and ticks_diff(ticks_ms(), last_msg_time) < NO_SIGNAL_TIMEOUT:
            oled.text(str(last_value), 40, 40)
        else:
            oled.text("No Signal", 20, 40)

        oled.show()
        sleep(0.1)



#main.py for the above
#How to Launch with Your Pushbutton main.py
#Example main.py for running receiver when the button is pressed
from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import sys
import receiver  # Or sender when testing transmitter

BUTTON_PIN = 4
TIMEOUT_MS = 1000  # 1 second

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

print("Waiting for button press...")

start = ticks_ms()
while ticks_diff(ticks_ms(), start) < TIMEOUT_MS:
    if not button.value():  # Pressed
        print("Button pressed — running receiver")
        receiver.main()
        break
    sleep(0.05)

print("No button press — exiting safely")
sys.exit()
       
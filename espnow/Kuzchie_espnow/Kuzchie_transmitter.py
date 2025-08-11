# Kuzchie_transmitter.py matches up to Kuzechie_receiver.py
    # Kuzchie_transmitter.py esp32 with poteniometer espnow  in ESP32-ESPNOW[Github]
    # chat https://chatgpt.com/c/6895f701-c774-8331-8574-be8ffb608ed7
    #https://www.youtube.com/watch?v=GzugxHEzB0g
    # donsky.  donskytech
# My MAC address for esp module #1  	 b'H\xe7)\x98H\x08'  Device MAC Address: 48:E7:29:98:48:08
# My MC Address for esp module #2   						b'\xb0\xb2\x1c\xa7\xce@'       Device MAC Address: B0:B2:1C:A7:CE:40
# Mac Address for module #3 (my first)    b'\xb0\xb2\x1c\xa9:\\'  Device MAC Address: B0:B2:1C:A9:3A:5C
# Mac Address for ESP module #4          b'\xb0\xb2\x1c\xa8\x9b`'	Device MAC Address: B0:B2:1C:A8:9B:60 note the slight difference in the binary print out with the `' at end
# Mac Address for LilyTTGO number 1  MAC:                d4:d4:da:e0:8f:c4
## Mac address for LilyGo T-Display 2 MAC:               d4:d4:da:e0:2d:50
#Optional: Clean Exit on Ctrl+C
#If you want graceful exits while running the loop, wrap your while True: in a try...except KeyboardInterrupt: block for the main.py sketch at botom!
'''
Summary
✔️ Your current main.py logic is solid and works great to prevent Thonny hangs. at bottom
✔️ You do not need boot.py unless doing advanced configuration.
✅ Just ensure sender.py or receiver.py has a main() function.
🆗 Button press runs the program; no press exits safely.
'''
'''
✅ STEP 1: Algorithm (High-Level Flow)
📤 Transmitter:
Initialize ESP-NOW and set it to station mode.
Register the receiver's MAC address.
In a loop:
Read the potentiometer value from A0.
Send the value using ESP-NOW.
📥 Receiver:
Initialize ESP-NOW and set it to station mode.
Initialize the OLED screen (with dynamic I2C address detection).
Register a callback for incoming data.
In a loop:
Display the received potentiometer value on the OLED.
'''
# transmitter.py
import network
import espnow
from machine import ADC, Pin
from time import sleep

# Step 1: Set up Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Step 2: Initialize ESP-NOW
esp = espnow.ESPNow()
esp.init()

# Step 3: Add peer (receiver's MAC address)
peer_mac =  b'\xb0\xb2\x1c\xa9:\\'  # Replace with my receiver MAC address esp32 #3
esp.add_peer(peer_mac)

# Step 4: Set up ADC (Potentiometer on GPIO 36 / A0)
pot = ADC(Pin(36))       # GPIO 36 = A0 on ESP32
pot.atten(ADC.ATTN_11DB) # Full range: 0–3.3V
pot.width(ADC.WIDTH_10BIT)  # 0–1023

while True:
    pot_val = pot.read()
    print(f"Sending: {pot_val}")
    esp.send(peer_mac, str(pot_val))  # Send as string
    sleep(0.5)
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
# sender.py
def main():
    import network
    import espnow
    from machine import ADC, Pin
    from time import sleep

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    esp = espnow.ESPNow()
    esp.init()

    peer_mac = b'\x7C\x9E\xBD\xF5\xBE\x30'
    esp.add_peer(peer_mac)

    pot = ADC(Pin(36))
    pot.atten(ADC.ATTN_11DB)
    pot.width(ADC.WIDTH_10BIT)

    while True:
        val = pot.read()
        esp.send(peer_mac, str(val))
        print(f"Sent: {val}")
        sleep(0.5)
'''

# final updates  !!! and matches final updates in Kuzchie_receiver.py
#Wrapped everything in main() so your pushbutton loader can control execution.
#Added MAC display at startup so you know which ESP is which.
#Added try/except for ESP-NOW initialization and peer addition.
#Config section at the top so you can quickly change pins, MAC, and delay.
#More comments to follow along easily.
# the Kuzchie_transmitter.py and the main.py to go with it follows
import network
import espnow
from machine import ADC, Pin
from time import sleep
import binascii

# ====== CONFIG ======
PEER_MAC = b'\xb0\xb2\x1c\xa9:\\'   # <-- Replace with receiver MAC
POT_PIN = 36                        # GPIO 36 / A0
SEND_DELAY = 0.5                    # seconds
# ====================

def main():
    # --- 1. Wi-Fi STA mode ---
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Show our MAC address
    print("Transmitter MAC:", binascii.hexlify(wlan.config('mac')).decode())

    # --- 2. Initialize ESP-NOW ---
    esp = espnow.ESPNow()
    try:
        esp.init()
    except OSError as err:
        print("Failed to initialize ESP-NOW:", err)
        return

    # --- 3. Add receiver as peer ---
    try:
        esp.add_peer(PEER_MAC)
    except OSError as err:
        print("Failed to add peer:", err)
        return

    # --- 4. Configure ADC for potentiometer ---
    pot = ADC(Pin(POT_PIN))
    pot.atten(ADC.ATTN_11DB)       # Full 0–3.3V range
    pot.width(ADC.WIDTH_10BIT)     # Resolution: 0–1023

    print("Transmitter ready — sending values...")

    # --- 5. Main loop ---
    while True:
        pot_val = pot.read()
        print(f"Sending: {pot_val}")
        try:
            esp.send(PEER_MAC, str(pot_val))  # Send as string
        except OSError as err:
            print("Send failed:", err)
        sleep(SEND_DELAY)
'''
main.py for the above
from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import sys
import transmitter  # swap with receiver when testing

BUTTON_PIN = 4
TIMEOUT_MS = 1000

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

print("Waiting for button press...")

start = ticks_ms()
while ticks_diff(ticks_ms(), start) < TIMEOUT_MS:
    if not button.value():  # Pressed
        print("Button pressed — running transmitter")
        transmitter.main()
        break
    sleep(0.05)

print("No button press — exiting safely")
sys.exit()
'''


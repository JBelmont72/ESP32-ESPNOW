'''
# JBelmont72/ESP32-ESPNOW/espnow/espnow_init/Receiver.py
# https://www.google.com/search?q=espnow+init&ie=UTF-8&oe=UTF-8&hl=en-us&client=safari&udm=50&fbs=AIIjpHxU7SXXniUZfeShr2fp4giZud1z6kQpMfoEdCJxnpm_3WBcADgXS0kQ7L92bqYkFCFNOV_HVSgOLkzTtMTzzOoU9E7al0ivYItrO6EoUe-HW1iOl73fkm5mHKkC4QbpJ_9OfQFUG6x9jp3K3j00kLH4F67z51jCweMRzMhoEVNGOIbDo_3u5-5HQjZ7qTdgogrIrRUls2-o9Sv3O8gdVJjLg0xjl0YP5xulf7mZcJMEARofsOw&ved=2ahUKEwjajeDHmfyOAxWJLFkFHfnAIyMQ0NsOegQIHRAA&aep=10&ntc=1&mtid=4XGWaJ_5H7vV5NoPh-CTqQg&mstk=AUtExfDNSrd-umrk4amDvue9jkx9B2LfK5chsOBjRc-UNfzhcNqPbL-W9pTl3KVKOWrLXySI1u8F37YGauOVEssXvW2wco_njQr5x-GYHiWQIrlPIt_WrO0B1gDp3ZdbisfXLEq7acUESEDLWUKOdwKKzsuibNKsfT2ZvWe7pvjw4Y5e-DL-XTAehEIWuRdy4lE_kd1jF77PqkadutzHLM7EoejVmxqJ4HO0S0iK4u2fUP7yNdYA0a0cXF-gh8u7qaVaPUVkLUpk44GsPUwncnyN7tzfBRahe9fjthna9zBLnzRdzK72uyBr5xkDq8SaFZ_jR-BHjd-UqHnPDA&csuir=1
# My MAC address for esp module #1  							48:e7:29:98:48:08	b'H\xe7)\x98H\x08'
# My MC Address for esp module #2   						b'\xb0\xb2\x1c\xa7\xce@'       Device MAC Address: B0:B2:1C:A7:CE:40
# Mac Address for module #3 (my first)    b'\xb0\xb2\x1c\xa9:\\'  Device MAC Address: B0:B2:1C:A9:3A:5C
# Mac Address for ESP module #4          b'\xb0\xb2\x1c\xa8\x9b`'	Device MAC Address: B0:B2:1C:A8:9B:60 note the slight difference in the binary print out with the `' at end
# Mac Address for LilyTTGO number 1  MAC:                d4:d4:da:e0:8f:c4
## Mac address for LilyGo T-Display 2 MAC:               d4:d4:da:e0:2d:50
'''
import network
import espnow
import binascii # For converting MAC address to a printable format
import time

# Initialize Wi-Fi
sta = network.WLAN(network.STA_IF)
sta.active(True)
#sta.disconnect()

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
# to use this main.py the receiver (or transmttter.py) must have a main.py
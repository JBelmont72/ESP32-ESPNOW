'''
# JBelmont72/ESP32-ESPNOW/espnow/espnow_init/Transmitter.py
# My MAC address for esp module #1  							48:e7:29:98:48:08
# My MC Address for esp module #2   						b'\xb0\xb2\x1c\xa7\xce@'       Device MAC Address: B0:B2:1C:A7:CE:40
# Mac Address for module #3 (my first)    b'\xb0\xb2\x1c\xa9:\\'  Device MAC Address: B0:B2:1C:A9:3A:5C
# Mac Address for ESP module #4          b'\xb0\xb2\x1c\xa8\x9b`'	Device MAC Address: B0:B2:1C:A8:9B:60 note the slight difference in the binary print out with the `' at end
# Mac Address for LilyTTGO number 1  MAC:                d4:d4:da:e0:8f:c4
## Mac address for LilyGo T-Display 2 MAC:               d4:d4:da:e0:2d:50
'''
import network
import espnow
import time

# Receiver's MAC address
receiver_mac = b'\x30\xae\xa4\xf6\x7d\x4c' 

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

# Add the peer
try:
    e.add_peer(receiver_mac)
except OSError as err:
    print("Failed to add peer:", err)
    raise

print("Sending messages...")
for i in range(10):
    message = "Hello, world! " + str(i)
    e.send(receiver_mac, message.encode()) # Send as bytes
    time.sleep(1)
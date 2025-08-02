# espnow/find_device_mac_address.py
# Donsky. Donskytech
#/Users/judsonbelmont/Documents/RandomNerd/micropython-ESP32-ESP8266/espnow/find_device_mac_address.py
import network

# Initialize the network interface
wlan = network.WLAN(network.STA_IF)
# Activate the WLAN Interface
wlan.active(True)

# Check if the interface is active (connected)
if wlan.active():
    # Get the MAC address
    mac_address = wlan.config("mac")
    print(mac_address)
    print("Device MAC Address:", ":".join(["{:02X}".format(byte) for byte in mac_address]))
else:
    print("Wi-Fi is not active.")
# https://www.donskytech.com/discovering-esp-now-in-micropython-with-asyncio/
# /Users/judsonbelmont/Documents/RandomNerd/ESPNOW/EspNow-1/Asynchronous/esp_now_async_button_click_receiver.py
# donsky.  donskytech
# My MAC address for esp module #1  							48:e7:29:98:48:08
# My MC Address for esp module #2   						b'\xb0\xb2\x1c\xa7\xce@'       Device MAC Address: B0:B2:1C:A7:CE:40
# Mac Address for module #3 (my first)    b'\xb0\xb2\x1c\xa9:\\'  Device MAC Address: B0:B2:1C:A9:3A:5C
# Mac Address for ESP module #4          b'\xb0\xb2\x1c\xa8\x9b`'	Device MAC Address: B0:B2:1C:A8:9B:60 note the slight difference in the binary print out with the `' at end
# Mac Address for LilyTTGO number 1  MAC:                d4:d4:da:e0:8f:c4
# # Mac address for LilyGo T-Display 2 MAC:               d4:d4:da:e0:2d:50

import network
import aioespnow
import machine
import asyncio

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
esp.active(True)

led_pin = machine.Pin(22, machine.Pin.OUT)

async def wait_for_message():
    while True:
        _, msg = esp.recv()
        if msg:             # msg == None if timeout in recv()
            if msg == b'ledOn':
                print("Turning on LED")
                led_pin.on()
            elif msg == b'ledOff':
                print("Turning off LED")
                led_pin.off()
            else:
                print(f"Unknown message {msg}")
            

asyncio.run(wait_for_message())

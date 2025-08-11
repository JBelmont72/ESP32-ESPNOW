# /Users/judsonbelmont/Documents/RandomNerd/ESPNOW/EspNow-1/Asynchronous/esp_now_async_button_click_sender.py
# https://www.donskytech.com/discovering-esp-now-in-micropython-with-asyncio/
# partner program /Users/judsonbelmont/Documents/RandomNerd/ESPNOW/EspNow-1/Asynchronous/esp_now_async_button_click_receiver.py
# donsky.  donskytech
# My MAC address for esp module #1  							48:e7:29:98:48:08
# My MC Address for esp module #2   						b'\xb0\xb2\x1c\xa7\xce@'       Device MAC Address: B0:B2:1C:A7:CE:40
# Mac Address for module #3 (my first)    b'\xb0\xb2\x1c\xa9:\\'  Device MAC Address: B0:B2:1C:A9:3A:5C
# Mac Address for ESP module #4          b'\xb0\xb2\x1c\xa8\x9b`'	Device MAC Address: B0:B2:1C:A8:9B:60 note the slight difference in the binary print out with the `' at end
# Mac Address for LilyTTGO number 1  MAC:                d4:d4:da:e0:8f:c4
## Mac address for LilyGo T-Display 2 MAC:               d4:d4:da:e0:2d:50
import network
import aioespnow
import asyncio
from machine import Pin

# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)

esp = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
esp.active(True)
peer = b'x!\x84\xc68\xb0'
esp.add_peer(peer)

# Create a function to send data when a button is pressed (optional)
button_pin = Pin(23, Pin.IN, Pin.PULL_UP)
debounce_delay = 50  # Adjust this value to your needs (milliseconds)


async def send_button_state(espnow):
    last_state = button_pin.value()
    while True:
        state = button_pin.value()
        if state != last_state:
            await asyncio.sleep_ms(debounce_delay)
            state = button_pin.value()
            if state != last_state:
                if state == 0:
                    message = "ledOn"
                    print(f"Sending command : {message}")
                    await espnow.asend(peer, message)
                else:
                    message = "ledOff"
                    print(f"Sending command : {message}")
                    await espnow.asend(peer, message)
                last_state = state
        await asyncio.sleep_ms(10)  # Adjust the polling interval as needed
        
        
asyncio.run(send_button_state(esp))
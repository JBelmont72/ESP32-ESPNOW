'''
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Asyncio_lessons/asyncio_1.py
[chat for learning asyncio in micropython](https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855)
Point to remember about asyncio in micropython:
1.async def defines coroutines (non-blocking functions)
2.await asyncio.sleep() pauses without freezing other tasks
3.create_task() lets both run together(place these in def  main())
4.asyncio.run(main()) then starts the event loop
5. uasyncio is the MicroPython version (lighter and correct for Pico W).
6.The infinite loop inside main() keeps it running, so you don’t need loop.run_forever().
7. asyncio.run(main()) handles setup and cleanup properly
version 3 incorporates isinstnace(). line 92

adc on 28 and 27 Pico
Start with the **Pico W as the BLE peripheral** is the best approach. It lets you test advertising and data sending first, then you can connect from *anything else* later.

the quick concept you need to keep in mind for BLE peripherals:

### 🧠 BLE Peripheral Basics

* A **peripheral** *advertises* — it says “I’m here!”
* It exposes **services**, each with **characteristics** (data points you can read/write/notify).
* Example: a “Temperature Service” with a “Current Temp” characteristic.
* The **central** (e.g., another Pico, your Mac, or Pi) connects and reads/writes those characteristics.

---

We’ll use the **`aioble`** library in MicroPython (it wraps the `bluetooth` module and works great with `uasyncio`).

A minimal peripheral needs to:

1. Create a BLE service and characteristic.
2. Advertise with a name.
3. Keep running in an async loop.

--- The **structure** :

```python
import aioble
import bluetooth
import uasyncio as asyncio

# create a BLE service
service_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
service = aioble.Service(service_uuid)

# add a characteristic (readable)
char_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
characteristic = aioble.Characteristic(service, char_uuid, read=True, notify=True)

# register the service
aioble.register_services(service)### note the plural

This defines your BLE “identity.” Next we’ll advertise it and allow connections.
[chat tutorial for bluetooth](https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855)

NOTE: there are two versions of bluetooth. My Pico W has the older version
(probably my ESP32s have the newer version!)
I am copying the chat input about the differences just in case i am using the ESP32 and have to change to the new version.
If i have problems: read the Asyncio_BLE_lesson.md!!

program number 1 on Pico:
advertises a service
accepts a connection
but doesn’t yet serve any data (so nRF Connect can’t show any values)
Program 2 will send a single digit to nrf mobile app to 'notify'
'''
# import aioble       ## program 1 advertises and accepts connection, old BLE library
# import bluetooth
# import uasyncio as asyncio

# async def peripheral_task():
#     ble = bluetooth.BLE()

#     # --- Define a service and a characteristic ---
#     service_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
#     service = aioble.Service(service_uuid)

#     char_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
#     characteristic = aioble.Characteristic(
#         service,
#         char_uuid,
#         read=True,
#         notify=True
#     )

#     # ✅ Correct registration method for your version
#     aioble.register_services(service)

#     print("Starting BLE advertisement...")

#     # --- Advertise the service ---
#     async with await aioble.advertise(
#         interval_us=500000,
#         name="PicoPeripheral",
#         services=[service_uuid]
#     ) as connection:
#         print("Connected to:", connection.device)
#         while True:
#             await asyncio.sleep(1)

# asyncio.run(peripheral_task())

#########~~~~~~ program number 2 'notifies' a single digit SEE program number 3
# note: this does not work because it uses the newer version of aioble.  We use `await aioble.notify(connection, characteristic)` instead of calling a method on the characteristic.
#This matches your `aioble` build (since `characteristic.notify()` doesn’t exist there).SEE Nov2025/Asyncio_lessons/Asyncio_BLE_lesson.md for discussion 
# import aioble
# import bluetooth
# import uasyncio as asyncio
# import struct  # helps pack integers into bytes for BLE

# async def peripheral_task():
#     ble = bluetooth.BLE()

#     # --- Define service and characteristic ---
#     service_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
#     service = aioble.Service(service_uuid)

#     char_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
#     characteristic = aioble.Characteristic(
#         service, char_uuid, read=True, notify=True
#     )

#     aioble.register_services(service)

#     print("Starting BLE advertisement...")

#     async with await aioble.advertise(
#         interval_us=200000,
#         name="PicoPeripheral",
#         services=[service_uuid]
#     ) as connection:
#         print("Connected to:", connection.device)
#         count = 0
#         while connection.is_connected():
#             # pack integer as 2 bytes (BLE sends bytes)
#             value = struct.pack("<h", count)
#             characteristic.write(value)
#             await characteristic.notify(connection)
#             print("Sent:", count)
#             count += 1
#             await asyncio.sleep(1)

# asyncio.run(peripheral_task())
########~~~~~~~~.    program number 3 same as number 2 but adjusted for the older version of aioble. slightly older aioble API, where you need to manually write to the characteristic’s GATT handle and then call connection.notify() instead of characteristic.notify().

import aioble
import bluetooth
import uasyncio as asyncio
import struct

async def peripheral_task():
    ble = bluetooth.BLE()

    # --- Define service & characteristic ---
    service_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
    service = aioble.Service(service_uuid)

    char_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
    characteristic = aioble.Characteristic(
        service, char_uuid, read=True, notify=True
    )

    aioble.register_services(service)

    print("Starting BLE advertisement...")

    async with await aioble.advertise(
        interval_us=200000,
        name="PicoPeripheral",
        services=[service_uuid]
    ) as connection:
        print("Connected to:", connection.device)

        count = 0
        while connection.is_connected():
            # pack value into bytes
            value = struct.pack("<h", count)
            characteristic.write(value)  # update local value
            await aioble.notify(connection, characteristic)  # send notify
            print("Sent:", count)
            count += 1
            await asyncio.sleep(1)

asyncio.run(peripheral_task())







'''
import uasyncio as asyncio
import bluetooth
import aioble
from machine import Pin, ADC
import sys


green_led = Pin(17, Pin.OUT)
blue_led = Pin(16, Pin.OUT)

async def LED(pin,delay):
    try:
        while True:
            pin.value(0)
            await asyncio.sleep(delay)
            pin.value(1)
            await asyncio.sleep(delay)
    except Exception as e:
        print(f'Error value:  {e}')    
    
async def main():
    asyncio.create_task(LED(green_led,1))
    asyncio.create_task(LED(blue_led,2))
    while True:  # keep main alive
        await asyncio.sleep(1)
try:
    asyncio.run(main())
except KeyboardInterrupt:
    green_led.value(0)
    blue_led.value(0)
    print('exiting cleanly!')
    sys.exit()
''' 


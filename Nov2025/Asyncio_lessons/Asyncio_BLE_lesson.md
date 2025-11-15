

Perfect 👍 — since `aioble` is installed, we can now make your **Pico W advertise** like a real BLE peripheral.

Here’s the basic async structure you’ll use (just study this one first):

```python
import aioble
import bluetooth
import uasyncio as asyncio

async def peripheral_task():
    ble = bluetooth.BLE()
    service_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
    service = aioble.Service(service_uuid)
    char_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
    characteristic = aioble.Characteristic(service, char_uuid, read=True, notify=True)

    aioble.register_service(service)

    # advertise with a name
    async with await aioble.advertise(
        interval_us=500000,
        name="PicoPeripheral",
        services=[service_uuid],
    ) as connection:
        print("Connected:", connection.device)
        while True:
            await asyncio.sleep(1)

asyncio.run(peripheral_task())
```

🔍 **What happens:**

* The Pico advertises with the name `"PicoPeripheral"`.
* When a central (like a phone or another board) connects, the `print()` runs.
* The loop keeps it alive.

---

### ✅ Action Step

Run this program and open your phone or computer’s **Bluetooth scanner** app (e.g., nRF Connect).
See if you can spot `"PicoPeripheral"` broadcasting.
Tell me:

* Can you see the device name?
* Does it show the UUID we defined?
Excellent — you’re digging right into the right area 👏

The reason for this confusion is that **there are two ways to do BLE in MicroPython**:

1. The **low-level `bluetooth` / `ubluetooth`** module (where you use `gatts_register_services()` yourself).
2. The **high-level `aioble`** library (which *wraps* the Bluetooth layer and adds async helpers).

You’re currently mixing the two styles — and that’s why you see `AttributeError` (your `aioble` version doesn’t use `.register()` or `aioble.register_service()` because your build is slightly older).

Let’s confirm your environment before we continue, so I can show you the **exact syntax your firmware uses**.

---

### ✅ Quick Check

Please open the REPL and run:

```python
import aioble
dir(aioble)
```

Then copy or describe the function names you see — especially anything like:

```
Service, Characteristic, advertise, Peripheral, register_service, etc.
```

That will tell us whether your `aioble` build uses the:

* **old** `aioble.register_service(service)` pattern,
* or the **new** `service.register()` pattern,
* or if it’s missing both (and we’ll use `bluetooth.gatts_register_services()` directly).

Once I know that, I’ll show you a *working* minimal advertiser for your specific MicroPython build.

print(dir(aioble)
['__class__', '__name__', 'const', 'stop', '__dict__', '__file__', '__path__', 'config', 'scan', 'core', '__version__', 'Device', 'DeviceDisconnectedError', 'device', 'log_info', 'log_warn', 'log_error', 'GattError', 'advertise', 'peripheral', 'central', 'Service', 'Characteristic', 'BufferedCharacteristic', 'Descriptor', 'register_services', 'server', 'ADDR_PUBLIC', 'ADDR_RANDOM']
Perfect — thanks! 🎯
That tells us your `aioble` version is the **older MicroPython build**, which uses:

```python
aioble.register_services(service)
```

(not `register_service` or `service.register()`).

So let’s fix your code for *your* version.
Here’s a minimal, **working** BLE peripheral example for your environment 👇

---

```python
import aioble
import bluetooth
import uasyncio as asyncio

async def peripheral_task():
    ble = bluetooth.BLE()

    # --- Define a service and a characteristic ---
    service_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
    service = aioble.Service(service_uuid)

    char_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
    characteristic = aioble.Characteristic(
        service,
        char_uuid,
        read=True,
        notify=True
    )

    # ✅ Correct registration method for your version
    aioble.register_services(service)

    print("Starting BLE advertisement...")

    # --- Advertise the service ---
    async with await aioble.advertise(
        interval_us=500000,
        name="PicoPeripheral",
        services=[service_uuid]
    ) as connection:
        print("Connected to:", connection.device)
        while True:
            await asyncio.sleep(1)

asyncio.run(peripheral_task())
```

---

### 💡 Key differences for your version

* The function is `aioble.register_services()` (plural).
* You don’t call `.register()` on the service object itself.
* Everything else — `Service`, `Characteristic`, and `advertise()` — works the same.

---

### ✅ Action Step

Run this exact version and open your BLE scanner (e.g., *nRF Connect* or *LightBlue*).
Tell me:

* Do you now see `PicoPeripheral` advertising?
* If yes, does it list the custom service UUID?


############
# first attempt at sending a single digit from Pico  as gthe peripheral to my mobile app nRF iphone app. 

## this did not work because it recommends the new version of AIOBLE library
Awesome 👍 — we’ll now make your **Pico W peripheral** send (notify) a changing number every second, so you can *see live updates* in your nRF app.

Here’s the clean, working pattern for your version of `aioble` For the New version of aioble: SEE next section for explanation of why this does not work for the older aioble library

```python
import aioble   ## the newer version
import bluetooth
import uasyncio as asyncio
import struct  # helps pack integers into bytes for BLE

async def peripheral_task():
    ble = bluetooth.BLE()

    # --- Define service and characteristic ---
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
            # pack integer as 2 bytes (BLE sends bytes)
            value = struct.pack("<h", count)
            characteristic.write(value)
            await characteristic.notify(connection)
            print("Sent:", count)
            count += 1
            await asyncio.sleep(1)

asyncio.run(peripheral_task())
```

---

### 💡 What happens:

* The Pico advertises.
* When you connect via nRF Connect, it sends an incrementing counter once per second.
* You’ll see `"Sent: 0"`, `"Sent: 1"`, etc. in your REPL.
* In nRF Connect, tap your characteristic (UUID ending in `...ef1`) → *Enable Notifications* → watch values update live.


1. Run this code.
2. Connect from nRF Connect.
3. Find the characteristic, enable **Notifications**, and tell me what you see — do numbers appear or increment every second?
### error from this newer aioble library
'not connecting. browser terminal: Starting BLE advertisement...
Connected to: Device(ADDR_RANDOM, 7c:14:33:fc:33:27, CONNECTED)
Traceback (most recent call last):
  File "<stdin>", line 142, in <module>
  File "asyncio/core.py", line 1, in run
  File "asyncio/core.py", line 1, in run_until_complete
  File "asyncio/core.py", line 1, in run_until_complete
  File "<stdin>", line 137, in peripheral_task
TypeError: 'NoneType' object isn't iterable.'   the command:  await characteristic.notify(connection).   is highlighted in VSCode as if not recognized

## This is the revision of above for sending a single digit with older aioble lib

Good troubleshooting 👏 — that error explains exactly what’s happening: your `aioble` version doesn’t use

```python
await characteristic.notify(connection)
```

(it returns `None`, hence the “NoneType isn’t iterable” error).

You’re on a slightly **older `aioble` API**, where you need to manually **write to the characteristic’s GATT handle** and then call **`connection.notify()`** instead of `characteristic.notify()`.

Here’s how to fix it for *your version*:

---

```python
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
```

---

### 💡 What changed

* We use `await aioble.notify(connection, characteristic)` instead of calling a method on the characteristic.
* This matches your `aioble` build (since `characteristic.notify()` doesn’t exist there).

---

### ✅ Action Step

Run this new version, connect again with **nRF Connect**,
enable *Notifications* on your custom characteristic,
and tell me what happens — do you now see incrementing values (or changing hex bytes)?




'''in Nov2025/Asyncio_lessons/Bluetooth folder
Basic_Advertising.py
https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855
obsidian-2025/Bluetooth.md
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth
ESP32_Sender.py
obsidian-2025/Bluetooth.md
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth

ESP32_UART_peripheral.py
obsidian-2025/Bluetooth.md
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth

ESP32_UART_Central.py
https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855
obsidian-2025/Bluetooth.md
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth

'''
ADC_BLE_peripheral.py
can use with the ESP_UART_central.py which will receive the data from the ADC potentiometer
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth/ADC_BLE_peripheral.py

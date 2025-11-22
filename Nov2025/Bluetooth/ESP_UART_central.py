'''
ESP32_Central.py
ESP32 Central (connects to peripheral and reads its messages)
The central scans for any BLE device advertising the Nordic UART Service UUID.
It connects, discovers TX/RX characteristics, and listens for notifications (like your "Ping 0", "Ping 1", etc.).
It also writes a short acknowledgment (ACK) message back to the peripheral.
Run the peripheral script first (the one named ESP32_UART).
On a second ESP32, run this central script.
https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855
obsidian-2025/Bluetooth.md
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth


'''
import aioble
import bluetooth
import uasyncio as asyncio

# ---- same Nordic UART UUIDs ----
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

async def central_task():
    print("Scanning for peripherals advertising UART service...")

    # Scan for 10 seconds
    async with aioble.scan(duration_ms=10000, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            name = result.name() or "?"
            print("Found:", name)
            if _UART_SERVICE_UUID in result.services():
                print("✅ Found UART peripheral:", name)
                device = result.device
                break
        else:
            print("❌ No UART device found.")
            return

    # Connect
    print("Connecting...")
    connection = await device.connect()
    print("Connected to:", device)

    # Discover UART service and characteristics
    service = await connection.service(_UART_SERVICE_UUID)
    rx = await service.characteristic(_UART_RX_CHAR_UUID)
    tx = await service.characteristic(_UART_TX_CHAR_UUID)

    # ---- Main communication loop ----
    while connection.is_connected():
        # Read notifications from peripheral (UTF-8)
        data = await tx.notified()
        message = data.decode("utf-8")
        # print(f"Received:, {message}" )
        print(f"Received:, {message}" )
        

        # Optionally send something back
        reply = f"ACK:{message}"
        rx.write(reply.encode("utf-8"))
        await asyncio.sleep(1)

asyncio.run(central_task())

''' program two is the central for ADC_BLE_peripheral.py
it RECEIVES  the ADC value from  the ADC_BLE_peripheral.py as in program one 
AND also will send the command  to turn on or off the led
Now have:
Peripheral sending data (ADC)
Central sending commands (LED control)
This is the same pattern  used for:
motors
servos
multi-axis joysticks
multi-sensor boards
This is the foundation of final BLE control system.

'''

import aioble
import bluetooth
import uasyncio as asyncio

# ---- same Nordic UART UUIDs ----
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

async def central_task():
    print("Scanning for peripherals advertising UART service...")

    # Scan for 10 seconds
    async with aioble.scan(duration_ms=10000, interval_us=30000, window_us=30000) as scanner:
        async for result in scanner:
            name = result.name() or "?"
            print("Found:", name)
            if _UART_SERVICE_UUID in result.services():
                print("✅ Found UART peripheral:", name)
                device = result.device
                break
        else:
            print("❌ No UART device found.")
            return

    # Connect
    print("Connecting...")
    connection = await device.connect()
    print("Connected to:", device)

    # Discover UART service and characteristics
    service = await connection.service(_UART_SERVICE_UUID)
    rx = await service.characteristic(_UART_RX_CHAR_UUID)
    tx = await service.characteristic(_UART_TX_CHAR_UUID)

    # ---- Main communication loop ----
    while connection.is_connected():
        # Read notifications from peripheral (UTF-8)
        data = await tx.notified()
        message = data.decode("utf-8")
        # print(f"Received:, {message}" )
        print(f"Received:, {message}" )
        
        rx.write("Ledon".encode())
        await asyncio.sleep(1)
        rx.write("Ledoff".encode())

        

        # Optionally send something back
        reply = f"ACK:{message}"
        rx.write(reply.encode("utf-8"))
        await asyncio.sleep(1)

asyncio.run(central_task())



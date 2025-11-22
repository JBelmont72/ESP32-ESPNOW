'''
this builds upon ESP_UART_central.py where i could turn the led on and off from the nRF app but not the browser because the terminal kept updating with new ADC values
I could have just stopped printing the adc values but i wanted to try button control.
create a Bluetooth LE central device using an ESP32 that connects to a peripheral device running the UART service.
The central scans for peripherals advertising the UART service, connects to one when found, and then enters a communication loop where it listens for notifications from the peripheral and sends back acknowledgments.
Additionally, implement functionality to control an LED on the peripheral device by sending "Ledon" and "Ledoff" commands based on a button press on the central device. 
create a button input on the central device to trigger LED control commands to the peripheral.  
use debouncing to ensure reliable button presses.   and asynchronously handle Bluetooth communication and button presses.   
'''
#https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855
import aioble
import bluetooth
import uasyncio as asyncio
from machine import Pin

button = Pin(15, Pin.IN, Pin.PULL_DOWN)

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

async def button_task(rx):
    last = 0
    while True:
        val = button.value()
        if val == 1 and last == 0:
            print("Button → LED ON")
            rx.write(b"LED_ON")
            last = 1
        elif val == 0 and last == 1:
            print("Button → LED OFF")
            rx.write(b"LED_OFF")
            last = 0
        await asyncio.sleep(0.05)   # debounce

async def receive_task(tx):
    while True:
        data = await tx.notified()
        print("Received:", data.decode())
        await asyncio.sleep(0)  # yield

async def central_task():
    print("Scanning...")
    async with aioble.scan(5000) as scanner:
        async for result in scanner:
            if _UART_SERVICE_UUID in result.services():
                device = result.device
                break

    print("Connecting...")
    conn = await device.connect()
    print("Connected!")

    service = await conn.service(_UART_SERVICE_UUID)
    rx = await service.characteristic(_UART_RX_CHAR_UUID)
    tx = await service.characteristic(_UART_TX_CHAR_UUID)

    # Run two tasks in parallel
    asyncio.create_task(button_task(rx))
    asyncio.create_task(receive_task(tx))

    # Keep the connection alive
    while conn.is_connected():
        await asyncio.sleep(1)

asyncio.run(central_task())

'''
The aioble.scan() function in MicroPython's aioble library is used to initiate a Bluetooth Low Energy (BLE) scan for advertising devices. It allows a central device to discover nearby peripherals. 
Usage: 
The aioble.scan() function is typically used within an async with statement, creating an asynchronous context manager that manages the scanning process. 
import asyncio
import aioble

async def scan_devices():
    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # Process each scan result
            print(f"Device found: {result.name()} ({result.device.addr})")
            # You can access other properties of the result object, like RSSI, advertising data, etc.

async def main():
    await scan_devices()

asyncio.run(main())

Parameters: 

• duration_ms: The duration of the scan in milliseconds. Set to 0 for an indefinite scan, or None to stop scanning. 
• interval_us: The interval between scan windows in microseconds. 
• window_us: The duration of each scan window in microseconds. 
• active: A boolean indicating whether to perform an active scan (requesting scan responses) or a passive scan. 

Functionality: 

• Initiates a scan: When aioble.scan() is called, the BLE radio starts listening for advertising packets from peripheral devices. 
• Returns a scanner object: The async with statement yields a scanner object, which is an asynchronous iterator. 
• Iterates through results: The async for result in scanner: loop iterates over each advertising packet received during the scan. 
• Provides scan results: Each result object contains information about the discovered device, including its name, address, RSSI, and advertising data. 
• Manages scan lifecycle: The async with statement ensures that the scan is properly started and stopped, even if errors occur. 

Key Concepts: 

• Asynchronous Programming: aioble.scan() is an asynchronous function, requiring the use of asyncio and await for proper execution. 
• Central and Peripheral Roles: aioble.scan() is used by a central device to discover peripherals. 
• Advertising Packets: Peripherals broadcast advertising packets to announce their presence, and the scanner detects these packets. 

AI responses may include mistakes.

'''
'''
The central/client/controller for the peripheral/server programs in /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth/Lesson_Peripheral.py
'''
import aioble
import bluetooth
import uasyncio as asyncio
from machine import Pin

# Button to send commands
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

# Nordic UART UUIDs
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_UUID      = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_UUID      = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")


# ------------------------------------------------------------
# Task: Button press sends LED_ON / LED_OFF
# ------------------------------------------------------------
async def button_task(rx_char):
    last = 0
    while True:
        val = button.value()
        if val == 1 and last == 0:
            print("Button → LED ON")
            rx_char.write(b"LED_ON")
            last = 1

        elif val == 0 and last == 1:
            print("Button → LED OFF")
            rx_char.write(b"LED_OFF")
            last = 0

        await asyncio.sleep(0.05)  # debounce + yield


# ------------------------------------------------------------
# Task: Receive notifications (ADC values, replies)
# ------------------------------------------------------------
async def receive_task(tx_char):
    while True:
        data = await tx_char.notified()
        print("Peripheral:", data.decode())
        await asyncio.sleep(0)


# ------------------------------------------------------------
# CENTRAL MAIN
# ------------------------------------------------------------
async def central_task():
    print("Scanning for peripherals...")

    device = None
    async with aioble.scan(4000) as scanner:
        async for result in scanner:
            if _UART_SERVICE_UUID in result.services():
                print("Found:", result.device)
                device = result.device
                break

    if not device:
        print("ERROR: No device found.")
        return

    print("Connecting...")
    conn = await device.connect()
    print("Connected!")

    # Discover UART service + characteristics
    service = await conn.service(_UART_SERVICE_UUID)
    rx = await service.characteristic(_UART_RX_UUID)   # send commands TO peripheral
    tx = await service.characteristic(_UART_TX_UUID)   # read notifications FROM peripheral

    # Start concurrent tasks
    asyncio.create_task(button_task(rx))
    asyncio.create_task(receive_task(tx))

    # Keep alive loop
    while conn.is_connected():
        await asyncio.sleep(1)


# Run it
asyncio.run(central_task())
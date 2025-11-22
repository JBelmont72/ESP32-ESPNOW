#central   ESP_UART_central_button_led.py
# use a button to send led on and led off
# first look at method aioble.scan()
#obsidian link:/Users/judsonbelmont/Vaults/myVault_1/2024/separate file to understand aioble.scan() function.md
#  https://chatgpt.com/c/68dae8c2-ab04-832c-97c0-13503c72dad3



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
        else:
            print("Device not found!")
            return

    print("Connecting...")
    conn = await device.connect()
    print("Connected!")

    service = await conn.service(_UART_SERVICE_UUID)
    rx = await service.characteristic(_UART_RX_CHAR_UUID)
    tx = await service.characteristic(_UART_TX_CHAR_UUID)

    # Run tasks in parallel
    asyncio.create_task(button_task(rx))
    asyncio.create_task(receive_task(tx))

    # Keep alive
    while conn.is_connected():
        await asyncio.sleep(1)



asyncio.run(central_task())


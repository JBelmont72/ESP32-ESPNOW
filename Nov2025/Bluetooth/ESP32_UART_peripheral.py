'''This is first version that is compatible with nRF and Bluefruit COnnect
https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855

ESP32_UART.py
this advertises and matches up to both nRF and BlueFruit Connect 
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

# ---- Standard Adafruit / Nordic UART UUIDs ----
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")  # phone → ESP32
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")  # ESP32 → phone

async def uart_peripheral():
    service = aioble.Service(_UART_SERVICE_UUID)

    rx = aioble.Characteristic(service, _UART_RX_CHAR_UUID, write=True)
    tx = aioble.Characteristic(service, _UART_TX_CHAR_UUID, read=True, notify=True)

    aioble.register_services(service)

    print("Advertising as Bluefruit-compatible UART...")
    async with await aioble.advertise(
        interval_us=200_000,
        name="ESP32_UART",
        services=[_UART_SERVICE_UUID],
    ) as connection:

        print("Connected to:", connection.device)
        count = 0

        while connection.is_connected():
            # ---- read any text sent from phone ----
            data = rx.read()
            if data:
                msg = data.decode("utf-8")
                print("Received from phone:", msg)

            # ---- send a short text back every 2 s ----
            reply = f"Ping {count}"
            tx.write(reply.encode("utf-8"))
            tx.notify(connection)
            print("Sent:", reply)
            count += 1
            await asyncio.sleep(2)

asyncio.run(uart_peripheral())
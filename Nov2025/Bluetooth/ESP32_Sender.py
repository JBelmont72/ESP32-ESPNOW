'''ESP32_sender.py
esp_sender 2d version 
this uses the bluetooth custom UUID and works for nRF mobile app but not the more discerning BlueFruit COnnect
https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855
obsidian-2025/Bluetooth.md
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Bluetooth
'''
import aioble
import bluetooth
import uasyncio as asyncio

async def peripheral_task():
    ble = bluetooth.BLE()

    service_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
    service = aioble.Service(service_uuid)

    char_uuid = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
    characteristic = aioble.Characteristic(service, char_uuid, read=True, notify=True)

    aioble.register_services(service)

    print("Starting BLE advertisement...")

    async with await aioble.advertise(
        interval_us=200_000,
        name="ESP32_Sender",
        services=[service_uuid],
    ) as connection:
        print("Connected to:", connection.device)
        count = 0
        while connection.is_connected():
            msg = f"Count: {count}"
            data = msg.encode("utf-8")
            characteristic.write(data)
            # ✅ call notify() directly, no await
            characteristic.notify(connection)
            print("Sent:", msg)
            count += 1
            await asyncio.sleep(1)

asyncio.run(peripheral_task())

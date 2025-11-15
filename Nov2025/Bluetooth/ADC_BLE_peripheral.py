''' 
ADC_BLE_peripheral.py
3 d verision   see the obsidian file for details
2025/Bluetooth.md	obsidian
https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855
'''
import aioble
import bluetooth
import uasyncio as asyncio
from machine import ADC, Pin

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)

# ---- keep smoothing value in a global variable ----
smoothed_val = 0

async def read_adc(alpha=0.8):
    global smoothed_val
    raw = adc.read()
    smoothed_val = alpha * smoothed_val + (1 - alpha) * raw
    return int(smoothed_val)

async def uart_peripheral():
    service = aioble.Service(_UART_SERVICE_UUID)
    rx = aioble.Characteristic(service, _UART_RX_CHAR_UUID, write=True)
    tx = aioble.Characteristic(service, _UART_TX_CHAR_UUID, read=True, notify=True)
    aioble.register_services(service)

    print("Advertising as ESP32_ADC...")
    async with await aioble.advertise(
        interval_us=200_000, name="ESP32_ADC", services=[_UART_SERVICE_UUID]
    ) as conn:

        print("Connected:", conn.device)
        while conn.is_connected():
            val = await read_adc()
            msg = f"ADC:{val}"
            tx.write(msg.encode("utf-8"))
            tx.notify(conn)
            print("Sent:", msg)
            await asyncio.sleep(0.5)

asyncio.run(uart_peripheral())
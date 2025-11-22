## the adc-ble-peripheral.py with the led object added which will be controlled by the central_uart.py
import aioble
import bluetooth
import uasyncio as asyncio
from machine import ADC, Pin
led=Pin(22,Pin.OUT)
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
            
            if rx.written(): # added this condition the the 'led' object above
                cmd = rx.read().decode("utf-8")
                print("Received command:", cmd)

                if cmd == "Ledon":
                    led.value(1)
                elif cmd == "Ledoff":
                    led.value(0)


asyncio.run(uart_peripheral())

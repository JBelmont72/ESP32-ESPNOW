''' These programs are not working for thew ADC value transmission  
program 1 stripped down
program 2 led peripheral/server that issues commands of led_on and led_off
program 3 ADC potentiometer on the peripheral/server 

'''
'''
class CommandProcessor:     # program one stripped down
    def __init__(self, led_pin):
        from machine import Pin
        self.led = Pin(led_pin, Pin.OUT)

    def process(self, cmd):
        """
        cmd is a UTF-8 string
        Example commands:
            LED_ON
            LED_OFF
            SET_FREQ 5
            HELP
        """
        parts = cmd.strip().split()
        if len(parts) == 0:
            return "ERR Empty"

        if parts[0] == "LED_ON":
            self.led.value(1)
            return "LED ON"

        if parts[0] == "LED_OFF":
            self.led.value(0)
            return "LED OFF"

        if parts[0] == "HELP":
            return "CMDS: LED_ON LED_OFF"

        return "ERR Unknown"
'''
# obsidian://open?vault=myVault_1&file=2025%2FBluetooth
# /Users/judsonbelmont/Vaults/myVault_1/2025/Bluetooth.md
# https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855
# this does not work for the ADC but does for LED
# import aioble       # program two led commands given by this peripheral/ server
# import bluetooth
# import uasyncio as asyncio
# from machine import ADC, Pin

# # -----------------
# # Command Processor peripheral, server runs on esp32 with the led on gpio pin 23
# # -----------------
# class CommandProcessor:
#     def __init__(self, led_pin):
#         self.led = Pin(led_pin, Pin.OUT)

#     def process(self, cmd):
#         parts = cmd.strip().split()
#         if len(parts) == 0:
#             return "ERR"

#         if parts[0] == "LED_ON":
#             self.led.value(1)
#             return "OK LED_ON"

#         if parts[0] == "LED_OFF":
#             self.led.value(0)
#             return "OK LED_OFF"

#         return "ERR UNKNOWN"
        

# # BLE UUIDs
# _UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
# _UART_RX_UUID      = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
# _UART_TX_UUID      = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

# adc = ADC(Pin(32))
# adc.atten(ADC.ATTN_11DB)

# processor = CommandProcessor(led_pin=23)

# async def peripheral_task():
#     # BLE services
#     service = aioble.Service(_UART_SERVICE_UUID)
#     rx = aioble.Characteristic(service, _UART_RX_UUID, write=True)
#     tx = aioble.Characteristic(service, _UART_TX_UUID, notify=True)
#     aioble.register_services(service)

#     print("Advertising…")
#     async with await aioble.advertise(
#         interval_us=200_000,
#         name="ESP32_CMD",
#         services=[_UART_SERVICE_UUID],
#     ) as conn:

#         print("Connected:", conn.device)

#         while conn.is_connected():
#             # -----------------------
#             # Notify ADC value
#             # -----------------------
#             val = adc.read()
#             tx.write(f"ADC {val}".encode())
#             tx.notify(conn)

#             # -----------------------
#             # Read and process commands
#             # -----------------------
#             if rx.written():
#                 cmd = rx.read().decode()
#                 print("CMD:", cmd)
#                 reply = processor.process(cmd)
#                 tx.write(reply.encode())
#                 tx.notify(conn)

#             await asyncio.sleep(0.3)

# asyncio.run(peripheral_task())

####### program three  has the potentiometer and sends data to the controller/client/central
# import aioble
# import bluetooth
# import uasyncio as asyncio
# from machine import ADC, Pin

# # -----------------
# # Command Processor
# # -----------------
# class CommandProcessor:
#     def __init__(self, led_pin):
#         self.led = Pin(led_pin, Pin.OUT)

#     def process(self, cmd):
#         parts = cmd.strip().split()
#         if len(parts) == 0:
#             return "ERR"

#         if parts[0] == "LED_ON":
#             self.led.value(1)
#             return "OK LED_ON"

#         if parts[0] == "LED_OFF":
#             self.led.value(0)
#             return "OK LED_OFF"

#         return "ERR UNKNOWN"
        

# # BLE UUIDs
# _UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
# _UART_RX_UUID      = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
# _UART_TX_UUID      = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)

# processor = CommandProcessor(led_pin=22)

# async def peripheral_task():
#     # BLE services
#     service = aioble.Service(_UART_SERVICE_UUID)
#     rx = aioble.Characteristic(service, _UART_RX_UUID, write=True)
#     tx = aioble.Characteristic(service, _UART_TX_UUID, notify=True)
#     aioble.register_services(service)

#     print("Advertising…")
#     async with await aioble.advertise(
#         interval_us=200_000,
#         name="ESP32_CMD",
#         services=[_UART_SERVICE_UUID],
#     ) as conn:

#         print("Connected:", conn.device)

#         while conn.is_connected():
#             # -----------------------
#             # Notify ADC value
#             # -----------------------
#             val = adc.read()
#             tx.write(f"ADC {val}".encode())
#             tx.notify(conn)

#             # -----------------------
#             # Read and process commands
#             # -----------------------
#             if rx.written():
#                 cmd = rx.read().decode()
#                 print("CMD:", cmd)
#                 reply = processor.process(cmd)
#                 tx.write(reply.encode())
#                 tx.notify(conn)

#             await asyncio.sleep(0.3)

# asyncio.run(peripheral_task())

### program 4 to fix the error in program 2 where the adc value is not transmitted,ADC worked but not the LED, ??problem with queuing?
# import aioble
# import bluetooth
# import uasyncio as asyncio
# from machine import ADC, Pin

# led = Pin(22, Pin.OUT)

# _UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
# _UART_RX_UUID      = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
# _UART_TX_UUID      = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)

# # =====================
# # ADC NOTIFY TASK
# # =====================
# async def adc_notify_task(conn, tx):
#     while conn.is_connected():
#         val = adc.read()
#         msg = f"ADC {val}"
#         tx.write(msg.encode())
#         try:
#             tx.notify(conn)
#         except OSError:
#             pass   # occurs if client hasn't enabled notifications yet
#         await asyncio.sleep(0.5)


# # =====================
# # COMMAND HANDLER TASK
# # =====================
# async def command_task(conn, rx, tx):
#     while conn.is_connected():
#         if rx.written():
#             cmd = rx.read().decode()
#             print("CMD:", cmd)

#             if cmd == "LED_ON":
#                 led.value(1)
#                 tx.write(b"OK LED_ON")
#                 tx.notify(conn)

#             elif cmd == "LED_OFF":
#                 led.value(0)
#                 tx.write(b"OK LED_OFF")
#                 tx.notify(conn)

#         await asyncio.sleep(0)


# # =====================
# # MAIN PERIPHERAL
# # =====================
# async def peripheral_task():
#     service = aioble.Service(_UART_SERVICE_UUID)

#     rx = aioble.Characteristic(
#         service, _UART_RX_UUID, write=True
#     )
#     tx = aioble.Characteristic(
#         service, _UART_TX_UUID, read=True, notify=True
#     )

#     aioble.register_services(service)

#     print("Advertising...")
#     async with await aioble.advertise(
#         interval_us=200_000,
#         name="ESP32_ADC",
#         services=[_UART_SERVICE_UUID]
#     ) as conn:

#         print("Connected:", conn.device)

#         # start tasks
#         asyncio.create_task(adc_notify_task(conn, tx))
#         asyncio.create_task(command_task(conn, rx, tx))

#         # keep connection alive
#         while conn.is_connected():
#             await asyncio.sleep(1)


# asyncio.run(peripheral_task())

import aioble
import bluetooth
import uasyncio as asyncio
from machine import ADC, Pin

led = Pin(22, Pin.OUT)

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_UUID      = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_UUID      = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)

# LOCK to protect BLE notify operations
notify_lock = asyncio.Lock()

# ================
# ADC TASK
# ================
async def adc_notify_task(conn, tx):
    while conn.is_connected():
        val = adc.read()
        msg = f"ADC {val}".encode()

        # write the value then attempt a notification; if notifications aren't enabled,
        # silently ignore errors so it doesn't spam the console.
        async with notify_lock:
            try:
                tx.write(msg)
                await tx.notify(conn)
            except OSError:
                # notifications not enabled; ignore silently
                pass
            except Exception:
                # ignore other errors (write issues, etc.)
                pass

        await asyncio.sleep(0.5)


# ================
# COMMAND HANDLER
# ================
async def command_task(conn, rx, tx):
    while conn.is_connected():

        if rx.written():
            cmd = rx.read().decode().strip()
            print("CMD:", cmd)

            if cmd == "LED_ON":
                led.value(1)
                resp = b"OK LED_ON"
            elif cmd == "LED_OFF":
                led.value(0)
                resp = b"OK LED_OFF"
            else:
                resp = b"ERR UNKNOWN"

            # write the response and attempt to notify; if notifications aren't enabled,
            # ignore errors silently.
            async with notify_lock:
                try:
                    tx.write(resp)
                    await tx.notify(conn)
                except OSError:
                    # notifications not enabled; ignore silently
                    pass
                except Exception:
                    # ignore other errors
                    pass

        await asyncio.sleep(0)


# ================
# MAIN PERIPHERAL
# ================
async def peripheral_task():
    service = aioble.Service(_UART_SERVICE_UUID)
    rx = aioble.Characteristic(service, _UART_RX_UUID, write=True)
    tx = aioble.Characteristic(service, _UART_TX_UUID, read=True, notify=True)

    aioble.register_services(service)

    print("Advertising...")
    async with await aioble.advertise(
        interval_us=200_000,
        name="ESP32_ADC",
        services=[_UART_SERVICE_UUID]
    ) as conn:

        print("Connected:", conn.device)

        asyncio.create_task(adc_notify_task(conn, tx))
        asyncio.create_task(command_task(conn, rx, tx))

        while conn.is_connected():
            await asyncio.sleep(1)


asyncio.run(peripheral_task())

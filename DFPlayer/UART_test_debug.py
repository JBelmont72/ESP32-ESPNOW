'''
DFPlayer/UART_test_debug.py
How to test
Wire the connections:
Pico GP0 → RX of USB-UART adapter or other microcontroller
Pico GP1 → TX of the other device
GND → GND
Upload and run uart_test_debug.py on your Pico.
Open two serial ports:
USB REPL (115200 baud) — to see [DEBUG] messages.
UART terminal (9600 baud) — to watch messages arrive and type replies.
Observe what happens:
Pico prints debug info in the USB REPL (so you can confirm it’s sending).
The other device should see UART Test Message #….
If you type into the UART terminal, Pico prints [DEBUG] Received: and echoes back.
'''
"""
UART TEST SCRIPT — DEBUG VERSION
--------------------------------
This script is to help you learn and verify that the Pico's UART works.

Features:
- Sends a message out the UART every 2 seconds.
- Echoes back any characters received.
- Prints debug info to the USB REPL so you can see what’s happening.

Pins:
    TX = GP0  (Pico sends data out here)
    RX = GP1  (Pico listens for data here)
    GND must be shared with the other device.

Baud rate: 9600 bps (both devices must match).
"""
## NOTE THIS WORKS AND CONFIRMS THAT UART IS PROPERLY CONFIGURED
from machine import UART, Pin
import time

# === SETUP UART ===
print("Setting up UART0 on TX=GP17, RX=GP13 at 9600 baud...")
uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(13))

print("UART setup complete.\n")
print("Tips:")
print(" - Connect GP0 -> RX on the other device")
print(" - Connect GP1 -> TX on the other device")
print(" - Connect GND -> GND\n")
print("Open a serial terminal at 9600 baud on the other side to see the test messages.")
print("---- STARTING UART TEST ----\n")

counter = 1

while True:
    # 1️⃣ Send a test message out the TX pin
    message = f"UART Test Message #{counter}\r\n"
    print(f"[DEBUG] Sending: {message.strip()}")
    uart.write(message)

    # 2️⃣ Check if anything came in on RX
    if uart.any():  # check how many bytes are waiting
        bytes_waiting = uart.any()
        print(f"[DEBUG] Bytes waiting to read: {bytes_waiting}")
        data = uart.read()  # read everything available
        if data:
            try:
                decoded = data.decode()  # try to decode to text
            # except UnicodeDecodeError:  # for regular python
            except Exception:# for micropython
                decoded = str(data)  # fallback to raw bytes
            print(f"[DEBUG] Received: {decoded}")
            uart.write(b"Echo: " + data + b"\r\n")

    counter += 1
    time.sleep(2)

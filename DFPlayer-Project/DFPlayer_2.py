'''

# MicroPython example: make the TX pin an input (tri-state)
from machine import Pin
tx_pin = Pin(17, Pin.IN)   # stop driving TX

Last program I used to test having the sd card formatted correctly


the third program below worked for testing an sd card with just two files on it.
🛠️ How to test
Wire it up
GP0 → RX of your USB-to-UART adapter or another Pico
GP1 → TX of the other device
GND → GND
Run this script on the Pico
Upload uart_test.py and run it.
Open a terminal
On your computer, connect to the USB-to-UART adapter (e.g., /dev/ttyUSB0 on Linux, COMx on Windows, or cu.usbserial on macOS).
Set baud = 9600.
Observe
You should see “Hello from Pico UART!” every 2 seconds.
If you type something in the terminal, it should echo back with “Echo: …”.
💡 Key UART concepts explained
TX (Transmit): Data leaving the Pico.
RX (Receive): Data coming into the Pico.
Baud rate: The speed of data transfer (must match on both sides).
uart.any(): Checks if bytes are waiting to be read.
uart.write(): Sends data out the TX pin.
uart.read(): Reads incoming bytes.
Would you like me to make a second version with debug prints explaining each step as it runs (useful the first time you test hardware)?

'''
"""
UART TEST SCRIPT
----------------
This script tests UART communication on a Raspberry Pi Pico or Pico W.

What it does:
1. Initializes UART0 at 9600 baud (default TX=GP0, RX=GP1 on the Pico).
2. Sends a test message every 2 seconds to confirm transmission is working.
3. Echoes back anything it receives — type something from the connected device,
   and it will send the same text back.

How to use:
- Connect a USB-to-UART adapter or another microcontroller to the Pico:
    Pico GP0 (TX) → RX on adapter
    Pico GP1 (RX) → TX on adapter
    GND → GND
- Open a serial terminal (115200 baud for USB REPL; 9600 baud for UART0).
- Observe messages being sent automatically.
- Type into the UART terminal; the Pico should echo what you type., only works if you have another device


2️⃣ How to run the program from VSCode
Connect your ESP32 to the Mac via USB (you should already see a port like /dev/cu.usbserial-xxxx).
In VSCode (with the Pymakr or MicroPico extension), make sure you’re connected to the ESP32 board.
Upload the file:
In Pymakr: click Upload.
In MicroPico: right-click uart_test.py → Upload and Run.
The script now runs on the ESP32.
At this point the board is repeatedly writing “Hello from ESP32 UART!” out of its hardware TX pin, not back to your VSCode terminal.
⚠️ Your VSCode terminal is connected to the USB REPL — it won’t show what’s being sent out the other hardware UART pins.
3️⃣ How to see what’s being sent
If you want to confirm it’s working:
Option A (loopback test):
Connect the ESP32 TX pin to its RX pin (cross them, TX → RX, RX → TX).
Then you can add to the code:
if uart.any():
    print(uart.read().decode())
Now whatever it transmits will come back and print to your VSCode terminal.
Option B (external USB-to-UART adapter):
Use a second USB-to-serial adapter on your Mac:
Connect ESP32 TX → adapter RX
ESP32 GND → adapter GND
Open a terminal on Mac:
screen /dev/cu.usbserial-xxxxx 9600
You’ll see the “Hello from ESP32 UART!” messages coming in.
4️⃣ For DFPlayer Mini testing
When you connect the DFPlayer Mini to the ESP32:
ESP32 TX → DFPlayer RX
ESP32 RX → DFPlayer TX (optional — DFPlayer can work without TX back)
GND to GND, VCC 5V
Then run the DFPlayer test program (the class we built earlier).
You do not use your Mac’s terminal to see the DFPlayer’s output — the DFPlayer doesn’t print anything back by default. It just plays audio.
✅ Bottom line
When instructions said:
Open a terminal … and you should see “Hello from Pico UART!”
That’s only if you’re listening on the other side of the TX pin — either by loopback or another USB-to-UART device.
Your VSCode REPL alone won’t show that.
Would you like me to give you an ESP32 UART loopback test version of the code (so you can see the TX text echoed in your VSCode terminal without extra hardware
"""

# from machine import UART, Pin
# import time

# # --- UART SETUP ---
# # UART0 is available on GP0 (TX) and GP1 (RX) by default.BUT on ESP32 conflicts with the REPL
# ## UART0 made the terminal go crazy with callbacks
# # 9600 baud is a safe, standard speed to start with.
# uart = UART(2, baudrate=9600, tx=Pin(0), rx=Pin(1))

# print("UART test started. Sending messages every 2 seconds...")

# while True:
#     # 1️⃣ Send a test message out the UART TX pin
#     uart.write("Hello from Pico UART!\r\n")

#     # 2️⃣ Check if any data is waiting to be read
#     if uart.any():  # uart.any() returns number of bytes waiting
#         data = uart.read()  # read everything available
#         if data:
#             print("Received via UART:", data)  # show in USB REPL
#             uart.write(b"Echo: " + data + b"\r\n")  # send back to sender

#     time.sleep(2)

# What does it mean that this program only runs once even though it is
# a while loop and the entire output is:
#     MicroPython v1.26.1 on 2025-09-11; Generic ESP32 module with ESP32
# Type "help()" for more information.
# >>> UART loopback test â connect TX to RX on these pins
# Received: b'\x00'
# from machine import UART, Pin
# import time

# # On ESP32, UART0 is typically TX=GPIO1, RX=GPIO3 (pins used by USB too)
# # Better to use UART1 or UART2 to avoid interfering with USB REPL.
# # Example: use UART1 with TX=17, RX=16
# uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))

# print("UART loopback test — connect TX to RX on these pins")

# while True:
#     msg = "Hello from ESP32 UART!\r\n"
#     uart.write(msg)
#     time.sleep(1)
#     if uart.any():
#         data = uart.read()
#         print("Received:", data)

'''
from machine import UART, Pin
import time

uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))

print("UART loopback test — connect TX to RX on GPIO17 <-> GPIO16")

while True:
    msg = "Hello from ESP32 UART!\r\n"
    uart.write(msg)
    time.sleep(1)

    data = uart.read()   # grab whatever is available
    if data:
        print("Received:", data)
'''


# Program #1
# from machine import UART, Pin   ## this worked !!!
# import time

# uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # adjust pins

# def send_cmd(cmd, param=0, feedback=1):
#     buf = bytearray(10)
#     buf[0] = 0x7E
#     buf[1] = 0xFF
#     buf[2] = 0x06
#     buf[3] = cmd
#     buf[4] = feedback & 1
#     buf[5] = (param >> 8) & 0xFF
#     buf[6] = param & 0xFF
#     checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
#     buf[7] = (checksum >> 8) & 0xFF
#     buf[8] = checksum & 0xFF
#     buf[9] = 0xEF
#     uart.write(buf)

# def read_response(timeout_ms=1000):
#     t0 = time.ticks_ms()
#     resp = b""
#     while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
#         if uart.any():
#             resp += uart.read()
#         time.sleep_ms(10)
#     return resp

# # Example sequence: request status (play track 1 but with feedback)
# send_cmd(0x06, 30, feedback=1)   # set volume, ask for feedback
# time.sleep(0.1)
# send_cmd(0x03, 12, feedback=1)    # play track 1, ask for feedback

# time.sleep(0.5)
# resp = read_response(1500)
# print("Raw response:", resp)
# # If resp non-empty (10-byte-ish frames), DFPlayer replies; print hex:
# print("Hex:", " ".join("{:02X}".format(b) for b in resp))


# send_cmd(0x42, feedback=1)  # request status
# time.sleep(0.5)
# resp = read_response(1000)
# print("Status:", " ".join("{:02X}".format(b) for b in resp))

#  All the .mp3 files are on the SD Card in DFPlayer mini and not in a folder, .0001.mp3 etc
#  this program is to ask for input of .mp3 files by number
#  Program #2
'''
from machine import UART, Pin   ## this worked 
import time

uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # adjust pins

def send_cmd(cmd, param=0, feedback=1):
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = feedback & 1
    buf[5] = (param >> 8) & 0xFF
    buf[6] = param & 0xFF
    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF
    uart.write(buf)

def read_response(timeout_ms=1000):
    t0 = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if uart.any():
            resp += uart.read()
        time.sleep_ms(10)
    return resp


try:
#     while True:
#         cmd = int(input('Enter the desired song number'))
#         cmdHex=hex(cmd)
# # Example sequence: request status (play track 1 but with feedback)
#         send_cmd(0x06, 30, feedback=1)   # set volume, ask for feedback
#         time.sleep(0.1)
#         # send_cmd(cmdHex, 1, feedback=1)    # play track 1, ask for feedback
#         send_cmd(cmd, 1, feedback=1)    # play track 1, ask for feedback

#         time.sleep(0.5)
#         resp = read_response(1500)
#         print("Raw response:", resp)
#         # If resp non-empty (10-byte-ish frames), DFPlayer replies; print hex:
#         print("Hex:", " ".join("{:02X}".format(b) for b in resp))


#         # send_cmd(0x42, feedback=1)  # request status
#         time.sleep(0.5)
#         resp = read_response(1000)
#         print("Status:", " ".join("{:02X}".format(b) for b in resp))

    while True:
        ## query number of files on sd card
        send_cmd(0x48, 0, feedback=1)
        
        print(read_response(1000))
        resp=read_response(1000)
        print("Hex Requested Number of files on sd card:", " ".join("{:02X}".format(b) for b in resp))

        cmd = int(input('Enter the desired song number: '))
        
        send_cmd(0x06, 30, feedback=1)   # set volume
        time.sleep(0.1)
        send_cmd(0x03, cmd, feedback=1)  # 0x03 = play track number cmd from root folder

        time.sleep(0.5)
        resp = read_response(1500)
        print("Raw response:", resp)
        print("Hex Requested:", " ".join("{:02X}".format(b) for b in resp))

        send_cmd(0x4C, 0, feedback=1)  # Query current file
        resp = read_response(1000)
        print("Now playing:", resp)
        print("Hex Now Playing:", " ".join("{:02X}".format(b) for b in resp))

        send_cmd(0x48, 0, feedback=1)
        
        print(read_response(1000))
        resp=read_response(1000)
        print("Hex Requested Number of files on sd card:", " ".join("{:02X}".format(b) for b in resp))

        
        
        
except KeyboardInterrupt:
    print('exiting DFPlayer')
    tx_pin = Pin(17,Pin.IN)
    



finally:
    print('Program ending')
    # from machine import Pin
    tx_pin = Pin(17, Pin.IN)   # stop driving TX1
'''


### 22 oct 2025 optimazed form of progarm _1.py above
'''
Let’s optimize, document, and add BUSY pin monitoring with LED feedback for your ESP32 setup.
Here’s a clean, well-commented version that:
✅ Flushes the UART buffer before and after commands
✅ Uses the BUSY pin (GPIO 5) to detect playback state
✅ Drives an LED that lights when BUSY = LOW (i.e. audio is playing)
✅ Plays .0001.mp3, .0002.mp3, etc. sequentially
✅ Has detailed inline comments explaining each step
'''
# Program #1 (Optimized DFPlayer Control with BUSY LED)
# ESP32 <-> DFPlayer Mini
#  - UART2 TX = GPIO17
#  - UART2 RX = GPIO16
#  - BUSY pin = GPIO5 (input from DFPlayer)
#  - LED tied to BUSY pin (lights when BUSY = LOW)

from machine import UART, Pin
import time

# ------------------------------ Works with 3.3 volt setup 
# Hardware Setup
# ------------------------------
uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))   # UART2 for DFPlayer
busy_pin = Pin(5, Pin.IN)                               # BUSY pin from DFPlayer (LOW = playing)

# ------------------------------
# Helper Functions
# ------------------------------
def clear_uart_buffer():
    """Empty any leftover bytes in UART receive buffer."""
    while uart.any():
        uart.read()

def send_cmd(cmd, param=0, feedback=1):
    """Send a 10-byte command frame to DFPlayer Mini."""
    buf = bytearray(10)
    buf[0] = 0x7E                     # Start byte
    buf[1] = 0xFF                     # Version
    buf[2] = 0x06                     # Length
    buf[3] = cmd                      # Command
    buf[4] = feedback & 1             # Feedback flag
    buf[5] = (param >> 8) & 0xFF      # High byte of parameter
    buf[6] = param & 0xFF             # Low byte of parameter
    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF   # High byte checksum
    buf[8] = checksum & 0xFF          # Low byte checksum
    buf[9] = 0xEF                     # End byte
    uart.write(buf)

def read_response(timeout_ms=1000):
    """Read any response from DFPlayer within timeout period."""
    t0 = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if uart.any():
            resp += uart.read()
        time.sleep_ms(10)
    return resp

def wait_for_not_busy(timeout=10000):
    """Wait until DFPlayer BUSY pin goes HIGH (finished playing)."""
    start = time.ticks_ms()
    while busy_pin.value() == 0:  # LOW means playing
        if time.ticks_diff(time.ticks_ms(), start) > timeout:
            print("⚠️ Timeout waiting for track to finish.")
            break
        time.sleep_ms(100)
    print("✅ DFPlayer is idle (BUSY pin HIGH).")

# ------------------------------
# Initialization
# ------------------------------
clear_uart_buffer()                   # Ensure buffer is empty before we start
print("🔄 UART buffer cleared.")

send_cmd(0x06, 30, feedback=1)        # Set volume = 30 (range 0–30)
time.sleep(0.1)

# ------------------------------
# Play Sequential Tracks
# ------------------------------
track = 1
while track <= 5:                     # Play first 5 tracks as example
    print(f"▶️ Playing track {track:04d}.mp3")
    send_cmd(0x03, track, feedback=1)  # Play track number
    time.sleep(0.2)

    # Read DFPlayer feedback (if any)
    resp = read_response(1500)
    if resp:
        print("Response:", " ".join("{:02X}".format(b) for b in resp))
    else:
        print("No response received.")

    # Wait while BUSY = LOW (track is playing)
    wait_for_not_busy()

    # Small pause before next track
    time.sleep(0.5)
    track += 1

# ------------------------------
# Shutdown and Final Buffer Check
# ------------------------------
send_cmd(0x16)                        # Stop playback (optional)
time.sleep(0.2)
clear_uart_buffer()                   # Empty any trailing data
print("🧹 UART buffer cleared at end of program.")
print("✅ Done — all tracks finished.")



'''
Perfect — this is a great working base to build from.
Let’s **optimize**, **document**, and **add BUSY pin monitoring with LED feedback** for your ESP32 setup.
Here’s a clean, well-commented version that:

✅ Flushes the UART buffer before and after commands
✅ Uses the BUSY pin (GPIO 5) to detect playback state
✅ Drives an LED that lights when BUSY = LOW (i.e. audio is playing)
✅ Plays `.0001.mp3`, `.0002.mp3`, etc. sequentially
✅ Has detailed inline comments explaining each step

---

### 🧠 Optimized & Commented Program

```python
# Program #1 (Optimized DFPlayer Control with BUSY LED)
# ESP32 <-> DFPlayer Mini
#  - UART2 TX = GPIO17
#  - UART2 RX = GPIO16
#  - BUSY pin = GPIO5 (input from DFPlayer)
#  - LED tied to BUSY pin (lights when BUSY = LOW)

from machine import UART, Pin
import time

# ------------------------------
# Hardware Setup
# ------------------------------
uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))   # UART2 for DFPlayer
busy_pin = Pin(5, Pin.IN)                               # BUSY pin from DFPlayer (LOW = playing)

# ------------------------------
# Helper Functions
# ------------------------------
def clear_uart_buffer():
    """Empty any leftover bytes in UART receive buffer."""
    while uart.any():
        uart.read()

def send_cmd(cmd, param=0, feedback=1):
    """Send a 10-byte command frame to DFPlayer Mini."""
    buf = bytearray(10)
    buf[0] = 0x7E                     # Start byte
    buf[1] = 0xFF                     # Version
    buf[2] = 0x06                     # Length
    buf[3] = cmd                      # Command
    buf[4] = feedback & 1             # Feedback flag
    buf[5] = (param >> 8) & 0xFF      # High byte of parameter
    buf[6] = param & 0xFF             # Low byte of parameter
    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF   # High byte checksum
    buf[8] = checksum & 0xFF          # Low byte checksum
    buf[9] = 0xEF                     # End byte
    uart.write(buf)

def read_response(timeout_ms=1000):
    """Read any response from DFPlayer within timeout period."""
    t0 = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if uart.any():
            resp += uart.read()
        time.sleep_ms(10)
    return resp

def wait_for_not_busy(timeout=10000):
    """Wait until DFPlayer BUSY pin goes HIGH (finished playing)."""
    start = time.ticks_ms()
    while busy_pin.value() == 0:  # LOW means playing
        if time.ticks_diff(time.ticks_ms(), start) > timeout:
            print("⚠️ Timeout waiting for track to finish.")
            break
        time.sleep_ms(100)
    print("✅ DFPlayer is idle (BUSY pin HIGH).")

# ------------------------------
# Initialization
# ------------------------------
clear_uart_buffer()                   # Ensure buffer is empty before we start
print("🔄 UART buffer cleared.")

send_cmd(0x06, 30, feedback=1)        # Set volume = 30 (range 0–30)
time.sleep(0.1)

# ------------------------------
# Play Sequential Tracks
# ------------------------------
track = 1
while track <= 5:                     # Play first 5 tracks as example
    print(f"▶️ Playing track {track:04d}.mp3")
    send_cmd(0x03, track, feedback=1)  # Play track number
    time.sleep(0.2)

    # Read DFPlayer feedback (if any)
    resp = read_response(1500)
    if resp:
        print("Response:", " ".join("{:02X}".format(b) for b in resp))
    else:
        print("No response received.")

    # Wait while BUSY = LOW (track is playing)
    wait_for_not_busy()

    # Small pause before next track
    time.sleep(0.5)
    track += 1

# ------------------------------
# Shutdown and Final Buffer Check
# ------------------------------
send_cmd(0x16)                        # Stop playback (optional)
time.sleep(0.2)
clear_uart_buffer()                   # Empty any trailing data
print("🧹 UART buffer cleared at end of program.")
print("✅ Done — all tracks finished.")
```

---

### 🔍 Notes & What’s New

| Function / Feature            | Description                                                                                                                                                               |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`clear_uart_buffer()`**     | Reads & discards any leftover bytes at start and end of run — prevents “ghost” responses from old sessions.                                                               |
| **`wait_for_not_busy()`**     | Polls the BUSY pin; program waits until playback completes. Includes a timeout for safety.                                                                                |
| **BUSY pin + LED**            | The LED tied to BUSY will **light when a track plays (BUSY=LOW)** and **turn off when idle (BUSY=HIGH)** — no extra code needed; it happens automatically through wiring. |
| **Response printing**         | Shows hex responses from DFPlayer when available, otherwise indicates none.                                                                                               |
| **Commented lines**           | Each section clearly states its function — easy to reuse later in classes or modular design.                                                                              |
| **Sequential track playback** | Plays `.0001.mp3`, `.0002.mp3`, etc., not inside a folder. You can increase the `while track <= 5` limit.                                                                 |

---

Would you like me to extend this to **automatically detect how many tracks** are present on the SD card (using DFPlayer’s “query number of tracks” command `0x48`) so it can play them all dynamically?

'''
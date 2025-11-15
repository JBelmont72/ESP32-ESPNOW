# this works with the 3.3 volt setup


# from machine import Pin, UART
# import time

# # --- Pin setup ---
# BUSY_PIN = Pin(5, Pin.IN)
# uart = UART(2, baudrate=9600, tx=17, rx=15)

# # --- DFPlayer command function ---
# def send_cmd(cmd, param=0, feedback=1):
#     buf = bytearray(10)
#     buf[0] = 0x7E
#     buf[1] = 0xFF
#     buf[2] = 0x06
#     buf[3] = cmd
#     buf[4] = feedback & 1
#     buf[5] = (param >> 8) & 0xFF
#     buf[6] = param & 0xFF
#     checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] +
#                          buf[4] + buf[5] + buf[6]) + 1
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

# # --- Start clean ---
# while uart.any():
#     uart.read()
# print("🧹 UART buffer cleared.")

# # --- Step 1: Request module version / query status ---
# send_cmd(0x42, feedback=1)   # query status
# time.sleep(0.3)
# r = read_response(500)
# print("🔍 Query status:", " ".join("{:02X}".format(b) for b in r))

# # --- Step 2: Play track 0001.mp3 ---
# print("🎵 Attempting to play 0001.mp3 ...")
# send_cmd(0x03, 1, feedback=1)
# time.sleep(0.5)
# r = read_response(1000)
# print("Response to play:", " ".join("{:02X}".format(b) for b in r))

# # --- Step 3: Monitor BUSY pin logic ---
# print("\nBUSY monitor (0 = playing, 1 = idle):")
# for i in range(20):
#     val = BUSY_PIN.value()
#     print(f"{i:02d}: BUSY={val}")
#     time.sleep(0.5)

# # --- Step 4: Query again after playback attempt ---
# send_cmd(0x42, feedback=1)
# time.sleep(0.3)
# r = read_response(1000)
# print("\n🔍 Post-play query:", " ".join("{:02X}".format(b) for b in r))

## lilygo t-display
from machine import Pin, UART
import time

uart = UART(2, baudrate=9600, tx=17, rx=2)

def send_cmd(cmd, param=0, feedback=0):
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
send_cmd(0x42, feedback=1)
time.sleep(0.5)
print(uart.read())

# Try a reset first
send_cmd(0x0C)
time.sleep(1)

# Set volume (0–30)
send_cmd(0x06, 25)
time.sleep(0.2)

# Play first track
send_cmd(0x03, 1)
print("Sent play command for 0001.mp3")

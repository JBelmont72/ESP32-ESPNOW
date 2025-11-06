'''
'''
from machine import UART, Pin
import time

# --- UART setup ---
uart = UART(2, baudrate=9600, tx=17, rx=13)
print("🎵 DFPlayer Mini Test: UART2 TX=17 RX=13 @ 9600 baud")

# --- DFPlayer command helper ---
def send_cmd(cmd, param=0, feedback=0):
    """Send a 10-byte command to DFPlayer Mini."""
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = feedback & 1
    buf[5] = (param >> 8) & 0xFF
    buf[6] = param & 0xFF
    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] +
                         buf[4] + buf[5] + buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF
    uart.write(buf)

# --- Sequence: Reset, set volume, play track ---
print("🔄 Resetting DFPlayer...")
send_cmd(0x0C)  # reset
time.sleep(2)

print("🔊 Setting volume to 25 (range 0–30)...")
send_cmd(0x06, 25)
time.sleep(0.5)

print("▶️  Playing track 0001.mp3 from root folder...")
send_cmd(0x03, 1)
time.sleep(5)

print("⏭️  Next track (0002.mp3)...")
send_cmd(0x01)  # next track
time.sleep(5)

print("⏹️  Stopping playback.")
send_cmd(0x16)
print("✅ Done.")

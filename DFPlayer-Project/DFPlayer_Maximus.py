'''
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/DFPlayer_Maximus.py
The DFPlayer has no “text output” like the loopback — the way to confirm it works is:
Send it a command over UART.
It responds by playing audio (if an SD card with MP3 files is inserted).
1️⃣ Wiring check (important!)
ESP32 TX (e.g. GPIO17) → DFPlayer RX
ESP32 RX (e.g. GPIO16) → DFPlayer TX (optional, for feedback)
ESP32 GND → DFPlayer GND
ESP32 5V or 3.3 volts work fine → DFPlayer VCC (DFPlayer needs 5V for audio output!)
Speaker → DFPlayer SPK+ and SPK− (or to  PAM8304 amp input).
Make sure the SD card is formatted FAT32, with files like 0001.mp3, 0002.mp3, etc. in the root or in properly named folders (01/001.mp3, 01/002.mp3 etc).
'''

from machine import UART, Pin
import time
import sys


# =====================================================
# DFPLAYER SETUP
# =====================================================
uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))
busy_pin = Pin(5, Pin.IN)    # DFPlayer BUSY pin (LOW = playing)


# =====================================================
# Clear DFPlayer UART buffer
# =====================================================
def clear_uart():
    """Dump unread DFPlayer bytes."""
    while uart.any():
        uart.read()
    print("UART buffer cleared.\n")


# =====================================================
# Send DFPlayer command
# =====================================================
def send_cmd(cmd, param=0, feedback=0):
    """Send the 10-byte DFPlayer command frame."""
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

    print("Sending:", " ".join(f"{b:02X}" for b in buf))
    uart.write(buf)


# =====================================================
# DFPlayer Commands
# =====================================================
def play_track(n):
    print(f"▶️  Play {n:04d}.mp3")
    stop()              # this uses the stop() to reset so  new track works
    time.sleep_ms(120)  # DFPlayer needs gap
    clear_uart()
    send_cmd(0x03, n)


def pause():
    print("⏸️ Pause")
    send_cmd(0x0E)


def resume():
    print("▶️ Resume")
    send_cmd(0x0D)


def stop():
    print("⛔ Stop")
    send_cmd(0x16)


def set_volume(v):
    v = max(0, min(30, v))
    print(f"🔊 Volume {v}")
    send_cmd(0x06, v)


# =====================================================
# Busy Pin Checker (optional)
# =====================================================
def is_playing():
    """Return True if DFPlayer is currently playing."""
    return busy_pin.value() == 0


def wait_until_idle():
    """Block until track finishes."""
    print("⌛ Waiting for playback to finish...")
    while is_playing():
        time.sleep(0.1)
    print("✓ Track done.\n")


# =====================================================
# Menu
# =====================================================
def print_menu():
    print("""
Commands:
  p <n>   → Play track n (ex: p 1)
  v <n>   → Volume 0–30
  pause   → Pause playback
  resume  → Resume playback
  stop    → Stop
  exit    → Quit program
""")


# =====================================================
# MAIN PROGRAM LOOP
# =====================================================
clear_uart()
set_volume(20)

print("DFPlayer Ready.")
print_menu()

try:
    while True:
        cmd = input(">>> ").strip()

        # PLAY
        if cmd.startswith("p "):
            try:
                n = int(cmd.split()[1])
                play_track(n)
            except:
                print("Invalid track.")

        # VOLUME
        elif cmd.startswith("v "):
            try:
                vol = int(cmd.split()[1])
                set_volume(vol)
            except:
                print("Invalid volume.")

        # PAUSE
        elif cmd == "pause":
            pause()

        # RESUME
        elif cmd == "resume":
            resume()

        # STOP
        elif cmd == "stop":
            stop()

        # EXIT
        elif cmd == "exit":
            print("Exiting program.")
            stop()
            break

        else:
            print("Unknown command.")
            print_menu()

except KeyboardInterrupt:
    print("\nCtrl+C → stopping DFPlayer.")
    stop()
except Exception as e:
    print("Error:", e)
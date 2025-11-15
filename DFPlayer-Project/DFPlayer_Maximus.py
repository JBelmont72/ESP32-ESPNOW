'''
very simple UART test directly against the DFPlayer.
The DFPlayer has no “text output” like the loopback — the way to confirm it works is:
Send it a command over UART.
It responds by playing audio (if an SD card with MP3 files is inserted).
1️⃣ Wiring check (important!)
ESP32 TX (e.g. GPIO17) → DFPlayer RX
ESP32 RX (e.g. GPIO16) → DFPlayer TX (optional, for feedback)
ESP32 GND → DFPlayer GND
ESP32 5V → DFPlayer VCC (DFPlayer needs 5V for audio output!)
Speaker → DFPlayer SPK+ and SPK− (or to your PAM8304 amp input).
Also make sure the SD card is formatted FAT32, with files like 0001.mp3, 0002.mp3, etc. in the root or in properly named folders (01/001.mp3, 01/002.mp3 etc).
'''


from machine import UART, Pin
import time
import sys

# -------------------------------
# DFPlayer Setup
# -------------------------------

uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))
busy_pin = Pin(5, Pin.IN)     # DFPlayer BUSY pin (LOW = playing)

# -------------------------------
# Helper: Clear UART garbage
# -------------------------------
def clear_uart():
    """Dump any unread bytes in DFPlayer UART buffer."""
    while uart.any():
        uart.read()
    print("UART buffer cleared.\n")

# -------------------------------
# DFPlayer Command Sender
# -------------------------------
def send_cmd(cmd, param=0, feedback=0):
    """Send a 10-byte DFPlayer command frame."""
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

# -------------------------------
# DFPlayer Commands
# -------------------------------
def play_track(n):
    print(f"▶️  Playing track {n:04d}.mp3")
    send_cmd(0x03, n)

def pause():
    print("⏸️ Paused")
    send_cmd(0x0E)

def resume():
    print("▶️ Resume")
    send_cmd(0x0D)

def stop():
    print("⛔ Stopped")
    send_cmd(0x16)

def set_volume(v):
    v = max(0, min(30, v))
    print(f"🔊 Volume set to {v}")
    send_cmd(0x06, v)

# -------------------------------
# Wait until track finishes
# -------------------------------
def wait_until_idle():
    """Block until BUSY pin returns HIGH."""
    print("⌛ Waiting for track to finish...")
    while busy_pin.value() == 0:
        time.sleep(0.1)
    print("✓ Track finished.\n")

# -------------------------------
# Interactive terminal menu
# -------------------------------

def print_menu():
    print(
        "\nCommands:\n"
        "  p <n>  → Play track n (ex: p 1)\n"
        "  v <n>  → Volume 0–30\n"
        "  pause  → Pause playback\n"
        "  resume → Resume playback\n"
        "  stop   → Stop playback\n"
        "  exit   → Quit program\n"
    )

# -------------------------------
# MAIN PROGRAM
# -------------------------------

clear_uart()
set_volume(20)

print("DFPlayer Ready.")
print_menu()

while True:
    try:
        cmd = input(">>> ").strip()

        # --------------------------
        # PLAY COMMAND
        # --------------------------
        if cmd.startswith("p "):
            try:
                n = int(cmd.split()[1])
                clear_uart()
                play_track(n)
            except:
                print("Invalid track number.")

        # --------------------------
        # SET VOLUME
        # --------------------------
        elif cmd.startswith("v "):
            try:
                vol = int(cmd.split()[1])
                set_volume(vol)
            except:
                print("Invalid volume.")

        # --------------------------
        # PAUSE
        # --------------------------
        elif cmd == "pause":
            pause()

        # --------------------------
        # RESUME
        # --------------------------
        elif cmd == "resume":
            resume()

        # --------------------------
        # STOP
        # --------------------------
        elif cmd == "stop":
            stop()

        # --------------------------
        # EXIT PROGRAM
        # --------------------------
        elif cmd == "exit":
            print("Exiting program.")
            stop()
            break

        # --------------------------
        # UNKNOWN INPUT
        # --------------------------
        else:
            print("Unknown command.")
            print_menu()

    except KeyboardInterrupt:
        print("\nCtrl+C detected → stopping DFPlayer.")
        stop()
        break
    except Exception as e:
        print("Error:", e)  
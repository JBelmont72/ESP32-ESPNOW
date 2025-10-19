'''


'''
from machine import UART, Pin
import time

uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # Adjust pins as needed

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
    send_cmd(0x06, 25, feedback=1)   # Set volume to mid-level (0–30)
    time.sleep(0.2)
    print("Ready. Enter track numbers 1–255 from folder '01'.")

    while True:
        cmd = input("Enter track number (1–255): ").strip()
        if not cmd:
            continue
        if cmd.lower() in ("q", "quit", "exit"):
            break
        try:
            track = int(cmd)
            if not 1 <= track <= 255:
                print("⚠️  Track must be 1–255.")
                continue
            # Folder 01, file number = track
            param = (1 << 8) | track
            send_cmd(0x0F, param, feedback=1)
            print(f"🎵 Playing /01/{track:04d}.mp3")
            time.sleep(0.5)
            resp = read_response(1500)
            if resp:
                print("Response:", " ".join("{:02X}".format(b) for b in resp))
        except ValueError:
            print("Please enter a valid number.")

except KeyboardInterrupt:
    print("\nExiting DFPlayer...")

finally:
    tx_pin = Pin(17, Pin.IN)
    print("Program ended.")

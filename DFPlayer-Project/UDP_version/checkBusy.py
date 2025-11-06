'''
/Users/judsonbelmont/Vaults/myVault_1/2024/UDP DFPlayer.md path to Obsidian file
'''




from machine import UART, Pin
import time

# UART setup (same as working script)
uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(13))
busy = Pin(5, Pin.IN)

def clear_uart():
    while uart.any():
        uart.read()

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

def read_resp(timeout_ms=1000):
    t0 = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if uart.any():
            resp += uart.read()
        time.sleep_ms(10)
    return resp

print("Clearing UART buffer...")
clear_uart()
time.sleep(0.2)

print("Setting volume to 25 (with feedback)...")
send_cmd(0x06, 25, feedback=1)
time.sleep(0.2)
print("Response:", read_resp(500))

print("Playing track 1 (with feedback)...")
send_cmd(0x03, 1, feedback=1)
time.sleep(0.05)
print("BUSY now reads:", busy.value())
print("Response after play:", read_resp(1500))

# wait while playing and poll busy
start = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start) < 15000:
    print("BUSY =", busy.value())
    if uart.any():
        print("UART data:", uart.read())
    time.sleep(0.5)

print("Done.")

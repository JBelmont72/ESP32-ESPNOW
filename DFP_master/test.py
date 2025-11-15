'''


'''
# from machine import Pin, UART
# from time import sleep

# # Setup serial to DFPlayer
# uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # adjust pins to your wiring

# # Setup BUSY pin (read-only)
# busy = Pin(13, Pin.IN)

# def send_cmd(cmd, param1=0, param2=0):
#     # Build DFPlayer command packet
#     buf = bytearray([
#         0x7E, 0xFF, 0x06, cmd, 0x00,
#         (param1 << 8) | param2 >> 8, param2 & 0xFF, 0xFE, 0xBA, 0xEF
#     ])
#     uart.write(buf)

# def set_volume(level):
#     send_cmd(0x06, 0, level)
#     sleep(0.2)

# def play_track(track_num):
#     send_cmd(0x03, 0, track_num)
#     sleep(0.2)

# print("Setting volume to 25...")
# set_volume(25)

# print("Playing track 0001...")
# play_track(1)

# # Monitor BUSY pin
# for i in range(20):
#     print("BUSY:", "LOW (playing)" if busy.value() == 0 else "HIGH (idle)")
#     sleep(0.5)

###########
# from machine import UART, Pin
# import time

# uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # adjust pins if necessary
# busy = Pin(13, Pin.IN)  # change to the pin you're using for BUSY

# def send_cmd(cmd, param=0, feedback=1):
#     buf = bytearray(10)
#     buf[0] = 0x7E; buf[1] = 0xFF; buf[2] = 0x06
#     buf[3] = cmd
#     buf[4] = feedback & 1
#     buf[5] = (param >> 8) & 0xFF
#     buf[6] = param & 0xFF
#     checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
#     buf[7] = (checksum >> 8) & 0xFF
#     buf[8] = checksum & 0xFF
#     buf[9] = 0xEF
#     uart.write(buf)

# def read_response(timeout_ms=500):
#     t0 = time.ticks_ms()
#     resp = b""
#     while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
#         if uart.any():
#             resp += uart.read()
#         time.sleep_ms(10)
#     return resp

# # Set volume and play folder track 1
# send_cmd(0x06, 25, feedback=1)  # volume 25
# time.sleep(0.2)
# # Play folder 01 track 1 (param = (folder<<8) | track)
# param = (1 << 8) | 1
# send_cmd(0x0F, param, feedback=1)
# time.sleep(0.2)

# # Print initial responses
# print("Initial UART:", read_response(500))

# # Poll BUSY for 10 seconds, print transitions and UART
# start = time.time()
# prev = busy.value()
# print("BUSY start:", prev)
# while time.time() - start < 10:
#     cur = busy.value()
#     if cur != prev:
#         print("BUSY changed:", prev, "->", cur)
#         prev = cur
#     if uart.any():
#         r = read_response(200)
#         print("UART:", " ".join("{:02X}".format(b) for b in r))
#     time.sleep(0.1)

# print("Done.")



# Paste and run on your ESP32 - adjust pins if needed
# from machine import UART, Pin
# import time

# uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # keep your current pins
# print("Listening for bytes from DFPlayer... Ctrl-C to stop")

# try:
#     while True:
#         if uart.any():
#             b = uart.read()
#             # print readable hex
#             print("RX:", " ".join("{:02X}".format(x) for x in b))
#         time.sleep(0.05)
# except KeyboardInterrupt:
#     print("Stopped.")



from machine import UART, Pin
import time

uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # adjust if needed

buf = bytearray()

def find_frames(b):
    frames = []
    i = 0
    while i < len(b):
        # find start byte
        if b[i] != 0x7E:
            i += 1
            continue
        # need at least 10 bytes for full frame
        if i + 10 <= len(b):
            if b[i+9] == 0xEF:
                frames.append(bytes(b[i:i+10]))
                i += 10
                continue
            else:
                # bad frame: skip this start
                i += 1
                continue
        else:
            break
    return frames, b[i:]  # leftover

print("Listening for complete DFPlayer frames...")
while True:
    if uart.any():
        data = uart.read()
        if not data:
            continue
        buf.extend(data)
        frames, leftover = find_frames(buf)
        buf = bytearray(leftover)  # keep partial tail
        for f in frames:
            print("FRAME:", " ".join("{:02X}".format(x) for x in f))
    time.sleep(0.02)

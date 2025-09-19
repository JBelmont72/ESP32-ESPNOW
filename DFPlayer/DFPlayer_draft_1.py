''' 
DFPlayer_draft1.py
'''
from machine import Pin, UART
import time

# === UART for DFPlayer ===
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))  # adjust pins

def send_cmd(cmd, param=0, feedback=0):
    """Send DFPlayer command with checksum."""
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = feedback
    buf[5] = (param >> 8) & 0xFF
    buf[6] = param & 0xFF

    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF
    uart.write(buf)

# === Keypad setup (4x3) ===
rows = [Pin(x, Pin.OUT) for x in (12, 13, 14, 15)]  # adjust pins
cols = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in (16, 17, 18)]

keys = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']
]

def read_keypad():
    for r in range(4):
        rows[r].value(1)
        for c in range(3):
            if cols[c].value() == 1:
                rows[r].value(0)
                return keys[r][c]
        rows[r].value(0)
    return None

# === Menu logic with buffer ===
volume = 20
paused = False
track_buffer = ""
last_digit_time = 0
digit_timeout = 2  # seconds

def play_track(track):
    global paused
    send_cmd(0x03, track)
    paused = False
    print("Play track", track)

def handle_key(k):
    global volume, paused, track_buffer, last_digit_time

    if k.isdigit():
        if k == '0' and track_buffer == "":  # zero alone = pause/resume
            if paused:
                send_cmd(0x0D)  # play/resume
                paused = False
                print("Resume")
            else:
                send_cmd(0x0E)  # pause
                paused = True
                print("Pause")
        else:
            # store digit in buffer
            track_buffer += k
            last_digit_time = time.time()
            print("Buffer:", track_buffer)
            # If 2 digits entered, play immediately
            if len(track_buffer) == 2:
                play_track(int(track_buffer))
                track_buffer = ""

    elif k == '*':  # volume down
        if volume > 0:
            volume -= 1
            send_cmd(0x06, volume)
        print("Volume:", volume)

    elif k == '#':  # volume up
        if volume < 30:
            volume += 1
            send_cmd(0x06, volume)
        print("Volume:", volume)

# === Main loop ===
print("Ready. Use keypad to control DFPlayer.")
send_cmd(0x06, volume)  # initial volume

while True:
    k = read_keypad()
    if k:
        handle_key(k)
        time.sleep(0.3)  # debounce

    # Check timeout for single-digit entry
    if track_buffer and (time.time() - last_digit_time > digit_timeout):
        play_track(int(track_buffer))
        track_buffer = ""

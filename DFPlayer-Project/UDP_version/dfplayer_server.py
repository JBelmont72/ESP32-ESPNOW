'''
nov 16 2025   full dfplayer_server.py with status, volume, busy pin & led blink
non blocking version of dfplayer_server.py 
run this on esp32 , the client.py is run on python browser with python 3.13.9(.venv)
 

'''
# dfplayer_server.py — Full DFPlayer UDP Server with status, volume, busy pin & LED blink
# from machine import Pin, UART
# import socket
# import time

# # =========================
# # DFPLAYER SETUP
# # =========================
# uart = UART(2, baudrate=9600, tx=17, rx=16)
# busy = Pin(5, Pin.IN)     # DFPlayer BUSY pin (LOW = playing)
# led  = Pin(2, Pin.OUT)    # Status LED

# current_volume = 20
# last_track = None
# last_cmd = "NONE"

# # =========================
# # DFPLAYER LOW-LEVEL COMMAND
# # =========================
# def df_send(cmd, p1=0, p2=0):
#     """Send valid DFPlayer Mini command with checksum."""
#     buf = bytearray(10)
#     buf[0] = 0x7E
#     buf[1] = 0xFF
#     buf[2] = 0x06
#     buf[3] = cmd
#     buf[4] = 0x00     # no feedback
#     buf[5] = p1
#     buf[6] = p2

#     checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] +
#                          buf[4] + buf[5] + buf[6]) + 1

#     buf[7] = (checksum >> 8) & 0xFF
#     buf[8] = checksum & 0xFF
#     buf[9] = 0xEF

#     uart.write(buf)

# # =========================
# # HIGH-LEVEL COMMANDS
# # =========================

# def df_play(track):
#     global last_track, last_cmd
#     df_send(0x03, 0, track)
#     last_track = track
#     last_cmd = f"PLAY:{track}"

# def df_pause():
#     global last_cmd
#     df_send(0x0E)
#     last_cmd = "PAUSE"

# def df_resume():
#     global last_cmd
#     df_send(0x0D)
#     last_cmd = "RESUME"

# def df_stop():
#     global last_cmd
#     df_send(0x16)
#     last_cmd = "STOP"

# def df_volume(vol):
#     """Set volume 0–30."""
#     global current_volume, last_cmd
#     v = max(0, min(30, vol))
#     df_send(0x06, 0, v)
#     current_volume = v
#     last_cmd = f"VOLUME:{v}"

# # =========================
# # LED / BUSY STATUS HANDLER
# # =========================

# def update_led():
#     """Blink LED depending on DFPlayer state."""
#     if busy.value() == 0:
#         # Track is playing → fast blink
#         led.value(1)
#         time.sleep(0.05)
#         led.value(0)
#         time.sleep(0.05)
#     else:
#         # Idle → slow heartbeat blink
#         led.value(1)
#         time.sleep(0.3)
#         led.value(0)
#         time.sleep(1.2)

# # =========================
# # UDP SERVER SETUP
# # =========================

# def start_udp_server():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.settimeout(0.1)      # non-blocking for LED blinking
#     sock.bind(("0.0.0.0", 8888))
#     return sock

# # =========================
# # STATUS REPORT
# # =========================

# def get_status():
#     return (
#         f"BUSY:{busy.value()} "
#         f"VOLUME:{current_volume} "
#         f"LAST_CMD:{last_cmd} "
#         f"LAST_TRACK:{last_track}"
#     )

# # =========================
# # MAIN SERVER LOOP
# # =========================

# def main():
#     sock = start_udp_server()
#     print("📡 DFPlayer UDP Server running on port 8888")

#     while True:
#         # --- LED BLINK ALWAYS ---
#         update_led()

#         try:
#             data, addr = sock.recvfrom(128)
#         except OSError:
#             continue   # No incoming message, continue blinking

#         msg = data.decode().strip().upper()
#         print("📩", addr, msg)

#         # ----- Process Commands -----
#         if msg.startswith("PLAY:"):
#             track = int(msg.split(":")[1])
#             df_play(track)
#             sock.sendto(f"OK:PLAY {track}".encode(), addr)

#         elif msg.startswith("VOL:"):
#             vol = int(msg.split(":")[1])
#             df_volume(vol)
#             sock.sendto(f"OK:VOLUME {vol}".encode(), addr)

#         elif msg == "PAUSE":
#             df_pause()
#             sock.sendto(b"OK:PAUSE", addr)

#         elif msg == "RESUME":
#             df_resume()
#             sock.sendto(b"OK:RESUME", addr)

#         elif msg == "STOP":
#             df_stop()
#             sock.sendto(b"OK:STOP", addr)

#         elif msg == "STATUS":
#             sock.sendto(get_status().encode(), addr)

#         else:
#             sock.sendto(b"ERR:UNKNOWN_CMD", addr)




##### new  dfplayer_server.py file begins here #####
'''
non blocking version of dfplayer_server.py
'''
from machine import Pin, UART
import socket
import time

# =========================
# DFPLAYER SETUP
# =========================
uart = UART(2, baudrate=9600, tx=17, rx=16)
busy = Pin(5, Pin.IN)     # DFPlayer BUSY pin (LOW = playing)
led  = Pin(2, Pin.OUT)    # Status LED

current_volume = 20
last_track = None
last_cmd = "NONE"

# Non-blocking LED state
led_state = False
last_blink = time.ticks_ms()

# =========================
# DFPLAYER LOW-LEVEL COMMAND
# =========================
def df_send(cmd, p1=0, p2=0):
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = 0x00     # no feedback
    buf[5] = p1
    buf[6] = p2

    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] +
                         buf[4] + buf[5] + buf[6]) + 1

    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF

    uart.write(buf)

# =========================
# HIGH-LEVEL COMMANDS
# =========================
def df_play(track):
    global last_track, last_cmd
    df_send(0x03, 0, track)
    last_track = track
    last_cmd = f"PLAY:{track}"

def df_pause():
    global last_cmd
    df_send(0x0E)
    last_cmd = "PAUSE"

def df_resume():
    global last_cmd
    df_send(0x0D)
    last_cmd = "RESUME"

def df_stop():
    global last_cmd
    df_send(0x16)
    last_cmd = "STOP"

def df_volume(vol):
    global current_volume, last_cmd
    v = max(0, min(30, vol))
    df_send(0x06, 0, v)
    current_volume = v
    last_cmd = f"VOLUME:{v}"

# =========================
# LED / BUSY STATUS HANDLER (non-blocking)
# =========================
def update_led():
    global led_state, last_blink
    now = time.ticks_ms()
    if busy.value() == 0:
        interval = 50  # fast blink playing
    else:
        interval = 1200  # slow blink idle

    if time.ticks_diff(now, last_blink) >= interval:
        led_state = not led_state
        led.value(led_state)
        last_blink = now

# =========================
# UDP SERVER SETUP
# =========================
def start_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.05)      # short timeout for non-blocking LED
    sock.bind(("0.0.0.0", 8888))
    return sock

# =========================
# STATUS REPORT
# =========================
def get_status():
    return (
        f"BUSY:{busy.value()} "
        f"VOLUME:{current_volume} "
        f"LAST_CMD:{last_cmd} "
        f"LAST_TRACK:{last_track}"
    )

# =========================
# MAIN SERVER LOOP
# =========================
def main():
    sock = start_udp_server()
    print("📡 DFPlayer UDP Server running on port 8888")

    while True:
        # LED always updated
        update_led()

        # Handle incoming UDP messages
        try:
            data, addr = sock.recvfrom(128)
        except OSError:
            continue  # no data, continue loop

        msg = data.decode().strip().upper()
        print("📩", addr, msg)

        # ----- Process Commands -----
        if msg.startswith("PLAY:"):
            track = int(msg.split(":")[1])
            df_play(track)
            sock.sendto(f"OK:PLAY {track}".encode(), addr)

        elif msg.startswith("VOL:"):
            vol = int(msg.split(":")[1])
            df_volume(vol)
            sock.sendto(f"OK:VOLUME {vol}".encode(), addr)

        elif msg == "PAUSE":
            df_pause()
            sock.sendto(b"OK:PAUSE", addr)

        elif msg == "RESUME":
            df_resume()
            sock.sendto(b"OK:RESUME", addr)

        elif msg == "STOP":
            df_stop()
            sock.sendto(b"OK:STOP", addr)

        elif msg == "STATUS":
            sock.sendto(get_status().encode(), addr)

        else:
            sock.sendto(b"ERR:UNKNOWN_CMD", addr)
if __name__ == "__main__":
    main()  # for testing dfplayer_server.py independently
    
    
'''
Version below implements a second “exit” button on your ESP32 that stops the dfplayer_server.main() loop and returns control to main.py. Since MicroPython doesn’t really “un-import” a module, the cleanest way is to have your dfplayer_server.main() loop check a global running flag and exit if it’s cleared. Then main.py regains control and can let you press the short button again to restart the server.
dfplayer_server.py (with exit flag)
Add a global running variable and modify the main loop
'''
# At the top of dfplayer_server.py
running = True  # New: control loop from main.py

# =========================
# MAIN SERVER LOOP
# =========================
def main():
    global running
    sock = start_udp_server()
    print("📡 DFPlayer UDP Server running on port 8888")

    running = True  # ensure flag is True when starting
    while running:
        update_led()

        # Handle incoming UDP messages
        try:
            data, addr = sock.recvfrom(128)
        except OSError:
            continue  # no data, continue loop

        msg = data.decode().strip().upper()
        print("📩", addr, msg)

        # ----- Process Commands -----
        if msg.startswith("PLAY:"):
            track = int(msg.split(":")[1])
            df_play(track)
            sock.sendto(f"OK:PLAY {track}".encode(), addr)

        elif msg.startswith("VOL:"):
            vol = int(msg.split(":")[1])
            df_volume(vol)
            sock.sendto(f"OK:VOLUME {vol}".encode(), addr)

        elif msg == "PAUSE":
            df_pause()
            sock.sendto(b"OK:PAUSE", addr)

        elif msg == "RESUME":
            df_resume()
            sock.sendto(b"OK:RESUME", addr)

        elif msg == "STOP":
            df_stop()
            sock.sendto(b"OK:STOP", addr)

        elif msg == "STATUS":
            sock.sendto(get_status().encode(), addr)

        else:
            sock.sendto(b"ERR:UNKNOWN_CMD", addr)

    # Clean exit
    sock.close()
    print("DFPlayer UDP Server stopped")

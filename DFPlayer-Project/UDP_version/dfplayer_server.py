'''the dfplayer controlling program which will be called by the main.py

file in obsidian:  /Users/judsonbelmont/Vaults/myVault_1/2024/UDP DFPlayer.md
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/dfplayer_server.py
'''
'''
import socket
import utime
from machine import UART, Pin

# ===================== CONFIG =====================
UDP_PORT = 8888
# ===================================================

# ===================== DFPLAYER SETUP =====================
uart = UART(2, baudrate=9600, tx=17, rx=16)  # TX→RX, RX→TX
BUSY = Pin(5, Pin.IN)                         # BUSY pin (LOW = playing)
VOLUME = 20                                   # Default volume (0–30)
# ===========================================================

# -------------------- DFPLAYER COMMANDS --------------------
def send_cmd(cmd, param1=0, param2=0):
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = 0x00
    buf[5] = param1
    buf[6] = param2
    checksum = 0 - (0xFF + 0x06 + cmd + 0x00 + param1 + param2)
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF
    uart.write(buf)

def play_track(num):
    print("🎵 Playing track:", num)
    send_cmd(0x03, 0x00, num)
    
    # Wait briefly and check BUSY pin
    utime.sleep_ms(50)  # DFPlayer needs a moment to start
    busy_state = BUSY.value()
    if busy_state == 0:
        print("▶️ DFPlayer started playing, BUSY LOW")
    else:
        print("⚠️ DFPlayer did not start playing, BUSY HIGH — check track or SD card")

def set_volume(vol):
    global VOLUME
    vol = max(0, min(vol, 30))
    VOLUME = vol
    send_cmd(0x06, 0x00, vol)
    print("🔊 Volume set to:", vol)

def pause():
    send_cmd(0x0E)
    print("⏸️ Paused")

def resume():
    send_cmd(0x0D)
    print("▶️ Resumed")

def stop():
    send_cmd(0x16)
    print("⏹️ Stopped")

# -------------------- MAIN SERVER FUNCTION --------------------


def run_server(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, UDP_PORT))
    print(f"📡 UDP server listening on {ip}:{UDP_PORT}")
    set_volume(VOLUME)

    last_busy = BUSY.value()
    try:
        while True:
            # ------------------ CHECK FOR UDP MESSAGES ------------------
            if s:
                s.settimeout(0.1)
                try:
                    data, addr = s.recvfrom(128)
                    msg = data.decode().strip().upper()
                    print(f"📩 Received from {addr}: {msg}")

                    feedback = ""
                    if msg.startswith("PLAY:"):
                        track_num = int(msg.split(":")[1])
                        play_track(track_num)
                        feedback = f"Playing track {track_num}"
                    elif msg.startswith("VOL:"):
                        vol = int(msg.split(":")[1])
                        set_volume(vol)
                        feedback = f"Volume set to {vol}"
                    elif msg == "PAUSE":
                        pause()
                        feedback = "Paused"
                    elif msg == "RESUME":
                        resume()
                        feedback = "Resumed"
                    elif msg == "STOP":
                        stop()
                        feedback = "Stopped"
                    elif msg == "EXIT":
                        feedback = "Exiting server"
                        s.sendto(feedback.encode(), addr)
                        print("👋 Exiting on command...")
                        break
                    elif msg == "HELLO":
                        feedback = "Hello received!"
                    else:
                        feedback = f"Unknown command: {msg}"

                    # Send feedback back to client
                    if feedback:
                        s.sendto(feedback.encode(), addr)

                except OSError:
                    pass  # timeout, no message received

            # ------------------ BUSY PIN MONITOR ------------------
            current_busy = BUSY.value()
            if current_busy != last_busy:
                if current_busy == 0:
                    print("▶️ DFPlayer is playing (BUSY LOW)")
                else:
                    print("✅ DFPlayer idle (BUSY HIGH)")
                last_busy = current_busy

            utime.sleep_ms(50)

    finally:
        s.close()
        print("UDP server closed.")
'''
# dfplayer_server.py
import network
import socket
import time
from machine import UART, Pin

# ===================== CONFIG =====================
SSID = "NETGEAR48"
PASSWORD = "waterypanda901"
UDP_PORT = 8888
STATIC_IP = "10.0.0.24"
SUBNET = "255.255.255.0"
GATEWAY = "10.0.0.1"
# ===================================================

# ===================== DFPLAYER SETUP =====================
uart = UART(2, baudrate=9600, tx=17, rx=16)  # TX→RX, RX→TX
BUSY = Pin(5, Pin.IN)                         # BUSY pin
LED_BUSY = Pin(2, Pin.OUT)                    # Optional LED connected to BUSY

VOLUME = 20                                   # Default volume (0–30)
# ===========================================================

# ------------------ Helper Functions ------------------
def clear_uart():
    while uart.any():
        uart.read()

def send_cmd(cmd, param1=0, param2=0, feedback=1):
    """Send a 10-byte command to DFPlayer Mini"""
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = feedback & 1
    buf[5] = param1
    buf[6] = param2
    checksum = 0xFFFF - (buf[1]+buf[2]+buf[3]+buf[4]+buf[5]+buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF
    uart.write(buf)

def read_resp(timeout_ms=500):
    """Read DFPlayer response (optional)"""
    start = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        if uart.any():
            resp += uart.read()
        time.sleep_ms(10)
    return resp

def play_track(num):
    print("🎵 Playing track:", num)
    clear_uart()
    send_cmd(0x03, 0x00, num, feedback=1)
    time.sleep_ms(50)
    wait_for_play_start()

def set_volume(vol):
    global VOLUME
    vol = max(0, min(vol, 30))
    VOLUME = vol
    clear_uart()
    send_cmd(0x06, 0x00, vol, feedback=1)
    time.sleep_ms(50)
    print("🔊 Volume set to:", vol)

def pause():
    send_cmd(0x0E, feedback=1)
    print("⏸️ Paused")

def resume():
    send_cmd(0x0D, feedback=1)
    print("▶️ Resumed")

def stop():
    send_cmd(0x16, feedback=1)
    print("⏹️ Stopped")

def wait_for_play_start(timeout_ms=1000):
    """Wait until BUSY goes LOW indicating playback started"""
    start = time.ticks_ms()
    while BUSY.value() != 0:
        LED_BUSY.value(0)  # LED off when not playing
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            print("⚠️ Playback did not start (BUSY HIGH)")
            return False
        time.sleep_ms(10)
    print("▶️ Playback started (BUSY LOW)")
    LED_BUSY.value(1)  # LED on during play
    return True

def update_busy_led():
    """Call this periodically to reflect BUSY pin on LED"""
    LED_BUSY.value(0 if BUSY.value() else 1)

# ===================== WIFI SETUP =====================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, STATIC_IP))
    if not wlan.isconnected():
        print("📡 Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(0.5)
    if wlan.isconnected():
        print("✅ Wi-Fi connected:", wlan.ifconfig())
        return wlan
    else:
        print("❌ Could not connect to Wi-Fi.")
        return None

# ===================== MAIN =====================
def main():
    wlan = connect_wifi()
    if wlan is None:
        print("Exiting — no Wi-Fi")
        return

    ip = wlan.ifconfig()[0]
    print(f"📡 UDP server listening on {ip}:{UDP_PORT}")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, UDP_PORT))

    set_volume(VOLUME)

    while True:
        try:
            data, addr = s.recvfrom(128)
            msg = data.decode().strip().upper()
            print(f"📩 Received from {addr}: {msg}")

            if msg.startswith("PLAY:"):
                track_num = int(msg.split(":")[1])
                play_track(track_num)
            elif msg.startswith("VOL:"):
                set_volume(int(msg.split(":")[1]))
            elif msg == "PAUSE":
                pause()
            elif msg == "RESUME":
                resume()
            elif msg == "STOP":
                stop()
            elif msg == "EXIT":
                print("👋 Exiting on command...")
                break
            elif msg == "HELLO":
                print("👋 Hello received!")
            else:
                print("Unknown command:", msg)

            # Update LED according to BUSY pin
            update_busy_led()

        except Exception as e:
            print("⚠️ UDP error:", e)
            time.sleep(1)

    s.close()
    print("UDP server closed.")

# Run main
if __name__ == "__main__":
    main()

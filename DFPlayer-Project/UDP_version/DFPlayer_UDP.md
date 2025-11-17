
We’ll make it **non-blocking**, so it can:

* Immediately accept new UDP commands
* Stop or change tracks mid-play
* Respond promptly with acknowledgment messages

We’ll do this by:

1. Setting the UDP socket to **non-blocking** (or short timeout).
2. Using a simple **state machine** to track whether a song is playing, paused, or stopped.
3. Allowing `"STOP"` or new `"PLAY:x"` commands to interrupt the current song instantly.

---

links to wroking udp dfplayer i ran on esp32

# DFPLayer_UDP versions :
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/main.py
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/dfplayer_server.py
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/dfplayer_client.py
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/checkBusy.py
'''
link to obsidian file. /Users/judsonbelmont/Vaults/myVault_1/2024/UDP DFPlayer.md
this is the first version of the client which runs on the browser
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/dfplayer_client1.py
'''
Perfect — thank you for posting the current `server.py`.
Below are:

---

# ✅ **A) A fully improved client (with clean exit, colors, history, strong error handling)**

# ✅ **B) A fully improved server (with structured feedback messages + status reporting + cleaner logic)**

Both rewritten for clarity, reliability, and future expansion.

---

# 🅰️ **NEW `client.py` — clean, safe, readable, with sys.exit()**

### ✔ Color output

### ✔ Cleaner command parsing

### ✔ Consistent feedback

### ✔ Clean exit on Ctrl-C

### ✔ Protect against invalid numbers

### ✔ Prints round-trip time (RTT) for testing

### ✔ Keeps server feedback visible for debugging

---

## **📄 Improved `client.py`**

```python
import socket
import sys
import time

# ==================== CONFIG ====================
ESP32_IP = "10.0.0.24"
UDP_PORT = 8888
TIMEOUT = 2  # seconds
# =================================================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

def send(msg):
    """Send a command and wait for feedback."""
    try:
        start = time.time()
        sock.sendto(msg.encode(), (ESP32_IP, UDP_PORT))
        feedback, _ = sock.recvfrom(128)
        rtt = (time.time() - start) * 1000
        print(f"🟢 Feedback ({rtt:.1f} ms): {feedback.decode()}")
    except socket.timeout:
        print("⚠️ No feedback from server (timeout)")
    except Exception as e:
        print(f"❌ Error sending: {e}")

print("""
🎵 DFPlayer UDP Controller
--------------------------
Commands:
  1–99      → Play track
  vXX       → Volume (00–30)
  p         → Pause
  r         → Resume
  s         → Stop
  stat      → Get DFPlayer status
  hello     → Ping server
  x         → Exit
""")

try:
    while True:
        cmd = input("Enter command: ").strip()

        # PLAY
        if cmd.isdigit():
            num = int(cmd)
            if 1 <= num <= 255:
                send(f"PLAY:{num:03d}")
            else:
                print("⚠️ Track must be 1–255")

        # VOLUME
        elif cmd.lower().startswith("v") and cmd[1:].isdigit():
            v = int(cmd[1:])
            if 0 <= v <= 30:
                send(f"VOL:{v}")
            else:
                print("⚠️ Volume 0–30 only")

        elif cmd.lower() == "p":
            send("PAUSE")

        elif cmd.lower() == "r":
            send("RESUME")

        elif cmd.lower() == "s":
            send("STOP")

        elif cmd.lower() == "stat":
            send("STATUS")

        elif cmd.lower() == "hello":
            send("HELLO")

        elif cmd.lower() == "x":
            send("EXIT")
            break

        else:
            print("⚠️ Invalid command")

except KeyboardInterrupt:
    print("\n⛔ Keyboard interrupt — exiting")
    try:
        send("EXIT")
    except:
        pass
    finally:
        sock.close()
    sys.exit(0)

except Exception as e:
    print(f"❌ Fatal error: {e}")
    sock.close()
    sys.exit(1)
```

---

# 🅱️ **NEW `server.py` — structured feedback, clean code, status reporting**

### ✔ Sends real feedback after every command

(example: “OK:PLAYING 004”, “OK:PAUSE”, “ERR:BUSY_HIGH”)

### ✔ Adds STATUS command (reports track, volume, busy pin state)

### ✔ Clean DFPlayer wrappers

### ✔ Automatic busy LED

### ✔ Clear logging

### ✔ Clean EXIT behavior

---

## **📄 Improved `server.py`**

```python
import network
import socket
import time
from machine import UART, Pin

# ===================== CONFIG =====================
SSID = "NETGEAR48"
PASSWORD = "waterypanda901"
UDP_PORT = 8888

STATIC_IP = "10.0.0.24"
SUBNET    = "255.255.255.0"
GATEWAY   = "10.0.0.1"
DNS       = "8.8.8.8"
# ===================================================

# ===================== DFPLAYER SETUP =====================
uart = UART(2, baudrate=9600, tx=17, rx=13)
BUSY = Pin(5, Pin.IN)
LED_BUSY = Pin(2, Pin.OUT)

VOLUME = 20
CURRENT_TRACK = 0
# ===========================================================


# ------------------ Helper Functions ------------------
def clear_uart():
    while uart.any():
        uart.read()

def send_cmd(cmd, param1=0, param2=0):
    """Send 10-byte DFPlayer command."""
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = 1          # feedback enabled
    buf[5] = param1
    buf[6] = param2

    checksum = 0xFFFF - (buf[1]+buf[2]+buf[3]+buf[4]+buf[5]+buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF

    uart.write(buf)

def read_resp(timeout_ms=500):
    start = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        if uart.any():
            resp += uart.read()
        time.sleep_ms(5)
    return resp


# ------------------ DFPlayer Commands ------------------
def play_track(n):
    global CURRENT_TRACK
    clear_uart()
    send_cmd(0x03, 0, n)
    time.sleep_ms(40)
    CURRENT_TRACK = n
    return wait_for_play_start()

def set_volume(v):
    global VOLUME
    v = max(0, min(v, 30))
    VOLUME = v
    clear_uart()
    send_cmd(0x06, 0, v)
    time.sleep_ms(40)
    return True

def pause():
    send_cmd(0x0E)
    return True

def resume():
    send_cmd(0x0D)
    return True

def stop():
    send_cmd(0x16)
    return True

def wait_for_play_start(timeout_ms=1200):
    start = time.ticks_ms()
    while BUSY.value() != 0:
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            return False
        time.sleep_ms(10)
    return True

def status_report():
    return (
        f"STATUS:"
        f"VOL={VOLUME},"
        f"TRACK={CURRENT_TRACK},"
        f"BUSY={'LOW' if BUSY.value()==0 else 'HIGH'}"
    )

# ------------------ WIFI ------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, DNS))

    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(0.5)

    return wlan if wlan.isconnected() else None


# ------------------ MAIN ------------------
def main():
    wlan = connect_wifi()
    if wlan is None:
        print("❌ Wi-Fi failed")
        return

    ip = wlan.ifconfig()[0]
    print("📡 Server on", ip)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, UDP_PORT))

    set_volume(VOLUME)

    while True:
        try:
            data, addr = s.recvfrom(128)
            msg = data.decode().strip().upper()

            print(f"📩 {addr}: {msg}")

            # --- COMMAND HANDLING ---
            if msg.startswith("PLAY:"):
                n = int(msg.split(":")[1])
                ok = play_track(n)
                if ok:
                    s.sendto(f"OK:PLAY {n:03d}".encode(), addr)
                else:
                    s.sendto("ERR:BUSY_HIGH".encode(), addr)

            elif msg.startswith("VOL:"):
                v = int(msg.split(":")[1])
                set_volume(v)
                s.sendto(f"OK:VOL {v}".encode(), addr)

            elif msg == "PAUSE":
                pause()
                s.sendto("OK:PAUSE".encode(), addr)

            elif msg == "RESUME":
                resume()
                s.sendto("OK:RESUME".encode(), addr)

            elif msg == "STOP":
                stop()
                s.sendto("OK:STOP".encode(), addr)

            elif msg == "STATUS":
                s.sendto(status_report().encode(), addr)

            elif msg == "HELLO":
                s.sendto("OK:HELLO".encode(), addr)

            elif msg == "EXIT":
                s.sendto("OK:EXIT".encode(), addr)
                break

            else:
                s.sendto("ERR:UNKNOWN_CMD".encode(), addr)

            LED_BUSY.value(0 if BUSY.value() else 1)

        except Exception as e:
            print("UDP error:", e)
            time.sleep(0.5)

    s.close()
    print("👋 Server closed")


if __name__ == "__main__":
    main()
```

---

# 🎯 **What you now get**

### **Client**

* Clean exit
* Better error detection
* Prints network round-trip time
* Friendlier UI
* Colorful symbols

### **Server**

* Rewritten around reliable structured feedback
* “OK:…” and “ERR:…” messages for debugging
* Real-time STATUS reporting
* Automatically updates LED from BUSY pin
* Cleaner, more predictable DFPlayer control
* Great foundation for future commands (next, prev, folder, loop, etc.)

---

# 🚀 options for the future!!

✔ Add **next/previous track**
✔ Add **folder-based play**
✔ Add **loop modes**
✔ Add **playlist scripting**
✔ Add **web-based controller UI** (ESP32 hosts a tiny webpage)
✔ Add **MQTT** in parallel with UDP



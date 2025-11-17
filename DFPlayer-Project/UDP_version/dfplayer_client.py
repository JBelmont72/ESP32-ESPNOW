'''
notes 16 nov 2025   use python udp client to control dfplayer over wifi 
python 3.13.9(.venv).  interpreter path: /Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/.venv/bin/python3
ran client on old macbook pro m2 2023
ran  main.py on esp32 with short press importing dfplayer_server.py with dfplayer mini attached   


link to obsidian file. /Users/judsonbelmont/Vaults/myVault_1/2024/UDP DFPlayer.md
this is the first version of the client which runs on the browser
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/dfplayer_client.py
'''

# dfplayer_client.py —  DFPlayer UDP Client
import socket
import sys

# ==================== CONFIG ====================
ESP32_IP = "10.0.0.24"
UDP_PORT = 8888
TIMEOUT = 2       # Seconds to wait for server reply
SHOW_FEEDBACK = True   # <—— Toggle this ON/OFF easily
# =================================================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)


# ---------- Feedback-enabled send function ----------
def send(msg):
    sock.sendto(msg.encode(), (ESP32_IP, UDP_PORT))

    if not SHOW_FEEDBACK:
        return  # exit early → no need to wait for reply

    try:
        feedback, _ = sock.recvfrom(128)
        print("✅ Feedback:", feedback.decode().strip())
    except socket.timeout:
        print("⚠️ No feedback from server (timeout)")


# ---------- Optional microcontroller-style reset ----------
def optional_machine_reset():
    """Call this ONLY if running on Pico/ESP32, not PC."""
    try:
        import machine
        print("🔄 Performing hardware reset...")
        machine.reset()
    except ImportError:
        print("⚠️ machine.reset() not available on this platform.")


# ---------- Main Menu ----------
print("""
🎵 DFPlayer UDP Controller
--------------------------
Commands:
  01–99 → Play track
  vXX   → Set volume (00–30)
  p     → Pause
  r     → Resume
  s     → Stop
  x     → Exit client
  hello → Test connectivity
""")

# ---------- Main Loop ----------
try:
    while True:
        cmd = input("Enter command: ").strip()

        # ---- Play command 01-99 ----
        if cmd.isdigit() and 1 <= int(cmd) <= 99:
            send(f"PLAY:{int(cmd):02d}")

        # ---- Set volume vXX ----
        elif cmd.startswith("v") and cmd[1:].isdigit():
            vol = int(cmd[1:])
            send(f"VOL:{vol}")

        # ---- Basic controls ----
        elif cmd.lower() == "p":
            send("PAUSE")

        elif cmd.lower() == "r":
            send("RESUME")

        elif cmd.lower() == "s":
            send("STOP")

        # ---- Exit ----
        elif cmd.lower() == "x":
            send("EXIT")
            print("👋 Exiting client...")
            sock.close()
            sys.exit(0)

        # ---- Ping server ----
        elif cmd.lower() == "hello":
            send("HELLO")

        else:
            print("Invalid command. Try again.")

# ---------- Ctrl+C clean exit ----------
except KeyboardInterrupt:
    print("\n⚠️ Keyboard interrupt — exiting.")
    send("EXIT")
    sock.close()
    sys.exit(0)

# ---------- Catch-all errors ----------
except Exception as e:
    print(f"❌ Error: {e}")
    sock.close()
    sys.exit(1)
    
    
    
    


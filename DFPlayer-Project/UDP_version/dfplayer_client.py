'''
link to obsidian file. /Users/judsonbelmont/Vaults/myVault_1/2024/UDP DFPlayer.md
this is the first version of the client which runs on the browser
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/DFPlayer-Project/UDP_version/dfplayer_client1.py
'''
import socket

# ==================== CONFIG ====================
ESP32_IP = "10.0.0.24"  # server static IP
UDP_PORT = 8888
TIMEOUT = 2  # seconds to wait for server feedback
# =================================================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

def send(msg):
    sock.sendto(msg.encode(), (ESP32_IP, UDP_PORT))
    try:
        feedback, _ = sock.recvfrom(128)
        print("✅ Feedback:", feedback.decode())
    except socket.timeout:
        print("⚠️ No feedback from server")

print("""
🎵 DFPlayer UDP Controller
--------------------------
Commands:
  01–99 → Play track
  vXX   → Set volume (00–30)
  p     → Pause
  r     → Resume
  s     → Stop
  x     → Exit
  hello → Test connectivity
""")

while True:
    cmd = input("Enter command: ").strip()

    if cmd.isdigit() and 1 <= int(cmd) <= 99:
        send(f"PLAY:{int(cmd):02d}")
    elif cmd.startswith("v") and cmd[1:].isdigit():
        send(f"VOL:{int(cmd[1:])}")
    elif cmd.lower() == "p":
        send("PAUSE")
    elif cmd.lower() == "r":
        send("RESUME")
    elif cmd.lower() == "s":
        send("STOP")
    elif cmd.lower() == "x":
        send("EXIT")
        break
    elif cmd.lower() == "hello":
        send("HELLO")
    else:
        print("Invalid command. Try again.")

sock.close()
print("Client closed.")

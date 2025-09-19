'''DFPlayer_Keypad.py 
Class-Based DFPlayer + Keypad Control
This version does:
Volume control → * = down, # = up.
Root track selection → enter 2 digits (01–99).
Folder/track selection → press A–D (maps to folders 1–4), then enter 2 digits (01–99) for the track in that folder.
Extensible design with DFPlayer and Keypad classes, managed by a PlayerController.
CHAT  https://chatgpt.com/c/68c6e1a2-80ac-832e-9063-4c99fc53b034

'''
from machine import Pin, UART
import time

# ===================== DFPlayer Mini =====================
class DFPlayer:
    def __init__(self, uart_id=1, tx=17, rx=16, baud=9600):
        self.uart = UART(uart_id, baudrate=baud, tx=tx, rx=rx)
        self.volume = 20
        self.set_volume(self.volume)

    def _send_cmd(self, cmd, param=0):
        buf = bytearray(10)
        buf[0] = 0x7E
        buf[1] = 0xFF
        buf[2] = 0x06
        buf[3] = cmd
        buf[4] = 0x00
        buf[5] = (param >> 8) & 0xFF
        buf[6] = param & 0xFF
        buf[7] = buf[8] = 0x00  # checksum ignored here
        buf[9] = 0xEF
        self.uart.write(buf)

    def set_volume(self, vol):
        self.volume = max(0, min(30, vol))
        self._send_cmd(0x06, self.volume)

    def volume_up(self):
        self.set_volume(self.volume + 1)

    def volume_down(self):
        self.set_volume(self.volume - 1)

    def play_track(self, num):
        """Play track in root by number (1–2999)."""
        self._send_cmd(0x03, num)

    def play_folder_track(self, folder, num):
        """Play track num (1–255) from folder (1–99)."""
        param = (folder << 8) | num
        self._send_cmd(0x0F, param)

# ===================== Keypad =====================
class Keypad:
    def __init__(self, row_pins, col_pins, keys, threshold=3):
        self.rows = [Pin(r, Pin.OUT) for r in row_pins]
        self.cols = [Pin(c, Pin.IN, Pin.PULL_DOWN) for c in col_pins]
        self.keys = keys
        self.last_key = None
        self.stable_count = 0
        self.threshold = threshold

    def scan(self):
        for i, row in enumerate(self.rows):
            row.value(1)
            for j, col in enumerate(self.cols):
                if col.value() == 1:
                    key = self.keys[i][j]
                    if key == self.last_key:
                        self.stable_count += 1
                    else:
                        self.stable_count = 0
                        self.last_key = key
                    if self.stable_count >= self.threshold:
                        self.stable_count = 0
                        row.value(0)
                        return key
            row.value(0)
        return None

# ===================== Controller =====================
class PlayerController:
    def __init__(self):
        # Setup DFPlayer
        self.df = DFPlayer(uart_id=1, tx=17, rx=16)

        # Setup keypad
        row_pins = (14, 27, 26, 25)
        col_pins = (33, 32, 35, 34)
        keys = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]
        self.kp = Keypad(row_pins, col_pins, keys)

        # State
        self.track_buffer = ""
        self.folder_mode = None  # None = root, or 1–4 if A–D pressed

    def handle_key(self, key):
        print("Key pressed:", key)

        if key == "*":
            self.df.volume_down()
            print("Volume:", self.df.volume)

        elif key == "#":
            self.df.volume_up()
            print("Volume:", self.df.volume)

        elif key in "ABCD":
            self.folder_mode = {"A":1,"B":2,"C":3,"D":4}[key]
            self.track_buffer = ""  # reset buffer
            print(f"Folder mode {self.folder_mode}, enter 2-digit track.")

        elif key.isdigit():
            self.track_buffer += key
            if len(self.track_buffer) == 2:
                track_num = int(self.track_buffer)
                if self.folder_mode:
                    self.df.play_folder_track(self.folder_mode, track_num)
                    print(f"Playing folder {self.folder_mode}, track {track_num}")
                    self.folder_mode = None  # reset mode
                else:
                    self.df.play_track(track_num)
                    print(f"Playing root track {track_num}")
                self.track_buffer = ""

        else:
            # Ignore other keys, reset buffer
            self.track_buffer = ""
            self.folder_mode = None

    def run(self):
        print("🎵 Ready. Use keypad to control DFPlayer.")
        while True:
            key = self.kp.scan()
            if key:
                self.handle_key(key)
            time.sleep(0.05)

# ===================== Main =====================
if __name__ == "__main__":
    ctrl = PlayerController()
    ctrl.run()
'''
Organizing Files/Folders on the SD Card (Mac)
Root tracks: name 0001.mp3, 0002.mp3, … (/0001.mp3 → /0299.mp3).
Folders: name folders 01, 02, 03, …
Inside each: name tracks 001.mp3, 002.mp3, …
Example SD card layout:
/0001.mp3
/0002.mp3
/01/001.mp3
/01/002.mp3
/01/010.mp3
/02/001.mp3
/03/001.mp3
/04/005.mp3
Pressing 12 → plays /0012.mp3 (root).
Pressing A + 05 → plays /01/005.mp3.
Pressing B + 03 → plays /02/003.mp3.
👉 On macOS Finder:
Use Rename… → Format → Name + Counter → 001 to auto-format files with leading zeros.
Make sure folders are exactly two digits (01, 02, …).
✅ Now you have:
A clean class structure (DFPlayer, Keypad, PlayerController).
Extendable for OLED (just update handle_key() to also call oled.show_text(...)).
Ready for root and folder track selection
'''
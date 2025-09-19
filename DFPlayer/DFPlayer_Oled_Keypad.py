''' DFPlayer_Oled_Keypad.py
Adding Oled class to the MP3 player and the Keypad
Added an OLED class with a show_text(lines) method.
Right now, it just prints to console if ssd1306 isn’t enabled.
Once you copy ssd1306.py to your Pico/ESP32 and uncomment the lines, the text will appear on your 128×64 display.
Controller updates OLED every time you:
Change volume
Enter folder mode
Select a track
📌 Next Step
When you’re ready to wire the OLED (SDA→21, SCL→22 in this example), just:
Copy ssd1306.py to your board.
Uncomment:
from ssd1306 import SSD1306_I2C

and the uncomment the init
option i could extend the OLED class to also show a “live” keypad entry buffer (so if  press 1 it shows 1, then 12,



Why are rows outputs and columns inputs?
In a matrix keypad (like your 4×3 or 4×4), you have two sets of lines:
Rows (driven as outputs) → you actively set one row HIGH at a time.
Columns (read as inputs with pull-downs) → you check which column sees the HIGH signal.
👉 Example:
Set Row 1 = HIGH, all others = LOW.
If a button in Row 1 / Col 2 is pressed, Col 2 input will read HIGH.
That’s how you know which row+col pair is active → which key was pressed.
If you swapped them, you’d just flip the logic (drive columns, read rows). Either way works, but the convention is "rows = outputs, columns = inputs".
🔹 DFPlayer Class Annotations
Here’s a fully commented version of your DFPlayer class methods, showing exactly what’s happening in _send_cmd and others:

important:
Key Notes on Folder/Track Naming for DFPlayer (important on Mac!):
DFPlayer reads FAT32 filesystem.
Folders must be named 01, 02, … 99.
Inside folders, files must be named 001.mp3, 002.mp3, … up to 255.mp3.
In the root folder, files can be 0001.mp3 → 2999.mp3.
On Mac: when you copy files, macOS creates hidden files (._filename.mp3).
👉 These can confuse the DFPlayer.
So you should run this command in Terminal on your SD card:
dot_clean /Volumes/YOUR_SD_CARD_NAME
That removes all the hidden Apple metadata files.
Would you like me to merge your Keypad class + DFPlayer class into a single AudioPlayer controller class, so later you can add the OLED as just a new component? That way, the keypad selects folder/track, DFPlayer plays, and OLED just displays status.
'''

from machine import Pin, UART, I2C
import time
# If you already have the SSD1306 library:
# from ssd1306 import SSD1306_I2C

# ===================== OLED Display =====================
class OLED:
    def __init__(self, scl=22, sda=21, width=128, height=64):
        # Uncomment when ssd1306.py is available
        # i2c = I2C(0, scl=Pin(scl), sda=Pin(sda))
        # self.oled = SSD1306_I2C(width, height, i2c)
        self.width = width
        self.height = height
        self.oled = None  # placeholder until library is enabled

    def show_text(self, lines):
        """Display up to 4 lines of text (list of strings)."""
        if self.oled:
            self.oled.fill(0)
            for i, line in enumerate(lines):
                self.oled.text(line, 0, i*12)
            self.oled.show()
        else:
            # Fallback to console if OLED is not active
            print("OLED:", " | ".join(lines))

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
        buf[7] = buf[8] = 0x00
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
        self._send_cmd(0x03, num)

    def play_folder_track(self, folder, num):
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
        # DFPlayer
        self.df = DFPlayer(uart_id=1, tx=17, rx=16)

        # Keypad
        row_pins = (14, 27, 26, 25)
        col_pins = (33, 32, 35, 34)
        keys = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]
        self.kp = Keypad(row_pins, col_pins, keys)

        # OLED
        self.display = OLED(scl=22, sda=21)

        # State
        self.track_buffer = ""
        self.folder_mode = None

    def handle_key(self, key):
        if key == "*":
            self.df.volume_down()
            self.display.show_text([f"Volume: {self.df.volume}"])

        elif key == "#":
            self.df.volume_up()
            self.display.show_text([f"Volume: {self.df.volume}"])

        elif key in "ABCD":
            self.folder_mode = {"A":1,"B":2,"C":3,"D":4}[key]
            self.track_buffer = ""
            self.display.show_text([f"Folder {self.folder_mode}",
                                    "Enter 2-digit track"])

        elif key.isdigit():
            self.track_buffer += key
            if len(self.track_buffer) == 2:
                track_num = int(self.track_buffer)
                if self.folder_mode:
                    self.df.play_folder_track(self.folder_mode, track_num)
                    self.display.show_text([f"Folder {self.folder_mode}",
                                            f"Track {track_num}"])
                    self.folder_mode = None
                else:
                    self.df.play_track(track_num)
                    self.display.show_text([f"Root track {track_num}"])
                self.track_buffer = ""

        else:
            self.track_buffer = ""
            self.folder_mode = None

    def run(self):
        self.display.show_text(["🎵 DFPlayer Ready"])
        while True:
            key = self.kp.scan()
            if key:
                self.handle_key(key)
            time.sleep(0.05)

# ===================== Main =====================
if __name__ == "__main__":
    ctrl = PlayerController()
    ctrl.run()
###################
#DFPlayer Class Annotations
#Here’s a fully commented version of your DFPlayer class methods, showing exactly what’s happening in _send_cmd and others:
'''
class DFPlayer:
    def __init__(self, uart, volume=20):
        self.uart = uart
        self.volume = volume
        self.set_volume(volume)

    def _send_cmd(self, cmd, param=0):
        """
        Build and send a 10-byte DFPlayer command packet.

        Format: 
        [0x7E][0xFF][0x06][CMD][0x00][PARAM_H][PARAM_L][0x00][0x00][0xEF]

        - 0x7E : Start byte
        - 0xFF : Version
        - 0x06 : Length of following bytes (always 6)
        - cmd  : Command code (e.g., play, stop, volume set, etc.)
        - 0x00 : Feedback flag (0 = no reply, 1 = reply requested)
        - PARAM_H : High byte of parameter
        - PARAM_L : Low byte of parameter
        - 0x00,0x00 : Reserved (ignored in most cases)
        - 0xEF : End byte
        """

        buf = bytearray(10)
        buf[0] = 0x7E       # Start
        buf[1] = 0xFF       # Version
        buf[2] = 0x06       # Length
        buf[3] = cmd        # Command ID
        buf[4] = 0x00       # No feedback
        buf[5] = (param >> 8) & 0xFF   # High byte of parameter
        buf[6] = param & 0xFF          # Low byte of parameter
        buf[7] = 0x00       # Reserved
        buf[8] = 0x00       # Reserved
        buf[9] = 0xEF       # End

        self.uart.write(buf)  # Send to DFPlayer

    def set_volume(self, vol):
        """Set volume (0–30). Clamps to valid range."""
        self.volume = max(0, min(30, vol))
        self._send_cmd(0x06, self.volume)  # 0x06 = Set volume

    def volume_up(self):
        """Increase volume by 1 step (max 30)."""
        self.set_volume(self.volume + 1)

    def volume_down(self):
        """Decrease volume by 1 step (min 0)."""
        self.set_volume(self.volume - 1)

    def play_track(self, num):
        """Play track in root folder by index number."""
        self._send_cmd(0x03, num)  # 0x03 = Play track from root

    def play_folder_track(self, folder, num):
        """
        Play a track inside a specific folder.
        
        - folder: 1–99
        - num   : track number inside that folder (1–255)
        
        DFPlayer expects: PARAM = (folder << 8) | track
        """
        param = (folder << 8) | num
        self._send_cmd(0x0F, param)  # 0x0F = Play folder track
'''
'''
help me understand this command: def play_folder_track(self, folder, num): """ Play a track inside a specific folder. - folder: 1–99 - num : track number inside that folder (1–255) DFPlayer expects: PARAM = (folder << 8) | track """ param = (folder << 8) | num self._send_cmd(0x0F, param) # 0x0F = Play folder track.
step by step.
1. The DFPlayer play_folder_track requirement
The DFPlayer expects the parameter to be a 16-bit number:
PARAM = (folder << 8) | track
That means:
The folder number goes into the high byte (bits 15–8).
The track number goes into the low byte (bits 7–0).
So the final param looks like:
[ FOLDER (8 bits) ] [ TRACK (8 bits) ]
2. Your example: Folder C, Track 3
Folder "C" means the 12th folder (because A=10, B=11, C=12 in decimal).
Decimal: 12
Hexadecimal: 0x0C
Binary: 00001100
Track = 3
Decimal: 3
Hexadecimal: 0x03
Binary: 00000011
3. Shift and OR
The calculation:
param = (folder << 8) | track
Step by step:
folder << 8
0x0C << 8 = 0x0C00
Binary: 00001100 00000000
| track
0x0C00 | 0x03 = 0x0C03
Binary: 00001100 00000011
So:
param = 0x0C03   (decimal 3075)
4. How it’s used in the DFPlayer command
The _send_cmd(0x0F, param) builds the 10-byte frame:
[0] 0x7E   (start)
[1] 0xFF   (version)
[2] 0x06   (length)
[3] 0x0F   (command: play folder track)
[4] 0x00   (no feedback)
[5] 0x0C   (PARAM high byte = folder)
[6] 0x03   (PARAM low byte = track)
[7] 0x00
[8] 0x00
[9] 0xEF   (end)
👉 This is the full packet sent over UART to tell the DFPlayer:
“Play track 3 in folder 12”
✅ So in your wording:
It’s not 10000011.
It’s actually 00001100 00000011 (two bytes, not one).
High byte = folder = 00001100
Low byte = track = 00000011

helper you can run on your Pico (or even on your Mac with plain Python) to “see” how (folder, track) becomes the DFPlayer parameter and packet.
🔧 Helper Function

'''
def explain_folder_track(folder, track):
    """
    Show how DFPlayer builds the PARAM and command packet
    from folder and track numbers.
    """
    param = (folder << 8) | track
    high = (param >> 8) & 0xFF
    low  = param & 0xFF

    print("=== DFPlayer Folder/Track Command ===")
    print(f"Folder: {folder} (dec) = {folder:#04x} (hex) = {folder:08b} (bin)")
    print(f"Track : {track} (dec) = {track:#04x} (hex) = {track:08b} (bin)")
    print()
    print(f"PARAM = (folder << 8) | track = {param} (dec) = {param:#06x} (hex)")
    print(f"PARAM binary = {param:016b}")
    print(f"  High byte (folder) = {high:#04x} ({high:08b})")
    print(f"  Low  byte (track)  = {low:#04x} ({low:08b})")
    print()
    # Build the full 10-byte command
    buf = [
        0x7E, 0xFF, 0x06, 0x0F, 0x00,
        high, low,
        0x00, 0x00, 0xEF
    ]
    print("Full UART packet to DFPlayer:")
    print(" ".join(f"{b:02X}" for b in buf))
    print("====================================")
    print()
# Example: Folder 12 (C), Track 3 to use:
#explain_folder_track(12, 3)

# Example: Folder 1, Track 1
#explain_folder_track(1, 1)
# for (12,3):
'''
=== DFPlayer Folder/Track Command ===
Folder: 12 (dec) = 0x0c (hex) = 00001100 (bin)
Track : 3 (dec)  = 0x03 (hex) = 00000011 (bin)

PARAM = (folder << 8) | track = 3075 (dec) = 0x0c03 (hex)
PARAM binary = 0000110000000011
  High byte (folder) = 0x0c (00001100)
  Low  byte (track)  = 0x03 (00000011)

Full UART packet to DFPlayer:
7E FF 06 0F 00 0C 03 00 00 EF
====================================
'''


''' 16 Sept 2025 version where I explored the correlation of datasheet (in ComputerSetup in 'Documents)' and  checksum 
'''
from machine import Pin, I2C, UART
import utime
from ssd1306 import SSD1306_I2C

# -----------------------------
# DFPlayer Mini driver
# -----------------------------
class DFPlayerMini:
    START_BYTE = 0x7E
    VERSION = 0xFF
    LENGTH = 0x06
    END_BYTE = 0xEF

    def __init__(self, uart):
        self.uart = uart

    def _checksum(self, cmd, feedback, param):
        """Calculate DFPlayer checksum (two's complement)."""
        param_high = (param >> 8) & 0xFF
        param_low = param & 0xFF
        total = (self.VERSION + self.LENGTH + cmd + feedback + param_high + param_low)
        checksum = 0xFFFF - total + 1
        return (checksum >> 8) & 0xFF, checksum & 0xFF

    def _send(self, cmd, param=0, feedback=0):
        """Build and send DFPlayer command packet."""
        param_high = (param >> 8) & 0xFF
        param_low = param & 0xFF
        cks_high, cks_low = self._checksum(cmd, feedback, param)
        packet = bytearray([
            self.START_BYTE,
            self.VERSION,
            self.LENGTH,
            cmd,
            feedback,
            param_high,
            param_low,
            cks_high,
            cks_low,
            self.END_BYTE
        ])
        self.uart.write(packet)

    def play_folder_file(self, folder, file):
        """Play specific folder/file."""
        param = (folder << 8) | file
        self._send(0x0F, param)

    def volume(self, level):
        """Set volume (0–30)."""
        self._send(0x06, level)


# -----------------------------
# Keypad handler
# -----------------------------
class Keypad:
    KEYS = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
    ]

    def __init__(self, row_pins, col_pins):
        self.rows = [Pin(p, Pin.OUT) for p in row_pins]
        self.cols = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in col_pins]
        self.last_key = None
        self.last_time = 0
        self.debounce_ms = 200

    def scan(self):
        """Scan keypad and return pressed key, or None."""
        for i, row in enumerate(self.rows):
            row.value(1)
            for j, col in enumerate(self.cols):
                if col.value() == 1:
                    key = self.KEYS[i][j]
                    now = utime.ticks_ms()
                    if (self.last_key != key or
                        utime.ticks_diff(now, self.last_time) > self.debounce_ms):
                        self.last_key = key
                        self.last_time = now
                        row.value(0)
                        return key
            row.value(0)
        return None


# -----------------------------
# Player controller with OLED
# -----------------------------
class PlayerController:
    def __init__(self):
        # OLED setup
        i2c = I2C(0, scl=Pin(17), sda=Pin(16))
        self.oled = SSD1306_I2C(128, 64, i2c)

        # DFPlayer Mini setup
        uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
        self.dfplayer = DFPlayerMini(uart)
        self.dfplayer.volume(20)

        # Keypad setup
        self.keypad = Keypad(
            row_pins=[6, 7, 8, 9],     # adjust to your wiring
            col_pins=[10, 11, 12, 13]  # adjust to your wiring
        )

        # State
        self.folder = 1
        self.file = 1
        self.buffer = ""

    def display(self, msg1, msg2=""):
        self.oled.fill(0)
        self.oled.text("DFPlayer", 0, 0)
        self.oled.text(msg1, 0, 20)
        if msg2:
            self.oled.text(msg2, 0, 40)
        self.oled.show()

    def process_key(self, key):
        if key.isdigit():
            self.buffer += key
            self.display("Input: " + self.buffer)
            if len(self.buffer) == 2:
                self.file = int(self.buffer)
                self.buffer = ""
                self.dfplayer.play_folder_file(self.folder, self.file)
                self.display("Play", f"Folder {self.folder} File {self.file}")

        elif key == "A":  # Increase folder
            self.folder = min(self.folder + 1, 99)
            self.display("Folder ->", str(self.folder))

        elif key == "B":  # Decrease folder
            self.folder = max(self.folder - 1, 1)
            self.display("Folder <-", str(self.folder))

        elif key == "C":  # Volume up
            self.dfplayer.volume(25)
            self.display("Volume", "Up")

        elif key == "D":  # Volume down
            self.dfplayer.volume(10)
            self.display("Volume", "Down")

        elif key == "*":  # Clear buffer
            self.buffer = ""
            self.display("Input cleared")

        elif key == "#":  # Replay current file
            self.dfplayer.play_folder_file(self.folder, self.file)
            self.display("Replay", f"Folder {self.folder} File {self.file}")

    def run(self):
        self.display("Ready")
        while True:
            key = self.keypad.scan()
            if key:
                self.process_key(key)
            utime.sleep_ms(50)


# -----------------------------
# Main
# -----------------------------
def main():
    controller = PlayerController()
    controller.run()


if __name__ == "__main__":
    main()



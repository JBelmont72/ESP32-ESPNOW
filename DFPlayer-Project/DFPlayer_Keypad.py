'''


'''
from machine import Pin, UART
import time,sys

# ===================== DFPlayer Mini =====================
class DFPlayer:
    def __init__(self, uart_id=2, tx=17, rx=16, baud=9600, busy_pin=5):
        self.uart = UART(uart_id, baudrate=baud, tx=tx, rx=rx)
        self.busy_pin = busy_pin
        self.BUSY_PIN = Pin(self.busy_pin, Pin.IN)
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

        # Proper checksum
        checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
        buf[7] = (checksum >> 8) & 0xFF
        buf[8] = checksum & 0xFF
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

    def show_busy_state(self):
        """Display DFPlayer BUSY pin logic."""
        state = self.BUSY_PIN.value()
        if state == 0:
            print("🎶 DFPlayer is PLAYING (BUSY LOW)")
        else:
            print("⏹ DFPlayer is IDLE (BUSY HIGH)")

'''
class DFPlayer:
    def __init__(self, uart_id=2, tx=17, rx=16, baud=9600,busy_pin=5):
        self.uart = UART(uart_id, baudrate=baud, tx=tx, rx=rx)
        self.volume = 20
        self.set_volume(self.volume)
        self.busy_pin=busy_pin
        BUSY_PIN=Pin(self.busy_pin,Pin.IN)
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
    def show_busy_state():
        """Display DFPlayer BUSY pin logic."""
        state = BUSY_PIN.value()
        if state == 0:
            print("🎶 DFPlayer is PLAYING (BUSY LOW)")
        else:
            print("⏹ DFPlayer is IDLE (BUSY HIGH)")
'''
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

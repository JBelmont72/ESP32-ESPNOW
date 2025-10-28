'''


'''
from machine import Pin, UART
import time, sys

# ===================== DFPlayer Class =====================
class DFPlayer:
    """Control DFPlayer Mini via UART."""

    def __init__(self, uart_id=2, tx=17, rx=16, baud=9600, busy_pin=5):
        self.uart = UART(uart_id, baudrate=baud, tx=tx, rx=rx)
        self.busy_pin = busy_pin
        self.BUSY_PIN = Pin(self.busy_pin, Pin.IN)
        self.volume = 20
        self.set_volume(self.volume)
        self.clear_uart_buffer()
        print("🎧 DFPlayer initialized.")

    # ------------------------------------------------------
    def _send_cmd(self, cmd, param=0):
        """Send formatted 10-byte command frame to DFPlayer."""
        buf = bytearray(10)
        buf[0] = 0x7E
        buf[1] = 0xFF
        buf[2] = 0x06
        buf[3] = cmd
        buf[4] = 0x00
        buf[5] = (param >> 8) & 0xFF
        buf[6] = param & 0xFF

        checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
        buf[7] = (checksum >> 8) & 0xFF
        buf[8] = checksum & 0xFF
        buf[9] = 0xEF

        self.uart.write(buf)

    # ------------------------------------------------------
    def clear_uart_buffer(self):
        """Flush any data in UART receive buffer."""
        while self.uart.any():
            self.uart.read()

    def set_volume(self, vol):
        self.volume = max(0, min(30, vol))
        self._send_cmd(0x06, self.volume)

    def volume_up(self):
        self.set_volume(self.volume + 1)
        print(f"🔊 Volume: {self.volume}")

    def volume_down(self):
        self.set_volume(self.volume - 1)
        print(f"🔉 Volume: {self.volume}")

    def play_track(self, num):
        """Play track in root folder by number (1–2999)."""
        print(f"▶️ Playing track {num:04d}.mp3")
        self._send_cmd(0x03, num)

    def play_folder_track(self, folder, num):
        """Play track num (1–255) from folder (1–99)."""
        param = (folder << 8) | num
        print(f"▶️ Playing folder {folder}, track {num}")
        self._send_cmd(0x0F, param)

    def wait_while_playing(self, timeout=60000):
        """Pause until DFPlayer finishes (BUSY LOW = playing)."""
        start = time.ticks_ms()
        while self.BUSY_PIN.value() == 0:
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                print("⚠️ Timeout waiting for playback to finish.")
                break
            time.sleep_ms(100)
        print("✅ Playback complete (BUSY HIGH).")

    def stop(self):
        """Stop playback."""
        self._send_cmd(0x16)
        print("⏹ Stopped playback.")

# ===================== Keypad Class =====================
class Keypad:
    """4x4 Matrix Keypad Reader."""
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

# ===================== Controller Class =====================
class PlayerController:
    """Main controller that connects keypad and DFPlayer."""

    def __init__(self):
        self.df = DFPlayer(uart_id=2, tx=17, rx=16, busy_pin=5)

        row_pins = (14, 27, 26, 25)
        col_pins = (33, 32, 35, 34)
        keys = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]
        self.kp = Keypad(row_pins, col_pins, keys)
        self.track_buffer = ""
        self.folder_mode = None
        self.playing = False

    def handle_key(self, key):
        if self.playing:
            # Ignore keypresses while a track is playing
            return

        print("Key pressed:", key)

        if key == "*":
            self.df.volume_down()

        elif key == "#":
            self.df.volume_up()

        elif key in "ABCD":
            self.folder_mode = {"A":1, "B":2, "C":3, "D":4}[key]
            self.track_buffer = ""
            print(f"📁 Folder mode {self.folder_mode}, enter 2-digit track.")

        elif key.isdigit():
            self.track_buffer += key
            if len(self.track_buffer) == 2:
                track_num = int(self.track_buffer)
                self.playing = True
                if self.folder_mode:
                    self.df.play_folder_track(self.folder_mode, track_num)
                    self.folder_mode = None
                else:
                    self.df.play_track(track_num)
                self.df.wait_while_playing()
                self.playing = False
                self.track_buffer = ""

        else:
            self.track_buffer = ""
            self.folder_mode = None

    def run(self):
        print("🎵 Ready. Use keypad to control DFPlayer.")
        try:
            while True:
                key = self.kp.scan()
                if key:
                    self.handle_key(key)
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user.")
        except Exception as e:
            print("❌ Error:", e)
        finally:
            print("🧹 Cleaning up UART and stopping playback...")
            self.df.stop()
            self.df.clear_uart_buffer()
            time.sleep(0.2)
            print("✅ Clean exit.")
            sys.exit()

# ===================== Main Entry Point =====================
if __name__ == "__main__":
    controller = PlayerController()
    controller.run()

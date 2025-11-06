'''
very simple UART test directly against the DFPlayer.
The DFPlayer has no “text output” like the loopback — the way to confirm it works is:
Send it a command over UART.
It responds by playing audio (if an SD card with MP3 files is inserted).
1️⃣ Wiring check (important!)
ESP32 TX (e.g. GPIO17) → DFPlayer RX
ESP32 RX (e.g. GPIO16) → DFPlayer TX (optional, for feedback)
ESP32 GND → DFPlayer GND
ESP32 5V → DFPlayer VCC (DFPlayer needs 5V for audio output!)
Speaker → DFPlayer SPK+ and SPK− (or to your PAM8304 amp input).
Also make sure the SD card is formatted FAT32, with files like 0001.mp3, 0002.mp3, etc. in the root or in properly named folders (01/001.mp3, 01/002.mp3 etc).
'''
# from machine import UART, Pin
# import time

# # Use UART2 on ESP32 Plays the first track
# uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # Adjust pins if needed

# def send_cmd(cmd, param=0):
#     """
#     Send 10-byte command to DFPlayer with checksum.
#     """
#     buf = bytearray(10)
#     buf[0] = 0x7E               # Start byte
#     buf[1] = 0xFF               # Version
#     buf[2] = 0x06               # Length
#     buf[3] = cmd                # Command
#     buf[4] = 0x00               # No feedback
#     buf[5] = (param >> 8) & 0xFF
#     buf[6] = param & 0xFF
#     checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
#     buf[7] = (checksum >> 8) & 0xFF
#     buf[8] = checksum & 0xFF
#     buf[9] = 0xEF               # End byte
#     uart.write(buf)

# print("DFPlayer test: setting volume and playing track 1")

# time.sleep(2)  # small delay after reset

# send_cmd(0x06, 20)   # set volume to 20 (range 0–30)
# time.sleep(0.5)
# send_cmd(0x03, 1)    # play track #1 in root folder

'''
3️⃣ Expected behavior
After reset, DFPlayer initializes (SD card must be ready).
This script sets volume to level 20.
Plays track 0001.mp3 in root.
If you have a speaker (or amplifier) wired, you should hear the sound.
4️⃣ If nothing plays
Double-check wiring (especially TX from ESP32 → RX on DFPlayer).
Ensure 5V supply, not 3.3V.
Ensure the SD card is FAT32 with correctly named files.
Try a smaller SD card (≤ 16 GB works best).
👉 Do you want me to extend this test so you can press a key on the VSCode REPL (like 1, 2, +, -) to play track numbers and change volume — before we connect it back to your keypad class?
'''
# from machine import UART, Pin
# import time
# import sys
# ## interactive with the REPL , another step toward the keypad
# # UART2 on ESP32 (adjust pins if needed)
# uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))

# # --- DFPlayer command sender ---
# def send_cmd(cmd, param=0):
#     buf = bytearray(10)
#     buf[0] = 0x7E
#     buf[1] = 0xFF
#     buf[2] = 0x06
#     buf[3] = cmd
#     buf[4] = 0x00
#     buf[5] = (param >> 8) & 0xFF
#     buf[6] = param & 0xFF
#     checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
#     buf[7] = (checksum >> 8) & 0xFF
#     buf[8] = checksum & 0xFF
#     buf[9] = 0xEF
#     uart.write(buf)

# # --- DFPlayer commands ---
# def set_volume(vol):
#     global volume
#     volume = max(0, min(30, vol))
#     send_cmd(0x06, volume)
#     print(f"🔊 Volume set to {volume}")

# def volume_up():
#     set_volume(volume + 1)

# def volume_down():
#     set_volume(volume - 1)

# def play_track(num):
#     send_cmd(0x03, num)
#     print(f"▶️ Playing track {num}")

# # --- startup ---
# volume = 20
# set_volume(volume)
# time.sleep(1)
# play_track(1)

# print("\n✅ DFPlayer interactive test ready.")
# print("Commands:")
# print(" 1–9 → play track number")
# print(" +   → volume up")
# print(" -   → volume down")
# print(" q   → quit\n")

# # --- main loop ---
# while True:
#     try:
#         if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
#             cmd = sys.stdin.read(1).strip()
#             if cmd.isdigit():
#                 play_track(int(cmd))
#             elif cmd == "+":
#                 volume_up()
#             elif cmd == "-":
#                 volume_down()
#             elif cmd.lower() == "q":
#                 print("Exiting.")
#                 break
#     except KeyboardInterrupt:
#         print("Stopped by Ctrl+C")
#         break





'''
Good — thanks. You’ve covered the most common big problems (5 V supply, Sandisk card). Let’s walk through a focused checklist and a few concrete tests you can run right now to pin down why you get **buzzing** instead of audio.

I’ll give you (A) quick hardware/audio wiring checks, (B) SD-card / file checks and Mac terminal commands to clean & reformat, (C) a UART “feedback” test to see whether DFPlayer answers, and (D) quick things to try in order. Do them in order — each step rules out a class of problems.

---

# A. Audio wiring — important to verify (PAM0834 vs DFPlayer SPK pins)

1. If you’re using the **PAM0834 amplifier** (common Class-D amp), **do not** drive PAM input from DFPlayer **SPK+ / SPK-**.

   * `SPK+ / SPK-` on the DFPlayer are speaker outputs (for driving a passive speaker directly).
   * The PAM0834 expects a **line-level input** on its input pins (L in / R in).
2. Correct wiring when using PAM0834:

   * DFPlayer `DAC_L` → PAM `IN_L`
   * DFPlayer `DAC_R` → PAM `IN_R`
   * DFPlayer `GND` → PAM `GND` (common ground with ESP32)
   * PAM `VCC` → 5V (amp) and speaker to PAM outputs (not DFPlayer SPK pins)
3. If you tried SPK+/- into PAM input, you’ll get buzzing or no proper audio. If you want to drive speaker directly from DFPlayer, connect speaker to DFPlayer `SPK+` / `SPK-` (no external amp).
4. Confirm amplifier power & speaker: PAM0834 needs stable 5V and speaker impedance match (e.g., 4Ω or 8Ω).

**Action:** Rewire so DFPlayer DAC outputs feed the PAM inputs, or temporarily connect a speaker directly to DFPlayer SPK pins to test.

---

# B. SD card & file naming (very common cause)

Even if the card is physically readable, DFPlayer can be picky about size, partition type, hidden macOS files, and filename format.

1. **Recommend:** try a small card (2–16 GB) if you have one — Sandisk 32 GB sometimes works, sometimes not. If you only have 32GB, reformat as below.
2. **File names** must be strict:

   * Root files: `0001.mp3`, `0002.mp3`, … (four digits)
   * Folder names: `01`, `02`, … (two digits). Inside a folder: `001.mp3`, `002.mp3`, …
3. **Remove macOS hidden files** (very important). On macOS Terminal run (replace `YOUR_SD` with the mount name):

```bash
# Show all files (see if dot-underscore files present)
ls -la /Volumes/YOUR_SD

# Remove Apple metadata ._ files (safe)
dot_clean /Volumes/YOUR_SD
```

4. **Reformat as FAT32 (MBR)** — terminal steps (careful: this erases the card):

```bash
# list disks to find your SD card (be sure of disk ID)
diskutil list

# assume disk identifier is /dev/disk2 (double-check!)
# Unmount and erase as FAT32 (MS-DOS) with MBR partition map:
diskutil eraseDisk FAT32 SDCARD MBRFormat /dev/disk2
```

5. After formatting, copy only real mp3 files named `0001.mp3` etc (no extra metadata files). Use `dot_clean` afterwards to be safe.

**Action:** Reformat the card to FAT32 MBR and copy only properly named mp3 files. If possible test with a 4–8–16GB card first.

---

# C. UART feedback test — ask DFPlayer for a reply (diagnose SD/card status)

We’ll set the DFPlayer command to request feedback, then read back any response on UART. If DFPlayer responds, we’ll get a small reply frame — that confirms DFPlayer got the command and is functioning.

Use this test on your ESP32 (adjust pins if needed). It will:

* Send a **request with feedback enabled**.
* Wait to read any bytes returned on the UART.

```python
from machine import UART, Pin
import time

uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))  # adjust pins

def send_cmd(cmd, param=0, feedback=1):
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = feedback & 1
    buf[5] = (param >> 8) & 0xFF
    buf[6] = param & 0xFF
    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF
    uart.write(buf)

def read_response(timeout_ms=1000):
    t0 = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if uart.any():
            resp += uart.read()
        time.sleep_ms(10)
    return resp

# Example sequence: request status (play track 1 but with feedback)
send_cmd(0x06, 20, feedback=1)   # set volume, ask for feedback
time.sleep(0.1)
send_cmd(0x03, 1, feedback=1)    # play track 1, ask for feedback

time.sleep(0.5)
resp = read_response(1500)
print("Raw response:", resp)
# If resp non-empty (10-byte-ish frames), DFPlayer replies; print hex:
print("Hex:", " ".join("{:02X}".format(b) for b in resp))
```

* If you get a non-empty response frame (10 bytes) -> DFPlayer acknowledged. That’s good and means the SD/file naming or audio wiring is likely the cause of buzzing.
* If **no response**, then either the DFPlayer isn’t powered correctly, UART pins/wiring wrong, or DFPlayer is not booted (SD card read/format problem).

**Action:** Run the above. Report back the `Raw response` or `Hex` output.

---

# D. Quick test flow & likely fixes (order matters)

1. **Check wiring to PAM**: If using PAM, wire `DAC_L`/`DAC_R` → PAM INs (not SPK pins). Test audio again.
2. If still buzzing:

   * Try speaker directly on DFPlayer SPK+/- (disconnect PAM) — if you then hear audio, the issue was PAM wiring.
3. If still buzzing:

   * Reformat SD card FAT32/MBR, copy only `0001.mp3` (try just a single small MP3 first).
   * Run `dot_clean` to remove macOS ._ files.
   * Optionally try another small SD card (8GB or 16GB).
4. Use the **UART feedback test** above. If DFPlayer responds, check SD & file naming. If DFPlayer does not respond, double-check VCC=5V and ground common; confirm DFPlayer busy pin or LED shows activity.
5. If DFPlayer acknowledges commands (feedback present) but no sound with PAM connected, likely wiring of DAC→PAM or PAM power/enable issues.

---

# Extra tips

* Some DFPlayer modules have BOTH `DAC_L/DAC_R` and `SPK+/SPK-` pins. Be sure to use the correct pins for your configuration.
* Try a *single* file named `0001.mp3` at modest bitrate (128 kbps) to reduce codec/bitrate issues.
* If you can, try a simple known-good MP3 from the internet converted to 128kbps with no weird metadata tags.
* If you want, paste the **hex output** of the `read_response()` result here and I’ll decode it for you.

---

If you want I can:

* (A) give you a compact script that alternately plays `0001.mp3` and then stops with feedback and logs the DFPlayer reply; or
* (B) help you reformat the SD card step-by-step with exact `diskutil` commands if you tell me the disk ID from `diskutil list`.

Which would you like to try next?

'''

from machine import UART, Pin
import time

uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(13))  # adjust pins

def send_cmd(cmd, param=0, feedback=1):
    buf = bytearray(10)
    buf[0] = 0x7E
    buf[1] = 0xFF
    buf[2] = 0x06
    buf[3] = cmd
    buf[4] = feedback & 1
    buf[5] = (param >> 8) & 0xFF
    buf[6] = param & 0xFF
    checksum = 0xFFFF - (buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6]) + 1
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF
    uart.write(buf)

def read_response(timeout_ms=1000):
    t0 = time.ticks_ms()
    resp = b""
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if uart.any():
            print('uart armed')
            
            resp += uart.read()
        time.sleep_ms(10)
    return resp
# --- main loop ---
while True:
    try:
        
        send_cmd(0x06, 25)   # volume = 25
        time.sleep(0.2)
        send_cmd(0x03, 1)    # play track 1
        # send_cmd(0x06, 20, feedback=1)   # set volume, ask for feedback
        # time.sleep(0.1)
        # send_cmd(0x03, 1, feedback=1)    # play track 1, ask for feedback

        # time.sleep(0.5)
        # resp = read_response(1500)
        # print("Raw response:", resp)

    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")

        break


# send_cmd(0x06, 25)   # volume = 25
# time.sleep(0.2)
# send_cmd(0x03, 1)    # play track 1

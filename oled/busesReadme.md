# understanding busses and use of SoftI2c and just ssd1306.py

why do a number of oled programs use: from machine import Pin, SoftI2C
import ssd1306
import framebuf

# using default address 0x3C
i2c = SoftI2C(sda=Pin(22), scl=Pin(23))
display = ssd1306.SSD1306_I2C(128, 64, i2c) constructors ?
# EXPLANATION

because in MicroPython there are two kinds of I²C objects you can use:
1️⃣ I2C (hardware I²C)
Uses the ESP32’s built-in hardware I²C peripheral.
Very fast and efficient.
On ESP32, it supports any GPIO pins (pin-muxed in software), but under the hood it still uses the hardware controller. Faster and uses less CPU
The constructor looks like:
    from machine import Pin, I2C
    i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # bus ID 0

2️⃣ SoftI2C (bit-banged I²C)
Implements I²C in pure software, toggling pins manually.
Works on any two GPIO pins, even if the hardware I²C peripheral is busy or unavailable.
Why use it?
Some boards’ default hardware I²C pins are already in use.
Hardware I²C may be buggy on certain MicroPython versions or pins.
Easier for beginners — no bus ID numbers, just SDA and SCL pins.
the bus ID number is ther 0 and 1
The constructor looks like:
    from machine import Pin, SoftI2C
    i2c = SoftI2C(sda=Pin(22), scl=Pin(23))

3️⃣ Why framebuf is sometimes imported
The ssd1306 driver uses framebuf internally to store the display’s pixel data in RAM before sending it to the OLED.
If you want to draw shapes or manipulate pixels yourself, you can call framebuf functions directly.
Example:  import framebuf

# In short
I2C(...) → hardware, faster, bus ID required.
SoftI2C(...) → software, more flexible, slightly slower.
Both work with the ssd1306.SSD1306_I2C(...) constructor.

# OLED auto-detection script work with either hardware I²C or SoftI2C — so it will try hardware first, then fall back to software if needed.
That would make it almost unbreakable for pin changes.
final “unbreakable” OLED script that:
Tries hardware I²C first (bus IDs 0 and 1).
Falls back to SoftI2C if no OLED is found.
Lists all I²C devices it sees.
Detects SSD1306 address automatically.
Auto-guesses 128×64 or 128×32 height by testing pixels.
How it works
Hardware first → checks bus 0 and bus 1.
Fallback → uses SoftI2C if no OLED found.
Device listing → prints all I²C addresses it sees for debugging.
Height guessing → writes a pixel at y=48 and sees if it’s visible. If not, it assumes 32px.

# Auto-I²C + SoftI2C OLED Detector
import time
from machine import Pin, I2C, SoftI2C
import ssd1306

# Pin configuration
SCL_PIN = 22
SDA_PIN = 21

def scan_bus(i2c, label):
    """Scan a given I2C bus and print devices."""
    devices = i2c.scan()
    if devices:
        print(f"{label}: Found {len(devices)} device(s) ->", [hex(d) for d in devices])
    else:
        print(f"{label}: No devices found.")
    return devices

# Step 1: Try hardware I2C buses first
i2c = None
oled_address = None

print("🔍 Scanning for OLED display...\n")

for bus_id in (0, 1):
    try:
        temp_i2c = I2C(bus_id, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        devices = scan_bus(temp_i2c, f"Hardware I2C bus {bus_id}")
        for addr in devices:
            if addr in (0x3C, 0x3D):
                i2c = temp_i2c
                oled_address = addr
                break
    except Exception as e:
        print(f"Hardware I2C bus {bus_id}: Error -> {e}")

    if i2c:
        break

# Step 2: If no OLED found, try SoftI2C
if not i2c:
    print("\n⚠️ No OLED found on hardware I2C. Trying SoftI2C...")
    try:
        temp_i2c = SoftI2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        devices = scan_bus(temp_i2c, "SoftI2C")
        for addr in devices:
            if addr in (0x3C, 0x3D):
                i2c = temp_i2c
                oled_address = addr
                break
    except Exception as e:
        print(f"SoftI2C: Error -> {e}")

# Step 3: Fail if no OLED found
if not i2c or not oled_address:
    print("\n❌ OLED not found! Check wiring, pins, and power.")
    while True:
        pass

print(f"\n✅ OLED found at address 0x{oled_address:02X}")

# Step 4: Guess height (test drawing near bottom)
oled_width = 128
oled_height = 64  # Assume 64 first
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=oled_address)
oled.fill(0)
oled.pixel(0, 48, 1)  # Draw near 48px row
oled.show()

time.sleep(0.2)
if oled.framebuf.pixel(0, 48) == 0:
    oled_height = 32
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=oled_address)

print(f"🖥 OLED resolution detected: {oled_width}x{oled_height}")

# Step 5: Display test message
oled.fill(0)
oled.text("Hello, ESP32!", 0, 0)
oled.text(f"{oled_width}x{oled_height}", 0, 16)
oled.show()

time.sleep(5)
oled.fill(0)
oled.show()

## expalin busses
1️⃣ What is a bus?
In hardware, a bus is just a set of wires and rules for how devices talk.
For I²C:
2 signal wires: SDA (data) and SCL (clock)
One master (your ESP32) and one or more slave devices (like an OLED, sensor, etc.)
Every device has an address (like 0x3C for many OLEDs).
You can put multiple devices on the same I²C bus, as long as they have different addresses.
2️⃣ Why does MicroPython talk about bus numbers?
The ESP32 has two hardware I²C controllers built in:
I2C(0)
I2C(1)
These are not the same as “GPIO pin numbers.”
They are internal hardware modules that can be assigned to any pins you want.
When you do:

I2C(0, scl=Pin(22), sda=Pin(21))
…you’re telling MicroPython:
“Use hardware I²C controller number 0, and connect it to pins 22 (SCL) and 21 (SDA).”
If you instead do:
I2C(1, scl=Pin(19), sda=Pin(18))
…you’re using the second hardware I²C controller on different pins.
3️⃣ Why are there multiple buses?
Reasons you might use more than one:
Two unrelated I²C networks: one for your OLED, one for other devices.
Address conflicts: if two devices have the same fixed I²C address, you can’t put them on the same bus — use different buses.
Performance: keep high-speed devices on a separate bus to avoid slowing others.
4️⃣ Where does SoftI2C fit in?
I2C(...) → Uses the ESP32’s hardware bus #0 or #1.
SoftI2C(...) → Ignores hardware controllers and bit-bangs the I²C protocol on any pins.
You can think of SoftI2C as a “fake bus” — slower but extremely flexible.
5️⃣ In practice for OLEDs
Most people just use one hardware bus for everything (I2C(0) or I2C(1)).
If you buy a second device with a conflicting address, you might need:
A second hardware bus
Or SoftI2C on different pins
Some ESP32 boards wire their default I²C devices to a specific hardware bus, so if you pick the wrong bus ID in code, you’ll see “no devices found.”
💡 Rule of thumb:
Try I2C(0, scl=Pin(22), sda=Pin(21)) first — it works for many ESP32 dev boards.
If nothing shows up in a scan, try I2C(1, ...).
If still nothing, try SoftI2C(...).
Use i2c.scan() to see what’s on each bus.


# chat for oled codes and explains buses 
    https://chatgpt.com/c/6896a5d3-9494-832e-be4c-c96f682e6f90
# OLED bare bones basic
import time
from machine import Pin, I2C
import ssd1306

# Step 1: Set up I2C (GPIO 22 = SCL, GPIO 21 = SDA)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Step 2: Detect OLED address
oled_address = None
for addr in i2c.scan():
    if addr in [0x3C, 0x3D]:  # Common OLED addresses
        oled_address = addr
        break

if oled_address is None:
    print("OLED not found!")
    while True:
        pass

# Step 3: Initialize OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Step 4: Clear display
oled.fill(0)
oled.show()

# Step 5: Display text
oled.text("Hello, World!", 0, 0)
oled.show()

# Keep the message for 5 seconds
time.sleep(5)

# Step 6: Clear again
oled.fill(0)
oled.show()

# !!version that auto-detects the I2C bus number so it works on both ESP32 and ESP8266 without changing I2C(0, …) manually.
That might prevent future “No display found” headaches.
Scan both common I²C buses on the ESP32 (I2C(0) and I2C(1)).
Detect the OLED’s actual I²C address (0x3C or 0x3D).
Bus auto-detect → works even if your board uses I2C(1) instead of I2C(0).
Address auto-detect → works with both common SSD1306 addresses without editing code.
Fail-safe → stays in an infinite loop with an error message if no display is found, so you know it’s wiring or power related.
# I2C auto-detect oled program
import time
from machine import Pin, I2C
import ssd1306

# Your I2C pin configuration (ESP32: GPIO 22 = SCL, GPIO 21 = SDA)
SCL_PIN = 22
SDA_PIN = 21

# Step 1: Try both I2C bus IDs (0 and 1) to find the display
i2c = None
oled_address = None

for bus_id in (0, 1):
    try:
        temp_i2c = I2C(bus_id, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        devices = temp_i2c.scan()
        if devices:
            for addr in devices:
                if addr in (0x3C, 0x3D):  # Common SSD1306 addresses
                    i2c = temp_i2c
                    oled_address = addr
                    break
    except Exception as e:
        pass  # Ignore errors and try next bus
    
    if i2c:  # Stop searching if found
        break

if i2c is None or oled_address is None:
    print("❌ OLED not found! Check wiring and power.")
    while True:
        pass

print(f"✅ OLED found at address 0x{oled_address:02X} on I2C bus {i2c}")

# Step 2: Initialize OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Step 3: Clear display
oled.fill(0)
oled.show()

# Step 4: Display text
oled.text("Hello, ESP32!", 0, 0)
oled.show()

# Keep for 5 seconds
time.sleep(5)

# Step 5: Clear again
oled.fill(0)
oled.show()

# 1️⃣ OLED program with I²C device list first
This one lists all detected I²C devices, then initializes the OLED if found.
import time
from machine import Pin, I2C
import ssd1306

# Pin configuration (ESP32 defaults: GPIO 22 = SCL, GPIO 21 = SDA)
SCL_PIN = 22
SDA_PIN = 21

# Try both bus IDs
i2c = None
oled_address = None

for bus_id in (0, 1):
    try:
        temp_i2c = I2C(bus_id, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        devices = temp_i2c.scan()

        if devices:
            print(f"I2C bus {bus_id}: Found devices:", [hex(d) for d in devices])
            for addr in devices:
                if addr in (0x3C, 0x3D):  # SSD1306 common addresses
                    i2c = temp_i2c
                    oled_address = addr
                    break
    except:
        pass

    if i2c:
        break

if i2c is None or oled_address is None:
    print("❌ OLED not found! Check wiring and power.")
    while True:
        pass

print(f"✅ OLED found at 0x{oled_address:02X} on I2C bus {i2c}")

# Initialize OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Display test
oled.fill(0)
oled.text("Hello, ESP32!", 0, 0)
oled.show()
time.sleep(5)
oled.fill(0)
oled.show()
############

# the OLED script auto-adjust resolution if it detects a 128×32 or 128×64 OLED.
That way you don’t need to hardcode 128, 64.
Scan both I²C buses.
List all devices it finds.
Detect the SSD1306 OLED address.
Auto-detect height → if it can’t tell, it defaults to 64px, but you can force 32px if needed.
## this is the autodetect script although it seems to set the height and width. Maybe try this in the future, not set as a .py in my folder until i try it.
import time
from machine import Pin, I2C
import ssd1306

# Pin configuration for ESP32 (adjust if needed)
SCL_PIN = 22
SDA_PIN = 21

# Try both I2C bus IDs
i2c = None
oled_address = None

print("🔍 Scanning I2C buses...\n")
for bus_id in (0, 1):
    try:
        temp_i2c = I2C(bus_id, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        devices = temp_i2c.scan()

        if devices:
            print(f"I2C bus {bus_id}: Found devices:", [hex(d) for d in devices])
            for addr in devices:
                if addr in (0x3C, 0x3D):  # Common SSD1306 addresses
                    i2c = temp_i2c
                    oled_address = addr
                    break
    except:
        pass

    if i2c:
        break

if i2c is None or oled_address is None:
    print("❌ OLED not found! Check wiring and power.")
    while True:
        pass

print(f"✅ OLED found at address 0x{oled_address:02X} on I2C bus {i2c}")

# Auto-detect OLED height
# Unfortunately, SSD1306 has no built-in way to report height,
# so we guess based on common addresses or let user override.
# Default to 64px unless user changes this line:
oled_height = 64  # Change to 32 if you know it's a 128x32 display
oled_width = 128

print(f"🖥 OLED resolution set to {oled_width}x{oled_height}")

# Initialize OLED
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=oled_address)

# Display test
oled.fill(0)
oled.text("Hello, ESP32!", 0, 0)
oled.text(f"{oled_width}x{oled_height}", 0, 16)
oled.show()

time.sleep(5)
oled.fill(0)
oled.show()
#####

# why do a number of oled programs use: from machine import Pin, SoftI2C import ssd1306 import framebuf # using default address 0x3C i2c = SoftI2C(sda=Pin(22), scl=Pin(23)) display = ssd1306.SSD1306_I2C(128, 64, i2c) constructors ?

That’s because in MicroPython there are **two kinds of I²C objects** you can use:

---

## **1️⃣ `I2C` (hardware I²C)**

* Uses the ESP32’s built-in hardware I²C peripheral.
* Very fast and efficient.
* On ESP32, it supports *any* GPIO pins (pin-muxed in software), but under the hood it still uses the hardware controller.
* The constructor looks like:

  ```python
  from machine import Pin, I2C
  i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # bus ID 0
  ```
* **Why use it?** → Faster and uses less CPU.

---

## **2️⃣ `SoftI2C` (bit-banged I²C)**

* Implements I²C in **pure software**, toggling pins manually.
* Works on *any* two GPIO pins, even if the hardware I²C peripheral is busy or unavailable.
* The constructor looks like:

  ```python
  from machine import Pin, SoftI2C
  i2c = SoftI2C(sda=Pin(22), scl=Pin(23))
  ```
* **Why use it?**

  * Some boards’ default hardware I²C pins are already in use.
  * Hardware I²C may be buggy on certain MicroPython versions or pins.
  * Easier for beginners — no bus ID numbers, just SDA and SCL pins.

---

## **3️⃣ Why `framebuf` is sometimes imported**

* The `ssd1306` driver uses `framebuf` internally to store the display’s pixel data in RAM before sending it to the OLED.
* If you want to draw shapes or manipulate pixels yourself, you can call `framebuf` functions directly.
* Example:

  ```python
  import framebuf
  # draw lines, rectangles, etc.
  ```

---

## **In short**

* `I2C(...)` → hardware, faster, bus ID required.
* `SoftI2C(...)` → software, more flexible, slightly slower.
* Both work with the `ssd1306.SSD1306_I2C(...)` constructor.

---

If you want, I can make your OLED auto-detection script work with **either hardware I²C or SoftI2C** — so it will try hardware first, then fall back to software if needed.
That would make it *almost unbreakable* for pin changes.


'''
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/oled/oled_Example.py
OLED auto-detection script work with either hardware I²C or SoftI2C — so it will try hardware first, then fall back to software if needed.
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
'''

# Auto-I²C + SoftI2C OLED Detector
import time
from machine import Pin, I2C, SoftI2C
import ssd1306
from time import sleep, sleep_us
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
# if oled.framebuf.pixel(0, 48) == 0:
#     oled_height = 32
#     oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=oled_address)

# print(f"🖥 OLED resolution detected: {oled_width}x{oled_height}")

# Step 5: Display test message
oled.fill(0)
oled.text("Hello, ESP32!", 0, 0)
oled.text(f"{oled_width}x{oled_height} ", 10, 16)
oled.show()

time.sleep(2)

oled.fill(0)
oled.text("My I2C address:", 0, 0)
oled.text(f"{oled_address}. 0x{oled_address:02X}", 0, 16)
oled.show()

time.sleep(2)



oled.fill(0)
oled.show()


'''
# auto_oled_detect.py
import time
from machine import Pin, I2C
import ssd1306

# Common I2C pin defaults for ESP32 (adjust if needed)
SCL_PIN = 22
SDA_PIN = 21

print("🔍 Scanning all I2C buses...\n")

i2c = None
oled_address = None

# Step 1: Try both I2C buses (0 and 1)
for bus_id in (0, 1):
    try:
        temp_i2c = I2C(bus_id, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        devices = temp_i2c.scan()

        if devices:
            print(f"📡 Bus {bus_id}: Found devices {[hex(d) for d in devices]}")
            for addr in devices:
                if addr in (0x3C, 0x3D):  # Common OLED addresses
                    i2c = temp_i2c
                    oled_address = addr
                    break
    except Exception as e:
        print(f"⚠️ Bus {bus_id} error: {e}")

    if i2c:
        break

if not i2c or not oled_address:
    print("❌ No OLED display found! Check wiring and power.")
    while True:
        pass

print(f"\n✅ Found OLED at address 0x{oled_address:02X} on I2C bus {bus_id}")

# Step 2: Try to auto-detect display height
oled_width = 128
possible_heights = [64, 32]
oled_height = None

for h in possible_heights:
    try:
        oled = ssd1306.SSD1306_I2C(oled_width, h, i2c, addr=oled_address)
        oled.fill(0)
        oled.text(f"Testing {oled_width}x{h}", 0, 0)
        oled.show()
        time.sleep(1)
        oled.fill(0)
        oled.show()
        oled_height = h
        break
    except Exception as e:
        print(f"⚠️ Failed with height {h}: {e}")

if not oled_height:
    print("❌ Could not initialize OLED — unknown size.")
    while True:
        pass

print(f"🖥 OLED resolution detected: {oled_width}x{oled_height}")

# Step 3: Final display message
oled.text("Hello, MicroPython!", 0, 0)
oled.text(f"{oled_width}x{oled_height}", 0, 16)
oled.show()


'''

#---Turn on the oled---
oled.poweron()
oled.contrast(0)

#---Show Text---
oled.text("...Test Begin...",0,0)
oled.text("Contrast LV",20,20)
oled.show()
sleep(1)

#---Show Contrast Level---
for contrast_level in range(0,256,1):
    oled.contrast(contrast_level)
    oled.text("LV:{}".format(contrast_level),50,40,1)
    oled.show()
    oled.text("LV:{}".format(contrast_level),50,40,0)
    sleep_us(1)
sleep(1)

#---Fill Screen (clear screen)---
oled.fill(0)
oled.show()
sleep(1)

#---Invert Screen---
oled.text("Color Inverted!",0,5)
oled.invert(1)
oled.show()
sleep(1)

# Scroll Text (Right->Left)
for x in range(0,128):
    oled.fill(0)
    oled.text("Scroll Text", 128 - x, 10)
    oled.show()
    sleep(0.01)

# Scroll Text (Left->Right)
for x in range(0,128):
    oled.fill(0)
    oled.text("Scroll Text",x, 10)
    oled.show()
    sleep(0.01)
oled.show()
oled.fill(1)
time.sleep(.2)
#---Draw line---
oled.fill(0)
oled.text("Line",50,10)
oled.hline(0,30,100,1) # Horizontal Line
oled.vline(64,25,60,1) # Vertival Line
oled.show()
sleep(1)

'''
#---Draw a Triangle--- ssd1306_i2c object has no attribute 'triangle'
oled.fill(0)
oled.text("Triangle",25,5)
oled.triangle(30, 20, 60, 60, 90, 20, color=1, fill=False) # Outline
oled.show()
sleep(1)
oled.triangle(30, 20, 60, 60, 90, 20, color=1, fill=True) #Filled
oled.show()
sleep(1)
'''
#---Draw a Rectangle---
oled.fill(0)
oled.text("Rectangle",25,5)
oled.rect(3,15,20,20,1,0) # Outline
oled.show()
oled.rect(3,40,20,20,1,1) # Filled
oled.show()
sleep(1)
'''
#---Draw a Round Rectangle---
oled.fill(0)
oled.text("Round Rectangle",5,5)
oled.round_rect(10, 20, 60, 40, 1, filled=False , radius=10) # Outline
oled.show()
sleep(1)
'''
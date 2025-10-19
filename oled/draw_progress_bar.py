''' i copied the 'auto_bus_detect_oled.py'''

import time
from machine import Pin, I2C, SoftI2C
import ssd1306
import sys
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

print("🔍 Scanning for OLED oled...\n")

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

# Step 5: oled test message
oled.fill(0)
oled.text("Hello, ESP32!", 0, 0)
oled.text(f"{oled_width}x{oled_height} ", 10, 16)
oled.show()

time.sleep(5)

oled.fill(0)
oled.text("My I2C address:", 0, 0)
oled.text(f"{oled_address}. 0x{oled_address:02X}", 0, 16)
oled.show()

time.sleep(5)



oled.fill(0)
oled.show()







oled.fill(0)                         # fill entire screen with colour=0
oled.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to width=107, height=53, colour=1

# draw battery percentage
x_pos = [12, 38, 64, 90]
percentages = [.25, .50, .75, 1.0]

try:
    while True:
        for ctr in range(4):
            oled.fill_rect(x_pos[ctr],11,24,40,1)
            oled.fill_rect(0,56,128,40,0)
            oled.text("{:.0%}".format(percentages[ctr]), 11, 56)
            oled.show()
            time.sleep_ms(1000)
        
        # This will clear the battery charge percentage
        for ctr in range(4):
            oled.fill_rect(x_pos[ctr],11,24,40,0)
            
        oled.show()
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print('Program Ending')
    sys.exit()
               






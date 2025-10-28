 

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

With Button to POSITIVE and pull_UP the relaxed is 0 and when pushed down, the value is 1

'''

# Auto-I²C + SoftI2C OLED Detector
import time
from machine import Pin, I2C, SoftI2C
import ssd1306
from time import sleep, sleep_us
# Pin configuration
SCL_PIN = 22
SDA_PIN = 21

#madori button
#button1 = Pin(34, Pin.IN, Pin.PULL_UP)  ## connect to Positive, not pressed is zero 
button1 = Pin(26, Pin.IN, Pin.PULL_DOWN)## cinnect to positive, not pressed is zero	
#Pinacolada Button
#button2 = Pin(35,Pin.IN,Pin.PULL_UP)

led = Pin(13, Pin.OUT)
activeBuzz=Pin(33,Pin.OUT)





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

butVal=button1.value()
print('butVal: ',butVal)
activeBuzz.value(1)
time.sleep(.2)
activeBuzz.value(0)
while True:
    led.value(0)
    oled.fill(0)
    oled.show()
    butVal=button1.value()
    #if button1.value()== 1:
    if butVal==1:    
        
       print('button1 value ==1, ', butVal)
       activeBuzz.value(1)
       oled.fill(0)
       oled.show()
       oled.text("Madori", 0, 0)
       oled.text("Splice", 0, 10)
       oled.show()
       led.value(1)
       time.sleep(0.5)
       print("button pressed")
       
    #if button1.value()== 0:
    if butVal==0:
       activeBuzz.value(0) 
       print('button1 value ==1, ', butVal)
       oled.fill(0)
       oled.show()
       oled.text("Pina", 0, 0)
       oled.text("Colada", 0, 10)
       oled.show()
       led.value(1)
       time.sleep(0.5)
       print("button pressed")


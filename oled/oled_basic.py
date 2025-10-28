'''
oled_basic.py located in ESP32_ESPNow
autodetects

https://docs.qmk.fm/features/oled_driver
https://duckduckgo.com/?q=Adafruit+0.96%22+128x64+OLED+Display+STEMMA+QT+Version+connections&t=osx&ia=chat
in obsidian as OLED file
second example:
Understanding the Fade Effect

The fade effect involves randomly turning off pixels in the display buffer. In MicroPython, you can achieve this by manipulating the pixel data directly.

Understanding the Logo Data

The qmk_logo array contains pixel data for a logo, where each byte represents a column of pixels. Each bit in the byte corresponds to a pixel's state (on or off). In MicroPython, you can create a similar array to represent your logo.
'''
'''
#1️⃣ OLED program with I²C device list first
#This one lists all detected I²C devices, then initializes the OLED if found.
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
'''
'''
# to use sh1106 driver oled
import machine
import sh1106
import time

# Initialize I2C
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)

# Initialize the SH1106 display
oled = sh1106.SH1106_I2C(128, 64, i2c)
'''

import machine
import ssd1306
import time
import random
import sys
oled_address = 0x3D
# Initialize I2C
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# Example logo data (8x8 pixels)
logo = [
    0b11111111,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b11111111,
    0b00000000
]
blank = [0b00000000] * 8

def draw_checkerboard(oled):
    rows = 64 // 8
    cols = 128 // 8
    for row in range(rows):
        for col in range(cols):
            # Alternate between logo and blank
            pattern = logo if (row + col) % 2 == 0 else blank
            for y in range(8):
                for x in range(8):
                    if pattern[y] & (1 << (7 - x)):
                        oled.pixel(col * 8 + x, row * 8 + y, 1)
                    else:
                        oled.pixel(col * 8 + x, row * 8 + y, 0)
    oled.show()

def fade_display(oled):
    for y in range(0, 64):
        for x in range(0, 128):
            if random.randint(0, 1):
                oled.pixel(x, y, 0)  # Turn off the pixel
    oled.show()
try:
    # Main loop
    while True:
        oled.fill(0)  # Clear the display
        draw_checkerboard(oled)  # Render the logo
        time.sleep(2)  # Display the logo for 2 seconds
        fade_display(oled)  # Apply the fade effect
        time.sleep(2)  # Wait before repeating
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    time.sleep(1)
    sys.exit()
        
## checkerboard
# import machine
# import ssd1306
# import time
# import random

# oled_address = 0x3D
# # Initialize I2C
# i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
# oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

# # Example logo data (8x8 pixels)
# logo = [
#     0b11111111,
#     0b10000001,
#     0b10000001,
#     0b10000001,
#     0b10000001,
#     0b10000001,
#     0b11111111,
#     0b00000000
# ]
# blank = [0b00000000] * 8

# def draw_checkerboard(oled):
#     rows = 64 // 8
#     cols = 128 // 8
#     for row in range(rows):
#         for col in range(cols):
#             # Alternate between logo and blank
#             pattern = logo if (row + col) % 2 == 0 else blank
#             for y in range(8):
#                 for x in range(8):
#                     if pattern[y] & (1 << (7 - x)):
#                         oled.pixel(col * 8 + x, row * 8 + y, 1)
#                     else:
#                         oled.pixel(col * 8 + x, row * 8 + y, 0)
#     oled.show()

# def fade_display(oled):
#     for y in range(0, 64):
#         for x in range(0, 128):
#             if random.randint(0, 1):
#                 oled.pixel(x, y, 0)  # Turn off the pixel
#     oled.show()

# # Main loop
# while True:
#     oled.fill(0)  # Clear the display
#     draw_checkerboard(oled)  # Render the logo
#     time.sleep(2)  # Display the logo for 2 seconds
#     fade_display(oled)  # Apply the fade effect
#     time.sleep(2)  # Wait before repeating
    
    
    
## single 8 bytes logo that fades randomly    
# import machine
# import ssd1306
# import time
# import random
# oled_address = 0x3D
# # Initialize I2C
# i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
# # oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)
# # Example logo data (8x8 pixels)
# logo = [
#     0b11111111,
#     0b10000001,
#     0b10000001,
#     0b10000001,
#     0b10000001,
#     0b10000001,
#     0b11111111,
#     0b00000000
# ]


# def render_logo(oled):
#     for i in range(len(logo)):
#         for j in range(8):  # Each byte represents 8 pixels
#             if logo[i] & (1 << (7 - j)):  # Check each bit
#                 oled.pixel(j, i, 1)  # Turn on the pixel
#     oled.show()

# def fade_display(oled):
#     for y in range(0, 64):
#         for x in range(0, 128):
#             if random.randint(0, 1):
#                 oled.pixel(x, y, 0)  # Turn off the pixel
#     oled.show()

# # Main loop
# while True:
#     oled.fill(0)  # Clear the display
#     render_logo(oled)  # Render the logo
#     time.sleep(2)  # Display the logo for 2 seconds
#     fade_display(oled)  # Apply the fade effect
#     time.sleep(2)  # Wait before repeating


'''
import time		##works same as above but added extra squares and automatic i2c address identification
from machine import Pin, I2C
import ssd1306
import random
# Your I2C pin configuration (ESP32: GPIO 22 = SCL, GPIO 21 = SDA)	#works 28 oct 25
SCL_PIN = 22 #esp32
SDA_PIN = 21

#SCL_PIN = 1	#Pico
#SDA_PIN = 0
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

# Example logo data (8x8 pixels)
logo = [
    0b11111111,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b11111111,
    0b00000000
]

def render_logo(oled):
    for i in range(len(logo)):
        for j in range(8):  # Each byte represents 8 pixels
            if logo[i] & (1 << (7 - j)):  # Check each bit
                oled.pixel(j, i, 1)  # Turn on the pixel
                oled.pixel(j+10,i+10,1)
    oled.show()

def fade_display(oled):
    for y in range(0, 64):
        for x in range(0, 128):
            if random.randint(0, 1):
                oled.pixel(x, y, 0)  # Turn off the pixel
    oled.show()

# Main loop
while True:
    oled.fill(0)  # Clear the display
    render_logo(oled)  # Render the logo
    time.sleep(2)  # Display the logo for 2 seconds
    fade_display(oled)  # Apply the fade effect
    time.sleep(2)  # Wait before repeating
'''
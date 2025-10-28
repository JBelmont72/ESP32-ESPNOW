## in this program i have both the hard wired i2c connection used in first and then the software use of i2c in the second initialization

### A simple example to display text on an SSD1306 OLED display using I2C interface.
# import machine
# import ssd1306
# import time
# import random
# import sys
# oled_address = 0x3D
# # Initialize I2C. Version 1
# i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
# display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)


# a simple text display example for ssd1306 oled using SoftI2C Version 2
from machine import Pin, SoftI2C
import ssd1306

SDA_PIN = 21
SCL_PIN = 22
oled_address = 0x3D
# Initialize I2C
# using SoftI2C
i2c = SoftI2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN))
display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

display.fill(0)
display.text('SSD1306 OLED', 0, 0)
display.text('with', 0, 16)
display.text('MicroPython', 0,32)

display.show()

'''
JBelmont72/ESP32-ESPNOW/oled/sh1106_oled.py
Code  includes a function to scan for I2C devices and identify the address of the SH1106 display
Explanation of the Modifications

I2C Scanning Function:
The scan_i2c_addresses function iterates through the possible I2C addresses (from 0x03 to 0x77) and attempts to write to each address. If the write operation is successful, it means a device is present at that address, and it gets added to the devices list.
Address Check:
After scanning, the code checks if the default SH1106 address (0x3C) is in the list of found addresses. If it is found, the display is initialized; otherwise, an error message is printed.
Initialization with Address:
The SH1106_I2C initialization now includes the addr parameter to specify the I2C address.
This modified program identifies the correct I2C address for the SH1106 OLED display and ensure that it is properly initialized before displaying any content. 
'''
import machine
import sh1106
import time

# Initialize I2C
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)

def scan_i2c_addresses(i2c):
    print("Scanning I2C addresses...")
    devices = []
    for address in range(0x03, 0x77):  # I2C addresses range from 0x03 to 0x77
        if i2c.writeto(address, b'') is not None:
            devices.append(address)
            print("Found device at address: 0x{:02X}".format(address))
    return devices

# Scan for I2C addresses
found_addresses = scan_i2c_addresses(i2c)

# Check if the SH1106 display address is found
sh1106_address = 0x3C  # Default I2C address for SH1106
if sh1106_address in found_addresses:
    print("SH1106 display found at address: 0x{:02X}".format(sh1106_address))
    # Initialize the SH1106 display
    oled = sh1106.SH1106_I2C(128, 64, i2c, addr=sh1106_address)

    # Clear the display
    oled.fill(0)
    oled.show()

    # Display some text
    oled.text("Hello, World!", 0, 0)
    oled.show()

    # Keep the display on for a while
    time.sleep(5)

    # Clear the display again
    oled.fill(0)
    oled.show()
else:
    print("SH1106 display not found. Please check connections.")


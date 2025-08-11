#receiver.py 
import network
import espnow
from machine import Pin, I2C
from time import sleep
import ssd1306
import binascii

# ===== CONFIG =====
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
# ==================

def main():
    # --- 1. Activate Wi-Fi in STA mode ---
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    print("Receiver MAC:", binascii.hexlify(wlan.config('mac')).decode())

    # --- 2. Initialize ESP-NOW ---
    esp = espnow.ESPNow()
    esp.active(True)  # REQUIRED before recv() or you'll get ESP_ERR_ESPNOW_NOT_INIT

    # --- 3. Set up OLED display via I2C ---
    i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
    oled_address = None
    for addr in i2c.scan():
        if addr in [0x3C, 0x3D]:  # Common SSD1306 addresses
            oled_address = addr
            break

    if oled_address is None:
        print("OLED not found! Continuing without display.")
        oled = None
    else:
        oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

    print("Receiver ready — waiting for messages...")

    # --- 4. Main receive loop ---
    while True:
        host, msg = esp.recv()
        if msg:
            try:
                pot_val = int(msg.decode())
            except ValueError:
                pot_val = 0

            print(f"Received from {binascii.hexlify(host).decode()}: {pot_val}")

            if oled:
                oled.fill(0)
                oled.text("ESP-NOW", 30, 0)
                oled.text("Receiver", 25, 18)
                oled.text(str(pot_val), 40, 40)
                oled.show()

        sleep(0.1)

if __name__ == "__main__":
    main()

"""
receiver.py — Receives potentiometer values from ESP-NOW transmitter
and displays them on an SSD1306 OLED.

Wiring for OLED (I2C):
    ESP32 GPIO 22 -> SCL
    ESP32 GPIO 21 -> SDA
"""
'''
import network
import espnow
from machine import Pin, I2C
from time import sleep
import ssd1306
import binascii  # For converting MAC to printable format

# ====== 1. Enable Wi-Fi in station mode ======
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# ====== 2. Initialize ESP-NOW ======
try:
    esp = espnow.ESPNow()  # No .init() needed in current MicroPython
except OSError as err:
    print("Failed to initialize ESP-NOW:", err)
    raise SystemExit

print("Receiver MAC:", binascii.hexlify(wlan.config('mac')).decode())

# ====== 3. Set up I2C for OLED ======
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Detect OLED address (common: 0x3C or 0x3D)
oled_address = None
for addr in i2c.scan():
    if addr in [0x3C, 0x3D]:
        oled_address = addr
        break

if oled_address is None:
    print("OLED not found! Stopping.")
    raise SystemExit

# ====== 4. Initialize OLED display ======
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)
oled.fill(0)
oled.text("ESP-NOW Receiver", 0, 0)
oled.show()

print("Receiver ready — waiting for messages...")

# ====== 5. Main loop: receive and display data ======
while True:
    host, msg = esp.recv()  # Blocks until data arrives
    if msg:
        try:
            pot_val = int(msg.decode())  # Convert from bytes->str->int
        except ValueError:
            pot_val = 0  # If bad data, fallback to 0

        # Print to console
        print(f"From {binascii.hexlify(host).decode()}: {pot_val}")

        # Update OLED
        oled.fill(0)
        oled.text("ESP-NOW", 30, 0)
        oled.text("Receiver", 25, 18)
        oled.text(str(pot_val), 40, 40)
        oled.show()

    sleep(0.1)
'''
'''
import network
import espnow
from machine import Pin, I2C
from time import sleep
import binascii
import ssd1306

def main():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Receiver MAC:", binascii.hexlify(wlan.config('mac')).decode())

    esp = espnow.ESPNow()

    i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    oled_address = next((addr for addr in i2c.scan() if addr in [0x3C, 0x3D]), None)

    if oled_address is None:
        print("OLED not found!")
        return

    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=oled_address)

    print("Receiver ready — waiting for messages...")
    while True:
        host, msg = esp.recv()
        if msg:
            try:
                pot_val = int(msg.decode())
            except:
                pot_val = 0

            oled.fill(0)
            oled.text("ESP-NOW", 30, 0)
            oled.text("Receiver", 25, 18)
            oled.text(str(pot_val), 40, 40)
            oled.show()
            print(f"Received from {binascii.hexlify(host).decode()}: {pot_val}")
        sleep(0.1)
if __name__ == '__main__':
    main()
'''
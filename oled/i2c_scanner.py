'''
2️⃣ Standalone I²C Scanner
This is a generic I²C scanner you can use to check all devices connected to ESP32.


'''
from machine import Pin, I2C

# Pin configuration
SCL_PIN = 22
SDA_PIN = 21

print("🔍 Scanning I2C buses...\n")

found_any = False

for bus_id in (0, 1):
    try:
        i2c = I2C(bus_id, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        devices = i2c.scan()

        if devices:
            found_any = True
            print(f"I2C bus {bus_id}: Found {len(devices)} device(s):")
            for addr in devices:
                print(f"  - Address: 0x{addr:02X}")
        else:
            print(f"I2C bus {bus_id}: No devices found.")
    except Exception as e:
        print(f"I2C bus {bus_id}: Error -> {e}")

if not found_any:
    print("\n❌ No I2C devices detected. Check wiring and power.")

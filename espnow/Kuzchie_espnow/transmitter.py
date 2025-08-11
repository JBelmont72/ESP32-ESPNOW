## transmitter.py is from Kuxchie_transmitter.py 
# note there are two versions of ESPNOW, the newer one does not have init
# to check modules: >>> import espnow
#   >>>dir(espnow)  

# output:  NO INIT is here ['__class__', '__name__', '__dict__', '__file__', 'ADDR_LEN', 'ESPNowBase', 'KEY_LEN', 'MAX_DATA_LEN', 'MAX_ENCRYPT_PEER_NUM', 'MAX_TOTAL_PEER_NUM', 'ESPNow']
#  Best approach for PEER_MAC
#If you have a MAC in string form (like "B0B21CA93A5C"), do:
#PEER_MAC = bytes.fromhex("B0B21CA93A5C")
#If you already have it as b'\xb0\xb2\x1c\xa9:\\', just use it directly.
'''Changes I made:
Removed try: esp — replaced with a proper try/except around object creation.
Fixed PEER_MAC to always be a 6-byte bytes object.
Kept your ADC + send loop as-is.
Kept it compatible with your pushbutton main.py.
'''
import network
import espnow
from machine import ADC, Pin
from time import sleep
import binascii

# ===== CONFIG =====
POT_PIN = 36
SEND_DELAY = 0.5
PEER_MAC = b'\xb0\xb2\x1c\xa9\x3a\x5c'  # <-- Replace with receiver's MAC
# ==================

def main():
    # --- 1. Activate Wi-Fi in STA mode ---
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)      # Must be active before ESP-NOW
    wlan.disconnect()      # Not strictly needed, but keeps it clean
    print("Transmitter MAC:", binascii.hexlify(wlan.config('mac')).decode())

    # --- 2. Initialize ESP-NOW ---
    esp = espnow.ESPNow()
    esp.active(True)       # REQUIRED or you'll get ESP_ERR_ESPNOW_NOT_INIT

    # --- 3. Add peer (receiver) ---
    esp.add_peer(PEER_MAC)

    # --- 4. Set up ADC for potentiometer ---
    pot = ADC(Pin(POT_PIN))
    pot.atten(ADC.ATTN_11DB)     # Full 0–3.3V range
    pot.width(ADC.WIDTH_10BIT)   # 0–1023 resolution

    print("Transmitter ready — sending values...")
    while True:
        pot_val = pot.read()
        print(f"Sending: {pot_val}")
        esp.send(PEER_MAC, str(pot_val))  # Send value as bytes/string
        sleep(SEND_DELAY)

if __name__ == "__main__":
    main()

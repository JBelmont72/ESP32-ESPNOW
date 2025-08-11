# Exploring ESP-NOW in MicroPython: A Learner's Guide

## Write Up
https://www.donskytech.com/exploring-esp-now-in-micropython-a-learners-guide/

![Featured Image - ESP-NOW in MicroPython](https://github.com/donskytech/micropython-ESP32-ESP8266/assets/69466026/20d5b8f1-d953-4945-a0d3-e96d63c035bb)

## transmitter.py is from Kuxchie_transmitter.py 
# note there are two versions of ESPNOW, the newer one does not have init
# to check modules: >>> import espnow
    >>>dir(espnow) 

# output:  NO INIT is here ['__class__', '__name__', '__dict__', '__file__', 'ADDR_LEN', 'ESPNowBase', 'KEY_LEN', 'MAX_DATA_LEN', 'MAX_ENCRYPT_PEER_NUM', 'MAX_TOTAL_PEER_NUM', 'ESPNow']
#  Best approach for PEER_MAC

If you have a MAC in string form (like "B0B21CA93A5C"), do:
PEER_MAC = bytes.fromhex("B0B21CA93A5C")
If you already have it as b'\xb0\xb2\x1c\xa9:\\', just use it directly.
JBelmont72/ESP32-ESPNOW/espnow/espnow_init
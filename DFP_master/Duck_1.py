''''


use pyserial
'''
# from machine import Pin, UART
# import time

# # Initialize UART (TX = Pin 17, RX = Pin 16)
# uart = UART(2, baudrate=9600, tx=19, rx=21)
# busy = Pin(5, Pin.IN, Pin.PULL_UP)  # Use internal pull-up

# # Functions to send commands to DFPlayer
# def send_command(cmd):
#     uart.write(cmd)
#     uart.write(b'\x0A')  # Write a line feed at the end

# def play_track(track_number):
#     cmd = bytearray([0x7E, 0xFF, 0x06, 0x03, track_number, 0xB5])
#     send_command(cmd)

# def set_volume(volume):
#     cmd = bytearray([0x7E, 0xFF, 0x06, 0x01, volume, 0xB4])
#     send_command(cmd)

# # Setup
# time.sleep(2)  # Wait for DFPlayer to initialize
# set_volume(20)  # Set volume 0-30
# play_track(1)   # Play track 1 (0001.mp3)

# while True:
#     busyVal = busy.value()
#     print("Busy pin value:", busyVal)

#     # Additional debug message
#     print("Playing track 1")
    
#     time.sleep(0.5)


# Paste and run on your ESP32 - adjust pins if needed
# from machine import UART, Pin
# import time

# uart = UART(2, baudrate=9600, tx=Pin(19), rx=Pin(21))  # keep your current pins
# print("Listening for bytes from DFPlayer... Ctrl-C to stop")

# try:
#     while True:
#         if uart.any():
#             b = uart.read()
#             # print readable hex
#             print("RX:", " ".join("{:02X}".format(x) for x in b))
#         time.sleep(0.05)
# except KeyboardInterrupt:
#     print("Stopped.")


from machine import Pin, UART
import time

# Initialize UART (TX = Pin 17, RX = Pin 16)
# uart = UART(2, baudrate=9600, tx=19, rx=21)
# uart = UART(2, baudrate=9600, tx=17, rx=16)# for esp32
uart = UART(2, baudrate=9600, tx=17, rx=13)# for lilygo T-display
pin_led = Pin(5, Pin.OUT)  # Optional: Used for debugging

# Send a test command
def send_command(command):
    uart.write(command)
    uart.write(b'\x0A')  # Line feed

# Test sending a volume command
def set_volume(volume):
    cmd = bytearray([0x7E, 0xFF, 0x06, 0x01, volume, 0xB4])
    send_command(cmd)

# Test setup
set_volume(20)  # Set volume to 20

while True:
    pin_led.value(1)  # Turn LED on for debugging
    time.sleep(0.5)
    pin_led.value(0)  # Turn LED off
    time.sleep(0.5)

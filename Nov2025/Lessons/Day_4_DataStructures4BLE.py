'''
ready to return to BLE.
Because:
You know how to parse commands
You know how to handle optional arguments
You can build a command processor for the peripheral
You can build a central that sends commands
You can receive UTF-8 strings reliably
You know how to convert strings into numbers safely
This is exactly the skill needed to make BLE motor control, LED control, and ADC reporting work cleanly.
'''
'''
# dictionary practice
device = {
    "name": "ESP32",
    "adc": 123,
    "led_state": False
}

device["led_state"] = True
device["adc"] += 5

print(device)
inventory = {}
inventory["apples"] = 10
inventory["oranges"] = 4
inventory["apples"] += 6

print(inventory)
'''

from machine import Pin

led = Pin(22, Pin.OUT)

def led_on():
    led.value(1)
    return "OK LED_ON"

def led_off():
    led.value(0)
    return "OK LED_OFF"

command_table = {
    "LED_ON":  led_on,
    "LED_OFF": led_off,
}
def execute_command(cmd):
    cmd = cmd.strip()

    if cmd in command_table:
        return command_table[cmd]()
    else:
        return "ERR Unknown command"



result = command_table["LED_ON"]()
print(result)


print(execute_command("LED_ON"))
print(execute_command("LED_OFF"))
print(execute_command("BANANA"))   # ERR Unknown command

'''
BLE command system
If you're ready, we proceed to:
BLE Peripheral
Sends ADC
Receives commands like:
LED ON
LED OFF
SET_RATE 0.80
SET_SPEED 45
SET_MODE AUTO
SET_UP 100 5 15 yes
BLE Central
Button or terminal sends commands
Displays ADC & responses'''
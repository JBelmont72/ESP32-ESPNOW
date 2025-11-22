'''
function one flashes led on/off based on command strings
'''
from machine import Pin
from time import ticks_ms, ticks_diff, sleep
led = Pin(22, Pin.OUT)
led2 = Pin(23, Pin.OUT)
led2.value(0)
def led_on():
    led.value(1)
    return "OK LED_ON"

def led_off():
    led.value(0)
    return "OK LED_OFF"
def mySleep(val=300):
    # sleep expects seconds; convert ms to seconds
    sleep(val / 1000)
    return "OK Sleep {}ms".format(val)
    
# use a dictionary to map commands to functions
command_table = {
    "LED_ON":  led_on,
    "LED_OFF": led_off,
    "Sleep": mySleep,
    
}

def execute_command(cmd):
    cmd = cmd.strip()

    if cmd in command_table:
        return command_table[cmd]()
    else:
        return "ERR Unknown command"
# test the command table
result = command_table["LED_ON"]()
print(result)
result=command_table["Sleep"]
print(result(500))  # sleep for 500 ms  
result = command_table["LED_OFF"]()
print(result)   



# below works but will try with another way next
# try: 
#     while True:
#         cmd = input("Enter command: ")
#         if cmd == "EXIT":
#             response = command_table["LED_OFF"]()
#             print(response)
#             break
#         response = command_table.get(cmd, lambda: "ERR Unknown command")()
#         print(response)
# except KeyboardInterrupt:
#     print('exit')                                       
#     result = command_table["LED_OFF"]()
#     print(result)
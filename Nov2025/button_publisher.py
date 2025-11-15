'''button_publisher.py 
I run led_mqtt_server.py  on the pico with a pushbutton on pin 16

on the other picoW I have the led_mqtt_server.py with the led on pin 16.  I used main.py to trigger calling the program
when I hold the button to 1 when powered on.
 
'''
## first is for regular button press, below this is for long button press
'''
import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Wi-Fi and MQTT Settings
SSID = "SpectrumSetup-41"         # Your Wi-Fi SSID
PASSWORD = "leastdinner914" # Your Wi-Fi password
BROKER = "broker.hivemq.com"    # Public MQTT broker
TOPIC = "led/control"           # Same topic for controlling the LED

# Button connected to Pin 14
button = Pin(16, Pin.IN, Pin.PULL_DOWN)  # Internal pull-up resistor
last_state = 1  # Button released state
led_state = 0   # Initial LED state (OFF)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    print("Connected to Wi-Fi. IP:", wlan.ifconfig()[0])

# Send MQTT message
def send_command(client, command):
    client.publish(TOPIC, command)
    print(f"Sent: {command}")

# Main program
def run_button_control():
    global last_state, led_state
    client = MQTTClient("button_publisher", BROKER)
    client.connect()
    print("Connected to MQTT broker")

    while True:
        button_state = button.value()
        
        # Button press detected (falling edge)
        if button_state == 0 and last_state == 1:
            led_state = 1 - led_state  # Toggle LED state
            if led_state == 1:
                send_command(client, "ON")  # Turn LED ON
            else:
                send_command(client, "OFF")  # Turn LED OFF
            time.sleep(0.2)  # Debounce delay

        last_state = button_state
        time.sleep(0.05)  # Small delay to prevent rapid toggling

# Connect to Wi-Fi and run the button control
connect_wifi()
run_button_control()
'''
'''
import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import secrets
# Wi-Fi and MQTT Settings
SSID = "SpectrumSetup-41"         # Your Wi-Fi SSID
PASSWORD = "leastdinner914" # Your Wi-Fi password
BROKER = "broker.hivemq.com"    # Public MQTT broker
TOPIC = "led/control"           # Same topic for controlling the LED

# Button connected to Pin 14
button = Pin(16, Pin.IN, Pin.PULL_DOWN)  # Internal pull-up resistor
last_state = 1  # Button released state
led_state = 0   # Initial LED state (OFF)

# Long press settings
LONG_PRESS_DURATION = 2000  # 2000ms (2 seconds)
button_pressed_time = 0
long_press_detected = False

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    print("Connected to Wi-Fi. IP:", wlan.ifconfig()[0])

# Send MQTT message
def send_command(client, command):
    client.publish(TOPIC, command)
    print(f"Sent: {command}")

# Handle short and long presses
def handle_button_press(client):
    global led_state, long_press_detected

    # Short press: Toggle LED
    if not long_press_detected:
        led_state = 1 - led_state  # Toggle LED state
        if led_state == 1:
            send_command(client, "ON")  # Turn LED ON
        else:
            send_command(client, "OFF")  # Turn LED OFF
    else:
        # Long press: Trigger another action (e.g., send RESET command)
        send_command(client, "LONG_PRESS_ACTION")
        print("Long press detected - Extra action executed!")
        long_press_detected = False  # Reset long press detection

# Main program
def run_button_control():
    global last_state, button_pressed_time, long_press_detected

    client = MQTTClient("button_publisher", BROKER)
    client.connect()
    print("Connected to MQTT broker")

    while True:
        button_state = button.value()

        # Button press detected (falling edge)
        if button_state == 1 and last_state ==0:
        #if button_state == 0 and last_state == 1:
            button_pressed_time = time.ticks_ms()
            long_press_detected = False  # Reset long press state
            time.sleep(0.02)  # Debounce delay

        # Button released (rising edge)
        elif button_state == 0 and last_state == 1:
        #elif button_state == 1 and last_state == 0:
            press_duration = time.ticks_ms() - button_pressed_time

            # Long press detection
            if press_duration >= LONG_PRESS_DURATION:
                long_press_detected = True
                print("Long press detected!")
            else:
                print("Short press detected!")

            # Handle button press (short or long)
            handle_button_press(client)
            time.sleep(0.2)  # Debounce delay

        last_state = button_state
        time.sleep(0.05)  # Small delay to prevent rapid toggling

# Connect to Wi-Fi and run the button control
connect_wifi()
run_button_control() 
'''
'''
import time 
fr om machine import Pin

butPin=16
Button=Pin(butPin,Pin.IN,Pin.PULL_DOWN)

while True:
    ButVal=Button.value()
    print(ButVal)
    time.sleep(1)
'''
'''
'''
import time		## this works as a toggle
from machine import Pin

buttonPin=15
Button=Pin(buttonPin,Pin.IN,Pin.PULL_DOWN)
gPin=16
gLed=Pin(gPin,Pin.OUT)
LedState=False
oldButVal=0
while True:
    newButVal=Button.value()
    print(f'{oldButVal}   {newButVal}')
    time.sleep(0.4)
    if oldButVal == 0 and newButVal == 1:  ## this triggers when button let up
        if LedState == False:
            print(f'The new ButtonVal is {newButVal} and LedState i {LedState}.')
            print('Turn the green led on.')
            gLed.value(1)
            
            LedState = True

        elif LedState == True:
            gLed.value(0)
            print('Green Led is turned off')

            LedState = False

    oldButVal= newButVal
'''
## this works as a toggle, try  to make a long push trigger ledPin  red 17 def blink():
import time
from machine import Pin

buttonPin=15
button=Pin(buttonPin,Pin.IN,Pin.PULL_DOWN)
gPin=16
gLed=Pin(gPin,Pin.OUT)
rPin = 17
rLed = Pin(rPin,Pin.OUT)
button_pressed_time = time.ticks_ms()
button_state =1
last_state = 0

LONG_PRESS_DURATION = 600
gLed.value(0)

def handle_button_press():
        global long_press_detected
        print('pressed')
        if not long_press_detected == True:
            for i in range(6):
                gLed.toggle()
                time.sleep(.5)
        else:
            for i in range(10):
                rLed.toggle()
                time.sleep(.2)
        long_press_detected =False    
while True:
        button_state = button.value()

        # Button press detected (falling edge)
        if button_state == 1 and last_state ==0:
        #if button_state == 0 and last_state == 1:
            print(f'{button_state}   {last_state} falling edge')
            button_pressed_time = time.ticks_ms() ## !! this MARKS when the time when button is pressed  and button_state ==1
            long_press_detected = False  # Reset long press state
            time.sleep(0.02)  # Debounce delay

        # Button released (rising edge)
        elif button_state == 0 and last_state == 1:
        #elif button_state == 1 and last_state == 0:
            press_duration = time.ticks_ms() - button_pressed_time

            # Long press detection
            if press_duration >= LONG_PRESS_DURATION:
                long_press_detected = True
                print("Long press detected!")
            else:
                print("Short press detected!")

            # Handle button press (short or long)
            handle_button_press()
            time.sleep(0.2)  # Debounce delay

        last_state = button_state
        time.sleep(0.05)  # Small delay to prevent rapid toggling
'''
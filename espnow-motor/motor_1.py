'''

'''
# motor.py
from machine import Pin
import time

# Define motor control pins
motor_in1 = Pin(23, Pin.OUT)  # IN1 pin
motor_in2 = Pin(22, Pin.OUT)  # IN2 pin

def motor_forward():
    motor_in1.on()  # Set IN1 high
    motor_in2.off()  # Set IN2 low

def motor_backward():
    motor_in1.off()  # Set IN1 low
    motor_in2.on()  # Set IN2 high

def motor_stop():
    motor_in1.off()  # Set IN1 low
    motor_in2.off()  # Set IN2 low

# Example usage
motor_forward()
time.sleep(2)  # Run motor forward for 2 seconds
motor_stop()
time.sleep(1)  # Stop for 1 second
motor_backward()
time.sleep(2)  # Run motor backward for 2 seconds
motor_stop()

'''
bme_testt_1.py   works great 

'''
from machine import Pin, I2C        #importing relevant modules & classes
from time import sleep
import BME280       #importing BME280 library
'''
i2c=I2C(1,sda=Pin(2), scl=Pin(3), freq=400000)    #initializing the I2C method 


while True:
  bme = BME280.BME280(i2c=i2c)          #BME280 object created
  print(bme.values)
  C,BP,H=bme.values
  print(C)
  print(BP)
  print(H)
  sleep(10)           #delay of 10s
  
'''
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, I2C
from time import sleep
import BME280

# Initialize I2C communication
i2c = I2C(id=1, scl=Pin(3), sda=Pin(2), freq=10000)

while True:
    try:
        while True:
          bme = BME280.BME280(i2c=i2c)          #BME280 object created
          print(bme.values)
          C,BP,H=bme.values
          print(C)
          print(BP)
          print(H)
          sleep(10)           #delay of 10s
          

    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)

    sleep(5)
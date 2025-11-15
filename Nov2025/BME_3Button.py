'''    
create the custom character by calling lcd.custom_char() and pass a number between 0-7 (allocated location) and the variable containing the bytearray as parameters inside it.
  
lcd.custom_char(0, heart)
lcd.custom_char(1, face)
lcd.putstr(chr(0)+" ESP32 with I2C LCD "+chr(1))

https://www.tomshardware.com/how-to/lcd-display-raspberry-pi-pico
this is used tieht the pico_i2c_lcd library and the lcd_api library
https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/
https://microcontrollerslab.com/i2c-lcd-esp32-esp8266-micropython-tutorial/

The I2C pin in ESP32 for SDA is GPIO21 and for SCL is GPIO22. 
SEE at bottom for the modification for ESP32 !
needs both of the libraries from the LCD workspace   pico_i2c_lcd    and lcd_api i have in LCD libraries

to produce custom characters
https://maxpromer.github.io/LCD-Character-Creator/




if want to use the 9 pin  lcd connection then  follow this tutorial:

https://circuitdigest.com/microcontroller-projects/interfacing-raspberry-pi-pico-with-16x2-lcd-using-micropython
Below is excellent article on the display itself, good pin info for bare metal programming/hacking
https://circuitdigest.com/article/16x2-lcd-display-module-pinout-datasheet

'''


from machine import Pin, I2C
from time import sleep
import bme280

from pico_i2c_lcd import I2cLcd

''' 
S= bytearray = ([
  0x04,
  0x0A,
  0x11,
  0x08,
  0x04,
  0x12,
  0x09,
  0x06
])

A  = bytearray([
  0x04,
  0x0E,
  0x1B,
  0x11,
  0x1F,
  0x11,
  0x11,
  0x11
])
M = bytearray ([
 0x11,
  0x1B,
  0x1F,
  0x15,
  0x11,
  0x11,
  0x11,
  0x11 
])

'''




butPin = 14
pushButton = Pin(butPin, Pin.IN, Pin.PULL_UP)

buttonState = False
buttonState3 = False
newButtonVal = 1
oldButtonVal = 1


sdaPINbme=Pin(2)
sclPINbme=Pin(3)
i2c=machine.I2C(1,sda=sdaPINbme, scl=sclPINbme, freq=400000)
bme = bme280.BME280(i2c=i2c)




i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)






while True:
    newButtonVal = pushButton.value()
    print(newButtonVal)
    sleep(1)
    print("Button Value:  ", newButtonVal)
    if newButtonVal == 0 and oldButtonVal == 1:
        if buttonState3 ==False and buttonState == False:
            lcd.putstr("Judson's Weather Station")
            sleep(3)
            
            for i in range(5):
                lcd.putstr(str(i))
                sleep(0.4)
                lcd.clear()
            sleep(1)
            
            
            
            
            
            
            buttonState = True
            
        elif  buttonState3 ==False and buttonState == True:
            print(" #2")
            lcd.clear()
            lcd.putstr("Judson's Weather Station")
           
            sleep(2)
            lcd.clear()
            t, p, h = bme.read_compensated_data()
            temperature=t/100
            p = p // 256
            pressure = p // 100
            hi = h // 1024
            hd = h * 100 // 1024 - hi * 100
            print ("{}C".format(temperature), "{}hPa".format(pressure),
            "{}.{:02d}%".format(hi, hd))
            lcd.putstr("Temp: "+str(temperature))
    
            sleep(1)
            lcd.clear()
            lcd.putstr("Humidity: "+str(hi))	#note the +, a comma did not work
    
            sleep(1)
            lcd.clear()
            
            
            buttonState = False
            buttonState3 = True
            
        elif buttonState3 ==True and buttonState == False:
            print("  #3")
            heart = bytearray([0x00,0x00,0x1B,0x1F,0x1F,0x0E,0x04,0x00])
            face = bytearray([0x00,0x00,0x0A,0x00,0x11,0x0E,0x00,0x00])
            lcd.custom_char(0, heart)
            lcd.custom_char(1, face)
            lcd.putstr(chr(0)+" Success is     Sweet "+chr(1))
            sleep(2.0)
            '''
            lcd.custom_char(2, S)
            lcd.custom_char(3, A)
            lcd.custom_char(4,M)
            lcd.putstr(chr(2)+"  "+chr(3)+"  "+chr(4))
            sleep(2.0)		'''
            
            lcd.clear()
            buttonState =False
            buttonState3 = False
    oldButtonVal = newButtonVal
    
    '''
import machine
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

heart = bytearray([0x00,0x00,0x1B,0x1F,0x1F,0x0E,0x04,0x00])
face = bytearray([0x00,0x00,0x0A,0x00,0x11,0x0E,0x00,0x00])
lcd.custom_char(0, heart)
lcd.custom_char(1, face)
lcd.putstr(chr(0)+" WELCOME "+chr(1))

'''
    
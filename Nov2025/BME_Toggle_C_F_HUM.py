''' 
  
 put chr(176) to get the degree symbol, you can type Alt + 0176 using the numeric keyboard in Word, WordPad, Notepad etc and  cut and paste it into your program
'''


from machine import Pin, I2C
from time import sleep
import bme280

from pico_i2c_lcd import I2cLcd
butPin = 15
pushButton = Pin(butPin, Pin.IN, Pin.PULL_UP)

buttonState = False
buttonState3 = False
newButtonVal = 1
oldButtonVal = 1


sdaPINbme=Pin(26)
sclPINbme=Pin(27)
i2c=machine.I2C(1,sda=sdaPINbme, scl=sclPINbme, freq=400000)
bme = bme280.BME280(i2c=i2c)




i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

while True:
    newButtonVal = pushButton.value()
    t, p, h = bme.read_compensated_data()
    temperature=t/100
    p = p // 256
    pressure = p // 100
    hi = h // 1024
    hd = h * 100 // 1024 - hi * 100
    if(newButtonVal == 0 and oldButtonVal == 1):
        if buttonState == False:
            lcd.clear()
            lcd.putstr("Judson's Weather Station")
            sleep(3)
            lcd.clear()
            t, p, h = bme.read_compensated_data()
            temperature=t/100
            p = p // 256
            pressure = p // 100
            hi = h // 1024
            hd = h * 100 // 1024 - hi * 100
            print ("{}C".format(temperature), "{}hPa".format(pressure),
            "{}.{:02d}%".format(hi, hd))
            lcd.putstr("Temp C: "+str(temperature))
            tempF = temperature *(9/5) +32
            lcd.putstr("   Temp F: "+str(tempF))
            print("Temperature F:  ", tempF ,"F",chr(176))
            sleep(3)
            lcd.clear()
            buttonState = True
            
        elif buttonState == True:
            lcd.clear()
            print("temp :"+str(temperature))
            print ("{}C".format(temperature), "{}hPa".format(pressure),
            "{}.{:02d}%".format(hi, hd))
            lcd.putstr("Temp: "+str(temperature))
            lcd.putstr("      Humidity: "+str(hi))
            sleep(3)
            lcd.clear()
            buttonState = False
    oldButtonVal = newButtonVal        
    
        
        
        
        
        
       
    
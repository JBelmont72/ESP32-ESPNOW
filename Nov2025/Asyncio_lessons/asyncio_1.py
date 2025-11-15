'''
/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Nov2025/Asyncio_lessons/asyncio_1.py
[chat for learning asyncio in micropython](https://chatgpt.com/g/g-Z7UTI21rg-python-teacher/c/691153b7-0624-832e-9bf2-96bf644e7855)
i am using this first code to blink two leds at different speeds without blocking each other but it only blinks one led at a time, can you help me fix it?    
The second code is from the chat and is a recommended improvement over the first code.
Point to remember about asyncio in micropython:
1.async def defines coroutines (non-blocking functions)
2.await asyncio.sleep() pauses without freezing other tasks
3.create_task() lets both run together(place these in def  main())
4.asyncio.run(main()) then starts the event loop
5. uasyncio is the MicroPython version (lighter and correct for Pico W).
6.The infinite loop inside main() keeps it running, so you don’t need loop.run_forever().
7. asyncio.run(main()) handles setup and cleanup properly
version 3 incorporates isinstnace(). line 92
 
 
'''
'''   version 1 - original code.
 # from Random Nerds Asyncio to blink two leds with different co routines at different speeds without blocking
 # Rui Santos & Sara Santos - Random Nerd Tutorials
 # Complete project details at https://RandomNerdTutorials.com/micropython-raspberry-pi-pico-asynchronous-programming/
import asyncio
from machine import Pin
# created two led objects
green_led_pin = 17
green_led = Pin(green_led_pin, Pin.OUT)
blue_led_pin = 16
blue_led = Pin(blue_led_pin, Pin.OUT)

# Define coroutine function 
async def blink_green_led():
    while True:
        green_led.toggle()
        await asyncio.sleep(2) 

# Define coroutine function
async def blink_blue_led():
    while True:
        blue_led.toggle()
        await asyncio.sleep(1.0)

# # Define the main function to run the event loop
async def main():
    # Create tasks for blinking two LEDs concurrently
    asyncio.create_task(blink_green_led())
    asyncio.create_task(blink_blue_led())

# Create and run the event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Create a task to run the main function
#loop.run_forever()  # Run the event loop indefinitely

# i tried this way but it didnt work as expected
# try: ## this only turns the green led on and then flashes the blue one
#     while True:
#         asyncio.run(blink_green_led())
#         asyncio.run(blink_blue_led())
# except KeyboardInterrupt:
#     print("Program stopped by User")    
try:
    loop.run_forever()  # Run the event loop indefinitely, this worked
except KeyboardInterrupt:
    print("Program stopped by User")
    
'''  
'''    version 2 - improved code from chatgpt 
import uasyncio as asyncio
from machine import Pin

green_led = Pin(17, Pin.OUT)
blue_led = Pin(16, Pin.OUT)

async def blink(pin, delay):
    while True:
        pin.toggle()
        await asyncio.sleep(delay)

async def main():
    asyncio.create_task(blink(green_led, 2))
    asyncio.create_task(blink(blue_led, 1))
    while True:  # keep main alive
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    green_led.off()
    blue_led.off()  
    print("Stopped by user")
'''

''' version 3 create a program using these lessons to have three coroutines, two that blicnk leds and third that the every 5 seconds prints "Status Check!" to the console.
Point to remember about asyncio in micropython:
1.async def defines coroutines (non-blocking functions)
2.await asyncio.sleep() pauses without freezing other tasks
3.create_task() lets both run together(place these in def  main())
4.asyncio.run(main()) then starts the event loop
5. uasyncio is the MicroPython version (lighter and correct for Pico W).
6.The infinite loop inside main() keeps it running, so you don’t need loop.run_forever().
7. asyncio.run(main()) handles setup and cleanup properly
bonus: work on isinstance()
class myObj:
  name = "John"

y = myObj()

x = isinstance(y, myObj


# Set the ADC width to 12 bits (range: 0-4095)
#adc.width(ADC.WIDTH_12BIT)

while True:
    # Read the ADC value (0-4095)
    raw = adc.read()	#this is 12 bit
    raw_u16=adc.read_u16()# this is 16 bit
    
    voltage = raw / 4095 * 3.3  # Scale to voltage (0-3.3V), this is 12 bit
    #print("Raw:", raw, "Voltage:", "{:.3f} V".format(voltage))
    print("Raw:", raw,"raw_16 ", raw_u16, "Voltage:", "{:.3f} V" .format(voltage),end='\r')
    sleep(1)

'''
## above is version 3 and then an improved version 4 with isinstance() method for the adc pin
'''
import uasyncio as asyncio  # Program 3 where i added two functions, a print/count and ADC read
from machine import Pin,ADC
import sys

green_led = Pin(17, Pin.OUT)
blue_led = Pin(16, Pin.OUT)
count =1

adcPin=28
myADC=ADC(adcPin)


#create four asyncio def functions
async def led(pin,delay):
    while True:
        pin.value(1)
        await asyncio.sleep(delay)
        pin.value(0)
        await asyncio.sleep(delay)
        
async def status():
    global count
    while True:
        print(f'status check!{count} ')
        await asyncio.sleep(5) 
        count +=1       
async def newADC(pin):
    myADC=ADC(pin)
    while True:
        myADC=ADC(pin)
        Val=myADC.read_u16()
        print(f'ADC value:  {Val}')
        await asyncio.sleep(1)
    
    
       
async def main():
    asyncio.create_task(led(green_led,1))
    asyncio.create_task(led(blue_led,2))
    asyncio.create_task(status())
    asyncio.create_task(newADC(28))
    while True:
        await asyncio.sleep(1)
try:
    asyncio.run(main())

    
except KeyboardInterrupt:
    blue_led.value(0)
    green_led.value(0)
    print('exiting cleanly')
    sys.exit()
'''   
## version 4 is version 3 but incorporates isinstance method so adc does not have to be connected  
'''
Below: Used try/except around the ADC setup — safer than isinstance for hardware detection.
isinstance(adc_pin, int) ensures you only pass numbers.
ADC(adc_pin) test happens once before the coroutine runs.
If ADC setup fails, the program continues without crashing

'''   
# import uasyncio as asyncio
# from machine import Pin, ADC
# import sys

# green_led = Pin(17, Pin.OUT)
# blue_led = Pin(16, Pin.OUT)

# async def led(pin, delay):
#     while True:
#         pin.toggle()
#         await asyncio.sleep(delay)

# async def status():
#     count = 1
#     while True:
#         print(f"status check! {count}")
#         count += 1
#         await asyncio.sleep(5)

# async def read_adc(pin_num):
#     try:
#         adc = ADC(pin_num)
#         while True:
#             value = adc.read_u16()
#             print(f"ADC value: {value}")
#             await asyncio.sleep(1)
#     except Exception as e:
#         print(f"⚠️ ADC not available: {e}")

# async def main():
#     asyncio.create_task(led(green_led, 1))
#     asyncio.create_task(led(blue_led, 2))
#     asyncio.create_task(status())

#     # only create ADC task if pin number is valid
#     adc_pin = 28
#     if isinstance(adc_pin, int):
#         try:
#             _ = ADC(adc_pin)  # test initialization
#             asyncio.create_task(read_adc(adc_pin))
#         except Exception as e:
#             print(f"Skipping ADC: {e}")

#     while True:
#         await asyncio.sleep(1)

# try:
#     asyncio.run(main())
# except KeyboardInterrupt:
#     green_led.value(0)
#     blue_led.value(0)
#     print("exiting cleanly")
#     sys.exit()


## number 5 is number 4 with a second ADC added on pin27 (first adc on pin28)

# import uasyncio as asyncio
# from machine import Pin, ADC
# import sys

# green_led = Pin(17, Pin.OUT)
# blue_led = Pin(16, Pin.OUT)

# async def led(pin, delay):
#     while True:
#         pin.toggle()
#         await asyncio.sleep(delay)

# async def status():
#     count = 1
#     while True:
#         print(f"status check! {count}")
#         count += 1
#         await asyncio.sleep(5)
# '''
# # async def read_adc(pin_num):
# #     try:
# #         adc = ADC(pin_num)
# #         while True:
# #             value = adc.read_u16()
# #             print(f"ADC value: {value}")
# #             await asyncio.sleep(2)
# #     except Exception as e:
# #         print(f"⚠️ ADC not available: {e}")
# '''
# ## with a smoothing function
# async def read_adc(pin_num):
#     adc = ADC(pin_num)
#     while True:
#         total = 0
#         samples = 10
#         for _ in range(samples):
#             val =adc.read_u16()
#             print(f'val: {val}')
#             total += adc.read_u16()
#             await asyncio.sleep_ms(5)  # tiny pause between reads
#         avg = total // samples
#         print(f"Average ADC: {avg}")
#         await asyncio.sleep(1)





# async def read_adc2(pin_num):
#     try:
#         adc2=ADC(pin_num)
#         while True:
#             value=adc2.read_u16()
#             print(f'2d ADC value:  {value}')
#             await asyncio.sleep(2)
#     except Exception as e:
#         print(f'2d adc is invalid {e}')
    
# async def main():
#     asyncio.create_task(led(green_led, 1))
#     asyncio.create_task(led(blue_led, 2))
#     asyncio.create_task(status())

#     # only create ADC task if pin number is valid
#     adc_pin = 28
#     if isinstance(adc_pin, int):
#         try:
#             _ = ADC(adc_pin)  # test initialization
#             asyncio.create_task(read_adc(adc_pin))
#         except Exception as e:
#             print(f"Skipping ADC: {e}")
#     adc_pin2=27
#     if isinstance(adc_pin2,int):
#         try:
#             _=ADC(adc_pin2)
#             asyncio.create_task(read_adc2(adc_pin2))
#         except Exception as e:
#             print(f' {e}')
#     while True:
#         await asyncio.sleep(1)

# try:
#     asyncio.run(main())
# except KeyboardInterrupt:
#     green_led.value(0)
#     blue_led.value(0)
#     print("exiting cleanly")
#     sys.exit()
### ~~~~~~~~~program number 6 (started with number 3 and this will add a smoothing function)


import uasyncio as asyncio
from machine import Pin, ADC
import sys


green_led = Pin(23, Pin.OUT)
blue_led = Pin(22, Pin.OUT)

async def led(pin, delay):
    while True:
        #pin.toggle() ## pico not esp32 command
        #await asyncio.sleep(delay)
        pin.value(1)
        await asyncio.sleep(delay)  # for esp32
        pin.value(0)
        await asyncio.sleep(delay)

async def status():
    count = 1
    while True:
        print(f"status check! {count}")
        count += 1
        await asyncio.sleep(5)
'''
# async def read_adc(pin_num):
#     try:
#         adc = ADC(pin_num)
#         while True:
#             value = adc.read_u16()
#             print(f"ADC value: {value}")
#             await asyncio.sleep(2)
#     except Exception as e:
#         print(f"⚠️ ADC not available: {e}")
'''
## ~~~~~~with 1st  smoothing function
# async def read_adc(pin_num):
#     adc = ADC(pin_num)
#     while True:
#         total = 0
#         samples = 10
#         for _ in range(samples):
#             val =adc.read_u16()
#             print(f'val: {val}')
#             total += adc.read_u16()
#             await asyncio.sleep_ms(5)  # tiny pause between reads
#         avg = total // samples
#         print(f"Average ADC: {avg}")
#         await asyncio.sleep(1)
## ~~~ 2d smoothing function modified the 1st

async def read_adc(pin_num):
    
    alpha = 0.2 ## value must be less than 1.  the lower values less jumpy
    adc = ADC(pin_num)
    ema=adc.read_u16() # grab one value to start with
    last_reported=ema
    while True:
        # total = 0
        # samples = 10
        # for _ in range(samples):
        #     val =adc.read_u16()
        #     print(f'val: {val}')
        #     total += adc.read_u16()
        #     await asyncio.sleep_ms(5)  # tiny pause between reads
        # avg = total // samples
        # print(f"Average ADC: {avg}")
        # await asyncio.sleep(1)

        raw = adc.read_u16()
        ema = alpha*raw + (1-alpha)*ema
        voltage = ema / 65535 * 3.3
        if abs(ema - last_reported) > 500:
            print(raw, int(ema), round(voltage,3))
            last_reported = ema
        # if last_reported != last_reported:
        #     print(f'the smoothed value is:  {last_reported}')
        await asyncio.sleep_ms(2)
        # return ema




async def read_adc2(pin_num):
    try:
        adc2=ADC(pin_num)
        while True:
            value=adc2.read_u16()
            print(f'2d ADC value:  {value}')
            await asyncio.sleep(2)
    except Exception as e:
        print(f'2d adc is invalid {e}')
    
async def main():
    asyncio.create_task(led(green_led, 1))
    asyncio.create_task(led(blue_led, 2))
    asyncio.create_task(status())

    # only create ADC task if pin number is valid
    adc_pin = 35
    if isinstance(adc_pin, int):
        try:
            _ = ADC(adc_pin)  # test initialization
            asyncio.create_task(read_adc(adc_pin))
            #how do i use the returned value 'ema' from this function
        except Exception as e:
            print(f"Skipping ADC: {e}")
    # adc_pin2=27# pico
    adc_pin2=32# esp32
    if isinstance(adc_pin2,int):
        try:
            _=ADC(adc_pin2)
            asyncio.create_task(read_adc2(adc_pin2))
        except Exception as e:
            print(f' {e}')
    while True:
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    green_led.value(0)
    blue_led.value(0)
    print("exiting cleanly")
    sys.exit()

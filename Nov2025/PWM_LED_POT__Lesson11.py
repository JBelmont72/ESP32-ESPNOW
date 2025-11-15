from machine import PWM,Pin,ADC
from time import sleep

'''THe libfary is Machine and the methods are PWM and PIN etc

us the dot to add attributes to object, use () to add variabloes to methods
'''
outPin = 17
analogOut =machine.PWM(Pin(outPin))
#	the PWM "object" is analogOut.  we create a PWM channmel connected to outPin to create a PWM "OBJECT"

analogOut.freq(1000)
analogOut.duty_u16(0)
#	lesson 11
potPin =27
myPot = machine.ADC(potPin) #don't need machine

redLed = 16
RedLed = machine.PWM(Pin(redLed))
RedLed.freq(1000)
RedLed.duty_u16(0)
# Lesson 10 Paul McWhorter
'''
while True:
    myVoltage = float(input("What Output Voltage do you want?"))
    
    pwmVal = (65535/3.3) * myVoltage 
    if (myVoltage>= 3.3):
        pwmVal = 65535
    analogOut.duty_u16(int(pwmVal))
    print(pwmVal)
 '''   
''' two point s (0,0) and (3.3,65535)
find the slope = m =(y2-y1/ (x2-x1)   m = 65535/3.3
y =65535/ 3.3 *x  "x" is myVoltage and "Y" is duty cycle aka pwmVal
'''
''' Lesson 11 The PWM value as it increases creates maximum brightness at a very low value , WE WOULD RATHER increement slowly and be able to perseive the changes. To do this we will change the scale from 0 to 65535 to 0-16.
The two points are (0,0) & (65535, 0) and Find the slope m=
If we read 65536 , we want to turn that into 16
m = (y2-y1) / (x2-x1)   m = 16 /65535
thus   the "exponentValue" is equal to (16/65535) times potVal 
'''

while True:
    
    potVal = myPot.read_u16() #reads potVal and then need to apply it to the led
    # comment this out so we can create increments over 16 or 50 or whatever  RedLed.duty_u16(int(potVal))  # since both are 16 digit integers do not need to correct
     
    
    #print(potVal)
    voltage= potVal *3.3/65535#do not need the voltage since we are using the 16 bit unsigned integer
    print (voltage)
    sleep(1.5)
    
    #analogOut.duty_u16(int(potVal))
    exponentVal= (16/65535)*potVal		# note if potVal was maximum, the exponentVal is 16!!!WOW!!
    brightness = (2)**exponentVal		#this now gives the exponential value which as it goes trom 0 to 16 results in a doubling of the duty cylce from the potentiometer!!
    #	if 16 increments, then the exponentVal is 16/65535 times the PotVal
    #	Now take the exponentVal and use that as the exponent for the base 2 since that is whre we started.
    # if 50 increments then this exponentVal= (50/65535)*potVal
    #brightness = (1.2433**exponentVal)
    
    analogOut.duty_u16(int(brightness))
    RedLed.duty_u16(int(brightness))
    print(potVal,exponentVal,brightness)
    '''
1.	can make as many increments as desired. Let's choose 50 increments.

2.	brightness = constant to the 50th power. b=c**(1/50)
3.	How do we get the constant. We have to solve for the constant.
    65535**(1/50) =[c**50]**(1/50)
    this gives  65535**(1/50) = c

4.  thus 65535 raised to the 1 /50th power is equal to the constant
    c = 1.2433

5	thus brightness = (1.2433 ** exponentVal)

now take that exponentVal and use it as an 

'''
    



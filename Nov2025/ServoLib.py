'''
from ServoLib import servoState 
import time
myServo1=servoState(0)
myServo2=servoState(1)
while True:       
    for angle in range(0,180,2):
        myServo1.servoAngle(angle)
        myServo2.servoAngle(180-angle)
    for angle in range(180,0,-2):
        myServo1.servoAngle(angle)
        myServo2.servoAngle(180-angle
'''
import time


class servoState:
    import rp2
    from machine import Pin
    counter =0
    freq=2000000
    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW,out_shiftdir=rp2.PIO.SHIFT_RIGHT)
    def servoSet():
        wrap_target()
        mov(x,osr)
        mov(y,isr)
        set(pins,0)
        label('timeLoop')
        jmp(x_not_y,'nxt')
        set(pins,1)
        label('nxt')
        jmp(y_dec,'timeLoop')    
        wrap()  

    def __init__(self,servoPin):
        self.sm = servoState.rp2.StateMachine(servoState.counter,servoState.servoSet, servoState.freq, set_base=servoState.Pin(servoPin))# instantiation
        self.sm.active(1)
        self.sm.put(20000)
        self.sm.exec('pull()')
        self.sm.exec('mov(isr,osr)')
        print('statemachine: '+str(servoState.counter) +'  '+str(servoPin)+ 'created') 
        servoState.counter=servoState.counter +1
        
    def servoAngle(self,angle):
        pw=int(500+angle*2000/180)
        self.sm.put(pw)
        self.sm.exec("pull()")
        


''' 
def main(): 
    myServo1=servoState(0)
    myServo2=servoState(1)
    while True:
        
        for angle in range(0,180,2):
            myServo1.servoAngle(angle)
            myServo2.servoAngle(180-angle)
        for angle in range(180,0,-2):
            myServo1.servoAngle(angle)
            myServo2.servoAngle(180-angle)
'''        
if __name__=='__main__':
    myServo1=servoState(0)
    myServo2=servoState(1)
    while True:
        
        for angle in range(0,180,2):
            myServo1.servoAngle(angle)
            myServo2.servoAngle(180-angle)
        for angle in range(180,0,-2):
            myServo1.servoAngle(angle)
            myServo2.servoAngle(180-angle)

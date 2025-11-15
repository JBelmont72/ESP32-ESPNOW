import machine
import utime
import urandom
interrupt_flag = 0
debounce_time = 0
reaction_time = 0



led = machine.Pin(16, machine.Pin.OUT) 
#button = machine.Pin(15, machine.Pin.IN,machine.Pin.PULL_DOWN) 
#button = machine.Pin(15, machine.Pin.IN,machine.Pin.PULL_DOWN)
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

def button_handler(pin):
    button.irq(handler =None)
    timer_reaction = utime.ticks_diff(utime.ticks_ms(),timer_start)
    print("Your reaction time was "+ str(timer_reaction)+ " milliseconds")
print(button.value())
led.value(1)
utime.sleep(urandom.uniform(2,5))
led.value(0)
timer_start =utime.ticks_ms()

button.irq(trigger = machine.Pin.IRQ_RISING , handler = button_handler)
print(button.value())
'''
this picks up where PythonLesson.py left off
Will construct command structures for BLE 

'''

# class LedController():
#     def __init__(self,pin):
#         from machine import Pin
#         from time import ticks_ms
#         self.led =Pin(pin,Pin.OUT)
        
#     def on(self):
#         self.led.value(1)
#     def off(self):
#         self.led.value(0)

#     def ticks_ms(self, ms):
#         # raise NotImplementedError
#         self.ticks_ms(100)
        
# try:
#     a=LedController(23)
#     while True:
#         a.led.on()
#         a.ticks_ms(100)
#         a.led.off()
#         a.ticks_ms(100)
        

# except KeyboardInterrupt:
#     print('exit')        
        
## above related to the next step in creating a command structure
# class CommandProcessor:
#     def __init__(self):
#         self.tax_rate = 7.0
#         self.discount = 0.0

#     def process(self, cmd):
#         parts = cmd.strip().split()

#         if parts[0] == "SET_RATE":
#             self.tax_rate = float(parts[1])
#             return "RATE_OK"

#         if parts[0] == "SET_DISCOUNT":
#             self.discount = float(parts[1])
#             return "DISCOUNT_OK"

#         if parts[0] == "CALC":
#             amount = float(parts[1])
#             total = amount * (1 + self.tax_rate/100)
#             return f"TOTAL {total}"

#         return "ERR"
# try:
    # cp = CommandProcessor()
    # print(cp.process("SET_RATE 10"))
    # print(cp.process("CALC 100"))

    # cp=CommandProcessor()
    # while True:
    #     cmd = input("Enter command: ")
    #     a=cp.process(cmd)
    #     print(a)
    #     print(cp.process(cmd))

# except KeyboardInterrupt:
#     print('exit')
# with no looping action
# cp = CommandProcessor()
# print(cp.process("SET_RATE 10"))
# print(cp.process("CALC 100"))
## EXERCISE.  Write a class:
# ShoppingCart
# with:
# attribute: list of items
# method: add_item(price)
# method: total() returns sum
# method: discount(percent) applies a discount to TOTAL
####### this needs to be reworked with the while loop caling add_item and otehr functions.
# class ShoppingCart:
     
#     def __init__(self,item,price,discount):
#         self.item=item
#         self.price=price
#         self.discount=discount
        
#     def add_item(self):
#         Item=[]
#         Item.append(self.item)
#         return Item
#     def total(self):
#         Total=[]
#         return Total
        
#     def discount(self):
#         finalPrice=self.Total  * (1-(self.discount/100))
#         print(finalPrice)
        
# myGroceries=ShoppingCart('apple','price',10)
# try:
#     while True:    
#         print(myGroceries.add_item())
#         print("Total price: ", myGroceries.total())
#         a=myGroceries.add_item()
#         print('a: ',a)
#         food=input('enter your selection')
        
        

# except KeyboardInterrupt:
#     print('exit')   
    


#####~~~~~~~~             
# class Car:
#     # Class attribute: shared by all Car instances
#     num_wheels = 4

#     def __init__(self, make, model):
#         self.make = make  # Instance attribute
#         self.model = model # Instance attribute

# # Accessing class attribute via the class
# print(f"Number of wheels for any car: {Car.num_wheels}")

# # Creating instances
# car1 = Car("Toyota", "Camry")
# car2 = Car("Honda", "Civic")

# # Accessing class attribute via instances
# print(f"Car 1 wheels: {car1.num_wheels}")
# print(f"Car 2 wheels: {car2.num_wheels}")

# # Modifying class attribute via the class
# Car.num_wheels = 6
# print(f"Updated number of wheels: {Car.num_wheels}")
# print(f"Car 1 wheels after update: {car1.num_wheels}") # Reflects the change
# print(f"Car 2 wheels after update: {car2.num_wheels}") # Reflects the change

# # Modifying class attribute via an instance (creates an instance attribute)
# car1.num_wheels = 3 # This creates a new 'num_wheels' instance attribute for car1
# print(f"Car 1 wheels after instance modification: {car1.num_wheels}")
# print(f"Car 2 wheels after instance modification: {car2.num_wheels}") # Unaffected
# print(f"Class num_wheels after instance modification: {Car.num_wheels}") # Unaffected
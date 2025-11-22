'''Objects & Classes (OOP Essentials for BLE Commands)
We will ONLY cover the parts you need — no theory fluff.
You will use OOP later to organize:
BLE commands
motor controllers
LED controllers
ADC readers
“device states” (connected, disconnected, etc.)

'''
# class Dog:
#     def __init__(self, name): # note the constructor has 'name' in it as arguement
#         self.name = name

#     def bark(self):
#         print(self.name, "says woof!")


# try: 
#     while True:
#         name ='Rover'
#         lab=Dog(name)
#         lab.bark()
#         name=str(input('name of dog\n'))
# except KeyboardInterrupt:
#     print('break')

### CLass with internal state.  (no argument in the init method)
# class Counter:
#     def __init__(self): # note the constructor does not have the arguement in it
#         self.value = 0

#     def add(self, amount=1):
#         self.value += amount
#         return self.value
# myMath=Counter()
# val=myMath.add(4)   # value is 4 add 1
# print(val)
# val=myMath.add()
# print(val)
# val=myMath.add(5)
# print(val)

## 3. BLE-Related Example — LED Controller Object
# The  ESP32 peripheral will use this structure.

# from machine import Pin
# # from time import sleep    # either import here or in the class method okay

# class LedController:
#     def __init__(self, pin):
#         self.led = Pin(pin, Pin.OUT)
#         self.led = Pin(pin, Pin.OUT)
#     def on(self):
#         self.led.value(1)

#     def off(self):
#         self.led.value(0)
#     def sleep_one_second(self):
#         from time import sleep
#         sleep(1)

# pin=23
# my_led=LedController(pin)

# try:
#     while True:
#         my_led.on()
#         my_led.sleep_one_second()
#         my_led.off()
#         my_led.sleep_one_second()
# except KeyboardInterrupt:
#     print('break')

# 4. Command Processor Class (BLE will use this!)
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
# myClass=CommandProcessor()
# a=myClass.process('SET_RATE 10')
# print(a)
# a=myClass.process('SET_DISCOUNT 10')
# print(a)
# print(myClass.process('SET_DISCOUNT 10'))

# b=myClass.process('CALC 134')
# print(b)

# ShoppingCart
# with:
# attribute: list of items
# method: add_item(price)
# method: total() returns sum
# method: discount(percent) applies a discount to total
# class ShoppingCart():# add list of items as attributes,be able to add new items with add_item(price) method, total() method to return sum of items, discount(percent) method to apply discount to total     
#     def __init__(self):
#         self.bananas=1.00
#         self.oranges=2.00
#         self.grapes=3.50
#     def add_item(self): # add item prices to total then second method 'total() returns sum and then compute price with discount
        
#         total=self.bananas+self.oranges+self.grapes
#         return total
#     def discount(self, percent):
#         total=self.add_item()
#         discount_amount=total*(percent/100)
#         discounted_total=total-discount_amount
#         return discounted_total 
# myCart=ShoppingCart()
# total=myCart.add_item()
# print('total before discount:', total)
# discounted_total=myCart.discount(10)
# print('total after discount:', discounted_total)    

##modify the shoppyng cart to add items dynamically
# class ShoppingCart():# add list of items as attributes,be able to add new items with add_item(price) method, total() method to return sum of items, discount(percent) method to apply discount to total     
#     def __init__(self):
#         self.items = []  # Initialize an empty list to store item prices

#     def add_item(self, price): # add item prices to total then second method 'total() returns sum and then compute price with discount
#         self.items.append(price)  # Add the price of the new item to the list

#     def total(self):
#         return sum(self.items)  # Return the sum of all item prices

#     def discount(self, percent):
#         total = self.total()
#         discount_amount = total * (percent / 100)
#         discounted_total = total - discount_amount
#         return discounted_total 
# myCart = ShoppingCart()
# myCart.add_item(1.00)  # Add bananas
# myCart.add_item(2.00)  # Add oranges
# myCart.add_item(3.50)  # Add grapes  and be able to add items  dynamically
# total = myCart.total()
# print('total before discount:', total)
# discounted_total = myCart.discount(10)
# print('total after discount:', discounted_total)  
###########
# modify the shopping cart to be able to add items by name and price
class ShoppingCart():# add list of items as attributes, be able to add new items with add_item(name, price) method, total() method to return sum of items, discount(percent) method to apply discount to total     
    def __init__(self):
        self.items = []  # Initialize an empty list to store items as {'name': ..., 'price': ...}

    def add_item(self, name, price): # add item by name and price
        self.items.append({'name': name, 'price': price})  # Add the new item to the list

    def total(self):
        return sum(item['price'] for item in self.items)  # Return the sum of all item prices

    def discount(self, percent):
        total = self.total()
        discount_amount = total * (percent / 100)
        discounted_total = total - discount_amount
        return discounted_total 

myCart = ShoppingCart()
myCart.add_item('bananas', 1.00)  # Add bananas
myCart.add_item('oranges', 2.00)  # Add oranges
myCart.add_item('grapes', 3.50)   # Add grapes dynamically
total = myCart.total()
print('total before discount:', total)
discounted_total = myCart.discount(10)
print('total after discount:', discounted_total)   
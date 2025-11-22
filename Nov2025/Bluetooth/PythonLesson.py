



'''
Example 4 is important because it shows how to pass a value or use a defalut value in the program. user_input=" "
| Range    | Output |
| -------- | ------ |
| 90–100   | `"A"`  |
| 80–89    | `"B"`  |
| 70–79    | `"C"`  |
| 60–69    | `"D"`  |
| below 60 | `"F"`  |
https://net-informations.com/q/py/dictapp.htm#:~:text=You%20can%20append%20a%20new%20value%20to%20an%20existing%20key%20in%20a%20dictionary%20by%20using%20the%20square%20bracket%20notation%20to%20access%20the%20key%20and%20then%20using%20the%20append%28%29%20method%20to%20add%20the%20new%20value%20to%20the%20corresponding%20list.
my_dict = {"name": ["Bill", "Gary"], "age": [35, 40]}
my_dict["name"].append("Willy")
my_dict["age"].append(32)
print(my_dict)

Optional Improvements (for later) of below 'grade' program
When you're ready, we can improve this with:
input validation
functions
formatted printing
rounding
using defaultdict(list)
computing median / mode
plotting a histogram
'''

# numGrades = int(input('Enter number of grades to be averaged and grouped: '))

# Grades = []
# Dictionary = {}
# i = 0
# total=0
# while i < numGrades:
#     grade = float(input(f'Enter grade #{i+1}: '))
#     print(f'The grade you entered is {grade}.')

#     Grades.append(grade)

#     # Assign letter grade
#     if grade >= 90:
#         letterGrade = 'A'
#     elif grade >= 80:
#         letterGrade = 'B'
#     elif grade >= 70:
#         letterGrade = 'C'
#     elif grade >= 60:
#         letterGrade = 'D'
#     else:
#         letterGrade = 'F'

#     print(f'Letter grade: {letterGrade}')

#     # Add to dictionary
#     if letterGrade in Dictionary:
#         Dictionary[letterGrade].append(grade)
#     else:
#         Dictionary[letterGrade] = [grade]

#     i += 1

# print(f'Your grades for this course are: {Grades}')
# print("Grouped by letter:", Dictionary)
# # for grade in Grades:
# #     total +=grade


# total = sum(Grades)
# print(f'Sum of grades = {total}, average = {total/len(Grades)}')
## proceed to functions
'''Write a function that:
✔ takes a number
✔ returns that number squared
✔ prints nothing inside the function
✔ use it twice
'''
# def squared(num):
#     numSq=num**2
#     return numSq
# myList=[3,5]
# for myNum in myList:
#     x=squared(myNum)
#     print(x)
'''
Exercise
Write a function called grade_info:
Input:
one number (0–100)
optional parameter: passing=60
Returns:
the letter grade ("A"–"F")
a Boolean: True if grade ≥ passing, False otherwise'''

# try:
#     while True:
#         grade= int(input('Enter your grade: '))
#         if grade >=90:
#             letterGrade='A'
#         elif grade >=80 and grade < 90:
#             letterGrade='B'
#         elif grade >70 and grade< 80:
#             letterGrade='C'
#         elif grade >60 and grade <70:
#             letterGrade='D'
#         else: 
#             letterGrade='F'
#         print('Your grade is {}'.format(letterGrade))

# except KeyboardInterrupt:
#     print('exiting')


# now make it a function version 3
# def ScoreGrade(grade,pas=60):
#         if grade >=90:
#             letterGrade='A'
#         elif grade >=80 and grade < 90:
#             letterGrade='B'
#         elif grade >70 and grade< 80:
#             letterGrade='C'
#         elif grade >60 and grade <70:
#             letterGrade='D'
#         else: 
#             letterGrade='F'
#         if grade >= pas:
#             boo =True
#         else:
#             boo =False
#         return letterGrade  , boo  
# try:
 
#     while True:
#         grade= int(input('Enter your grade: '))
#         pas=int(input('Enter a passing grade requirement.'))
  

#         a,b =ScoreGrade(grade,pas)
#         if b ==True:
#             c='passed'
#         elif b== False:
#             c='failed'
#         print('Your grade is {} and you {}'.format( a,c))
        
        
# except KeyboardInterrupt:
#     print('exiting')
# Next Ask the user for a passing requirement, but allow them to skip it by pressing Enter.user_input = input("Enter passing requirement (or press Enter for default): ")
''' this is how to do it so do not have to enter the second variable'''
'''
if user_input == "":
    a, b = ScoreGrade(grade)     # ← default 60 is used
else:
    pas = int(user_input)
    a, b = ScoreGrade(grade, pas)
'''
## version 4
# def ScoreGrade(grade, pas=60):

#     if grade >= 90:
#         letterGrade = 'A'
#     elif grade >= 80:
#         letterGrade = 'B'
#     elif grade >= 70:
#         letterGrade = 'C'
#     elif grade >= 60:
#         letterGrade = 'D'
#     else:
#         letterGrade = 'F'

#     boo = grade >= pas
#     return letterGrade, boo

# def main():
#     try:
#         while True:
#             grade = int(input("Enter your grade: "))

#             user_input = input("Enter passing grade (or press Enter for default 60): ")

#             if user_input == "":
#                 # ✔️ use default 60
#                 a, b = ScoreGrade(grade)
#             else:
#                 # ✔️ use custom passing requirement
#                 pas = int(user_input)
#                 a, b = ScoreGrade(grade, pas)

#             c = "passed" if b else "failed"
#             print("Your grade is {} and you {}.".format(a, c))

#     except KeyboardInterrupt:
#         print("exiting")
# if __name__  =='__main__':
#     main()
## version 5 another function with option of using a default or not

# def add_tax(price, rate=7.00):
#     global tax
#     if tax :
#         # rate=7.00   
#         total=price + price *(float(rate)/100)
#     else:
#         total=price + price *(float(rate)/100)
#     return total
# price=float(input('enter the price of your purchase.'))
# tax=input('enter the tax rate.') # do not convert to float yet!!! 
# if tax == "":
#     print(type(tax))# note this is str
#     a=add_tax(price)
    
#     print('price = ',a)
    
    
# else:
#     tax=float(tax)
#     a=add_tax(price,tax)
#     print('price is: ',a)
    

## cleaner version number 6
# def add_tax(price, rate=0.07):
#     total = price + price * rate
#     return total
# price = float(input("Enter the price: "))
# rate_input = input("Enter tax rate (or press Enter for 7%): ")

# if rate_input == "":
#     final = add_tax(price)            # use default 7%
# else:
#     rate = float(rate_input) / 100    # convert percent to decimal
#     final = add_tax(price, rate)

# print("Final price:", final)
#####!!!!!!!! number 7
## next:     def add_tax(price, rate=0.07, discount=0.0):
#Behavior:
# Apply discount first
# Then apply tax
# Return the final price
### !! this is what i struggled with and following is a much simpler solution (see number 8)
# def add_tax(price,rate = 7.00,discount = 0.0):
#     price =(price -(price * discount/100))*( 1+ rate/100)
#     return price

# price=float(input('Enter price.'))
# rate_input = input('Enter the tax rate') 
# discount_input =input('Enter the discount to be applied.')

# if rate_input == "":
#     if discount_input == "":
#         a=add_tax(price)
#     # elif discount:
#     else:
#         discount=float(discount_input)
#         a =add_tax(price,discount)   
# else:
#     if discount_input == "" :
#         rate=float(rate_input)
#         a=add_tax(price,rate)         
#     else:
#         rate=float(rate_input)
#         discount=float(discount_input)
#         a=add_tax(price,rate,discount)
# print(a)

#### Number 8,     this is the solution to number 7
# def add_tax(price, rate=7.00, discount=0.0):
#     price = (price - (price * discount / 100)) * (1 + rate / 100)
#     return price


# price = float(input("Enter price: "))
# rate_input = input("Enter tax rate (press Enter for default 7%): ")
# discount_input = input("Enter discount (press Enter for none): ")

# # Handle rate
# if rate_input == "":
#     rate = 7.00        # default
# else:
#     rate = float(rate_input)

# # Handle discount
# if discount_input == "":
#     discount = 0.0     # default
# else:
#     discount = float(discount_input)

# # Call function
# final_price = add_tax(price, rate, discount)

# print("Final price:", final_price)

## NUMBER 9

# def optional_float(prompt, default):
#     value = input(prompt)
#     if value == "":
#         return default
#     return float(value)


# def add_tax(price, rate=7.00, discount=0.0):
#     price = (price - price * discount / 100) * (1 + rate / 100)
#     return price

# price = optional_float("Enter price: ", 0.0)
# rate = optional_float("Enter tax rate (%): ", 7.00)
# discount = optional_float("Enter discount (%): ", 0.0)

# print("Final price:", add_tax(price, rate, discount))


# def optional_grades(prompt,default):
#     value=input(prompt)
#     if value=="":
#         return default
#     return int(value)        


# def compute_grade(grade=100,bonus=5):
#     finalGrade=grade +bonus
#     return finalGrade
            
# # grade=optional_grades(prompt,default)  SYNTAX 
# grade=optional_grades('Enter Grade',100)
# bonus =optional_grades('Earned bonus:', 5) 
# print(compute_grade(grade,bonus))

 
 ## NUMBER 10. my trial with price, add discount, add tax to remainder
 
 
# def optional_defaults(primary,default):
#     returnVal = input(primary)
#     if returnVal== "":
#         return default
#     return float(returnVal)

# def purchase_price(price,discount=10,tax=5):
#     sales_price =(price-discount/100) *(1+tax/100)
#     return sales_price


# price=optional_defaults('enter the price: ',default=100)
# discount=optional_defaults('enter any discount to be applied: ',default=10)
# tax= optional_defaults('enter state and federal tax: ',default=5)

# print(purchase_price(price,discount,tax))
###~~~~~~~~~ NUMBER 11 this below builds on above and necessary for motor control
# def optional_value(value, default, convert=float):
#     if value in (None, "", " "):
#         return default
#     return convert(value)

# def add_tax(price, rate, discount):
#     price_after_discount = price * (1 - discount/100)
#     final = price_after_discount * (1 + rate/100)
#     return final

# def process_command(cmd):
#     parts = cmd.strip().split()

#     if parts[0] == "SET_TAX":           # example: "SET_TAX 7 10"
#         price = float(parts[1])
#         rate = optional_value(parts[2] if len(parts) > 2 else "", 7.0)
#         discount = optional_value(parts[3] if len(parts) > 3 else "", 0.0)

#         final = add_tax(price, rate, discount)
#         return f"TAX_CALC {final}"

#     return "ERR Unknown command"

# print(process_command('SET_TAX 17 10'))
# process_command('SET_TAX 17 10')

# # repeat fo 11
# def optional_value(value, default, convert=float):
#     if value in (None, "", " "):
#         return default
#     return convert(value)

# def add_tax(price, rate, discount):
#     price_after_discount = price * (1 - discount / 100)
#     final = price_after_discount * (1 + rate / 100)
#     return final

# def process_command(cmd):
#     parts = cmd.strip().split()

#     if parts[0] == "SET_TAX":
#         price = float(parts[1])

#         rate = optional_value(parts[2] if len(parts) > 2 else "", 7.0)
#         discount = optional_value(parts[3] if len(parts) > 3 else "", 0.0)

#         final = add_tax(price, rate, discount)
#         return f"TAX_CALC {final}"

#     return "ERR Unknown command"

# print(process_command("SET_TAX 17 10"))

## new exercise to use above format.  Inputs:
# SET_TAX 25      <-- only price
# SET_TAX 25 5    <-- price + rate
# SET_TAX 25 5 10 <-- price + rate + discount
# SET_TAX 25  " " 10   <-- force default rate, add discount

def optional_value(value, default, convert=float):
    if value in (None, "", " "):
        return default
    return convert(value)

def Gift(value, default="No"):
    if value in (None, "", " "):
        return default
    return value  # already a string

def calculate(price, rate, discount):
    price = float(price)
    rate = float(rate)
    discount = float(discount)

    price_after_discount = price * (1 - discount/100)
    final_price = price_after_discount * (1 + rate/100)
    return final_price

def myFunction(cmd):
    parts = cmd.strip().split()

    if parts[0] == "SET_UP":
        price = parts[1]

        rate = optional_value(parts[2] if len(parts) > 2 else "", 5.0)
        discount = optional_value(parts[3] if len(parts) > 3 else "", 10.0)
        gift = Gift(parts[4] if len(parts) > 4 else "", "No")
        print(parts)
        final = calculate(price, rate, discount)
        return final, gift
a=myFunction('SET_UP 25 5 10')
print(a)

b,c=myFunction('SET_UP  100')
print(b,c)
print('final price is {}. and you choose this option for gift wrapping {}'.format(b,c))
b,c=myFunction('SET_UP 100 10')

print(b,c)
print('final price is {}. and you choose this option for gift wrapping {}'.format(b,c))

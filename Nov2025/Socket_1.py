'''('192.168.1.22', '255.255.255.0', '192.168.1.1', '192.168.1.1')
https://rnascimento.com/raspberry-pi-pico-w-and-vs-code/?unapproved=383&moderation-hash=ef3cb86f6dbb6dc20ef0592e3fc13984#comment-383

definitive documnetation on connecting to internet with pico W:
https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf

https://docs.micropython.org/en/latest/library/network.WLAN.html
'''
##  https://rnascimento.com/raspberry-pi-pico-w-and-vs-code/

# import time
# import network
# import socket

# from machine import Pin

# pin = Pin("LED", Pin.OUT)

# ssid = 'NETGEAR-48'
# password = 'waterypanda901'

# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# # wlan.config(hostname="pipicoserver")
# wlan.connect(ssid, password)


# # HTML Page
# html = """<!DOCTYPE html>
# <html>
#     <head> <title>Pico W</title> </head>
#     <body> <h1>Pico W</h1>
#         <p>It's alive!</p>
#     </body>
# </html>
# """

# # Wait for connect or fail
# max_wait = 10
# while max_wait > 0:
#     if wlan.status() < 0 or wlan.status() >= 3:
#         break
#     max_wait -= 1
#     print('waiting for connection...')
#     pin.toggle()
#     time.sleep(1)

# # Handle connection error
# if wlan.status() != 5:
#     raise RuntimeError('network connection failed')
# else:
#     print('connected')
#     status = wlan.ifconfig()
#     pin.on()
#     print( 'ip = ' + status[0] )
    
# # Open socket
# addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

# s = socket.socket()
# s.bind(addr)
# s.listen(1)

# print('listening on', addr)

# # Listen for connections
# while True:
#     try:
#         cl, addr = s.accept()
#         print('client connected from: ', addr)
#         cl_file = cl.makefile('rwb', 0)
#         while True:
#             line = cl_file.readline()
#             if not line or line == b'\r\n':
#                 break
#         response = html
#         cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
#         cl.send(response)
#         cl.close
        
#     except OSError as e:
#         cl.close()
#         print('connection closed')
        
     
######  https://rnascimento.com/raspberry-pi-pico-w-and-vs-code/
import time
import network
import socket

from machine import Pin

pin = Pin("LED", Pin.OUT)

ssid = 'NETGEAR48'
password = 'waterypanda901'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# wlan.config(hostname="pipicoserver")
wlan.connect(ssid, password)

# HTML Page
html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>It's alive!</p>
    </body>
</html>
"""
#below connects to led on pico W via VSCode socket

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    pin.toggle()
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    pin.on()
    print( 'ip = ' + status[0] )
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from: ', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
'''

import time
import network
import socket

wifi =network.WLAN(network.STA_IF)
wifi.active(True)
ssid ='NETGEAR48'
password= 'waterypanda901'
wifi.connect(ssid,password)

while wifi.isconnected()==False:
    print('Waiting to connect...')
    time.sleep(.1)
wifiInfo = wifi.ifconfig()
print(wifiInfo)
ServerIP = wifiInfo[0]
ServerPort = 2222
bufferSize = 1024
UDPServer= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDPServer.bind((ServerIP,ServerPort))
message,address = UDPServer.recvfrom(bufferSize)
## need to decode the message in the 'utf-8' code
messageDecoded= message.decode('utf-8')
print(messageDecoded)

'''
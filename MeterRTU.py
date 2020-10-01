#!/usr/bin/python3
import serial
from serial import Serial
import microgear.client as microgear
import logging
import time

slaveID = (0x48)                 # Slave address of Energy Meter
FC = (0x03)                           # Function code to read Holding Registers
StartAdd_H = (0x00)        # Higher order address of Voltage register
StartAdd_L = (0x66)         # Lower order address of Voltage register
Register_H = (0x00)          # Number of registers to read Higher order address
Register_L = (0x01)           # Number of registers to read Lower order address
CRC_L = (0x6A)                   # Lower order CRC
CRC_H = (0x4C)                  # Higher order CRC

appid = “Energymeter”               # Application id
gearkey = “xxxxxxxxxx”               # Device Key
gearsecret = “xxxxxxxxxxxxx”   # Secret

microgear.create(gearkey,gearsecret,appid,{‘debugmode’ : True})

def connection():
logging.info(“Now I am connect with netpie”)

def subscription(topic,message):
logging.info(topic+” “+message)

def disconnect():
logging.info(“disconnected”)

microgear.setalias(“python_code”)
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.connect()

ser = serial.Serial(‘/dev/ttyS2’,1200,parity=serial.PARITY_EVEN)
print(ser)

data = ([slaveID,FC,StartAdd_H,StartAdd_L,Register_H,Register_L,CRC_L,CRC_H])  # request frame
data_bytes = serial.to_bytes(data)      # Representing request frame in bytes

while 1:

x = [“x[1]”,”x[2]”,”x[3]”,”x[4]”,”x[5]”,”x[6]”,”x[7]”,”x[8]”]
y = [“y[1]”,”y[2]”,”y[3]”,”y[4]”,”y[5]”,”y[6]”,”y[7]”,”y[8]”]
for i in range(1,8):
ser.write(data_bytes)     # Sending request frame to Energy meter
time.sleep(0.001)
x[i] = ser.readline(1)        # Reading response from Energy meter
y[i] = int.from_bytes(x[i],byteorder = ‘big’)   # Converting response from Energy meter o integer
vol = ((y[4]*256)+y[5])/100
print(vol)
microgear.publish(“/modbus”, vol,{‘retain’:True})  #  Publishing data to NETPIE

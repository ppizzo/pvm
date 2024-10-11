#!/usr/bin/python3

import serial, fcntl, struct, time

ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600,
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

# Write/ Read data
ser.write(b"#010\r")
s = ser.read(66)
print(s)

time.sleep(2)

ser.write(b"#013\r")
s = ser.read(63)
print(s)

ser.close()

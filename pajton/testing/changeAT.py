
import serial
import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.OUT, initial=gpio.LOW)
ser = serial.Serial(

    port='/dev/ttyS0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=1,
)

while 1:
	gpio.output(23,gpio.LOW)
	time.sleep(1)
	ser.write("AT+C001")


	x = ser.readline()
	print(x)


	gpio.output(23, gpio.HIGH)
	ser.write("yo")
	time.sleep(1)
	gpio.output(23,gpio.LOW)
	time.sleep(1)
	ser.write("AT+C002")
	x = ser.readline()
	print(x)
ser.close()
gpio.cleanup()

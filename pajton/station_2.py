import serial
import json
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.OUT, initial=gpio.HIGH)

initialize_payload = {
    "name": "Grzybiarnia",
    "delay_time": 20
}
if __name__ == '__main__':
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_NONE,
        timeout=2,
    )
    ser.flush()
    gpio.output(23, gpio.LOW)
    time.sleep(0.5)
    ser.write("AT+C001")
    time.sleep(0.1)
    gpio.output(23, gpio.HIGH)
    time.sleep(0.7)
    ser.write(json.dumps(initialize_payload)+ "\n")
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline()
                payload = json.loads(line)
                print(payload["time"])
                payload["delay_time"] = 20
                ser.write(json.dumps(payload) + "\n")
                time.sleep(19)
        except Exception as e:
            print(str(e))
            continue

import json
import requests
import serial
import time
import sys
import schedule
import RPi.GPIO as gpio
from safe_schedule import TaskScheduler
import threading
import os

SET_PIN = 23
RELAY_REFRESH_TIME = 8
STATION_REFRESH_TIME = 300
counter = 0
gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.OUT, initial=gpio.HIGH)
g = False
ser = serial.Serial(

    port='/dev/ttyS0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=2,
)

payload = {
    "username": ["pjury"],
    "password": ["maniak123"]
}


def connect():
    try:
        r = requests.post('http://127.0.0.1/api/token/', data=payload)
        jsondata = r.json()
        headers = {'Authorization': 'Bearer ' + jsondata['access']}
        return headers
    except Exception as e2:
        print("e2")
        print(str(e2))
        return


payloade = {
    "relays": [
        {
            "index": 0,
            "state": False,
        },
        {
            "index": 1,
            "state": False,
        },
        {
            "index": 2,
            "state": False,
        },
        {
            "index": 3,
            "state": False,
        },
        {
            "index": 4,
            "state": False,
        },
        {
            "index": 5,
            "state": False,
        },
        {
            "index": 6,
            "state": False,
        },
        {
            "index": 7,
            "state": False,
        },
    ],
    "name": "Grzybiarnia",
    "refresh_time": 120,
}


def get_data():
    try:
        rx = requests.post('http://127.0.0.1/api/token/', data=payload)
        jsondata = rx.json()
        headers = {'Authorization': 'Bearer ' + jsondata['access']}
        rx = requests.get('http://127.0.0.1/grzybiarnia/data-show/', headers=headers, timeout=20)
        dicti = rx.json()[0]
        payloade["refresh_time"] = dicti["refresh_time"]
        for c, relays in enumerate(dicti["relays"]):
            payloade["relays"][c]["state"] = relays["state"]
        print(payloade)

        return json.dumps(payloade)
    except Exception as e:
        print("e4")
        print(str(e))
        return


def get_data_for_station():
    try:
        rx = requests.get('http://127.0.0.1/sensor/data', headers=connect(), timeout=20)
        beka = rx.json()
        beka["delay_time"] = 60
        print(beka)
        return json.dumps(beka)
    except Exception as e1:
        print("e1")
        print(str(e1))
        return


def job():
    global counter
    gpio.output(23, gpio.LOW)
    time.sleep(0.5)
    ser.write("AT+C002")
    time.sleep(0.1)
    gpio.output(23, gpio.HIGH)
    time.sleep(0.7)
    ser.write(get_data())
    ser.reset_input_buffer()
    time.sleep(0.3)
    # x = ser.readline()
    # print(x)
    # payload3 = json.loads(x)
    # r = requests.post('http://127.0.0.1/data-add/', headers=connect(), json=payload3)
    # to wyzej to stacja 2 z relay stacji
    time.sleep(0.3)
    gpio.output(23, gpio.LOW)
    time.sleep(0.8)
    ser.write("AT+C001")
    time.sleep(0.3)
    gpio.output(23, gpio.HIGH)
    time.sleep(0.3)
    counter += 1
    print(counter)


scheduler = TaskScheduler()

schedule.every(8).seconds.do(job)


def runanother():
    os.system("sudo python3.7 /home/pi/Dev/djangostation/pajton/relay.py")


while 1:
    try:
        schedule.run_pending()
        x = ser.readline()
        payload2 = json.loads(x)
        ser.write(get_data_for_station() + '/')
        print(x)
        r = requests.post('http://127.0.0.1/data-add/', headers=connect(), json=payload2)
        print(r.text)
        if g is False:
            t = threading.Thread(target=runanother)
            t.start()
            g = True



    except Exception as e:
        print("e")
        print(str(e))
        continue

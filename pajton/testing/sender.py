import json
import requests
import serial
import time
import sys

ser = serial.Serial(

    port='/dev/ttyS0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=1,
)

PAYLOAD = {
    "username": ["pjury"],
    "password": ["maniak123"]
}

payload = {
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
    r = requests.post('http://192.168.1.16/api/token/', data=PAYLOAD)
    jsondata = r.json()
    headers = {'Authorization': 'Bearer ' + jsondata['access']}
    r = requests.get('http://192.168.1.16/grzybiarnia/data-show/', headers=headers, timeout=20)
    dicti = r.json()[0]
    payload["refresh_time"] = dicti["refresh_time"]
    for c, relays in enumerate(dicti["relays"]):
        payload["relays"][c]["state"] = relays["state"]
    print(payload)

    return payload


def get_data_for_station():
    r = requests.post('http://192.168.1.16/api/token/', data=PAYLOAD)
    jsondata = r.json()
    headers = {'Authorization': 'Bearer ' + jsondata['access']}
    r = requests.get('http://192.168.1.16/sensor/data', headers=headers, timeout=20)
    beka = r.json()
    beka["delay_time"] = 120
    print(beka)
    return beka


while 1:
    try:
        x = ser.readline()
        payload2 = json.dumps(get_data())
        ser.write(payload2)
        time.sleep(1)
    except Exception as e:
        print(str(e))
        continue

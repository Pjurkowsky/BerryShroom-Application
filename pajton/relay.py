import json
import time
from datetime import datetime, timedelta, date
import schedule
import requests
import os
import threading

'''
import serial
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=1,
)'''

PAYLOAD = {
    "username": ["pjury"],
    "password": ["maniak123"]
}

g = False 

def run_another():
    os.system("sudo /usr/local/bin/sakis3g connect")

def get_data():
    r = requests.post('http://127.0.0.1/api/token/', data=PAYLOAD)
    jsondata = r.json()
    headers = {'Authorization': 'Bearer ' + jsondata['access']}
    r = requests.get('http://127.0.0.1/grzybiarnia/data-show/', headers=headers, timeout=20)
    return r.json()[0]


data = get_data()


change = [data["relays"][i]["state"] for i in range(len(data["relays"]))]


class Relays:
    def __init__(self, index):
        self.id = index
        self.state = data["relays"][self.id]["state"]
        self.mode = data["relays"][self.id]["mode"]
        self.time_on = datetime.strptime(data["relays"][self.id]["time_on"], '%H:%M:%S').time()
        self.time_off = datetime.strptime(data["relays"][self.id]["time_off"], '%H:%M:%S').time()
        self.interval = data["relays"][self.id]["interval"].split("-")
        self.after = datetime.now()
        self.c = 0
        self.now = None
        schedule.every(int(self.interval[0])).minutes.do(self.on_every_x).tag(self.id)
        self.data = data

    def time_on_time_off(self):
        global change
        self.now = datetime.now().time()
        if self.time_on <= self.time_off:
            change[self.id] = self.time_on <= self.now <= self.time_off
        else:
            change[self.id] = self.time_on <= self.now or self.now <= self.time_off

    def on_every_x(self):
        global change
        change[self.id] = True

    def off_after_y(self):
        global change
        if change[self.id] is True and self.c is 0:
            self.after = datetime.now() + timedelta(minutes=int(self.interval[1]))
            self.c = 1
        if datetime.now() > self.after:
            change[self.id] = False
            self.c = 0

    def read_mode(self):
        if self.mode == 'time_on_time_off':
            self.time_on_time_off()
        elif self.mode == 'off_after_y':
            self.off_after_y()
        elif self.mode == 'on':
            change[self.id] = True
        else:
            change[self.id] = False

    def update(self, new_data):
        self.state = new_data["relays"][self.id]["state"]
        self.mode = new_data["relays"][self.id]["mode"]
        self.time_on = datetime.strptime(new_data["relays"][self.id]["time_on"], '%H:%M:%S').time()
        self.time_off = datetime.strptime(new_data["relays"][self.id]["time_off"], '%H:%M:%S').time()
        self.interval = new_data["relays"][self.id]["interval"].split("-")
        if self.data["relays"][self.id]["interval"].split("-") != self.interval:
            schedule.clear(self.id)
            schedule.every(int(self.interval[0])).minutes.do(self.on_every_x).tag(self.id)
            # print("hehe")
        self.data = new_data
        global data
        data = self.data

    def start(self, new_data):
        self.update(new_data)
        self.read_mode()


def put_data():
    global data
    r = requests.post('http://127.0.0.1/api/token/', data=PAYLOAD)
    jsondata = r.json()
    headers = {'Authorization': 'Bearer ' + jsondata['access']}
    r = requests.put('http://127.0.0.1/grzybiarnia/data-update/2', headers=headers, json=data)
    # print(r.text)


relays = [Relays(i) for i in range(len(data["relays"]))]

while True:
    try:
        schedule.run_pending()
        for i in range(len(data["relays"])):
            relays[i].start(get_data())
        for c, i in enumerate(change):
            data["relays"][c]["state"] = i
            # print([data["relays"][c]["index"], data["relays"][c]["state"]])
        put_data()
        # print(data["relays"][1]["mode"])
        time.sleep(0.05)
        if g is False:
            t = threading.Thread(target=run_another)
            t.start()
            g = True

    except Exception as e:
        print(str(e))
        continue

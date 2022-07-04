import glob
import time
import json
import requests
import threading
import os

DELAY_TIME = 60
BASE_DIR = '/sys/bus/w1/devices/'

PAYLOAD = {
    "username": ["pjury"],
    "password": ["maniak123"]
}

JSON_STRING = '''
   {
  "name": "Centralka",
  "delay_time": null,
  "index": 1,
  "sensors": [
    {
      "name": "CPU",
      "index": 0,
      "type": "temperature",

      "values": [
        {
          "value": 2
        }
      ]
    },
    {
      "name": "DS18B20",
      "index": 1,
      "type": "temperature",
      "values": [
        {
          "value": 1
        }
      ]
    }
  ]
}

'''
data = json.loads(JSON_STRING)
data["delay_time"] = DELAY_TIME
URL = "http://127.0.0.1:8000/"

def read_temp():
    device_file = []
    lines = []
    lines2 = []

    for i in glob.glob(BASE_DIR + '28*'):
        device_file.append(i + '/w1_slave')

    temp_string = []
    temp_c = []
    equals_pos = []
    for y in device_file:
        f = open(y, 'r')
        lines.append(f.readlines())
        lines2 = lines
        f.close()
    for x in range(len(device_file)):
        while lines2[x][0].strip()[-3:] != 'YES':
            time.sleep(0.2)
        equals_pos.append(lines[x][1].find('t='))
        if equals_pos[x] != -1:
            temp_string.append(lines[x][1][equals_pos[x] + 2:])
            temp_c.append(float(temp_string[x]) / 1000.0)
    return temp_c


def read_cpu_temp():
    result = 0.0
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
            if line.isdigit():
                result = float(line) / 1000
    return result


while True:

        # for counter, temperature in enumerate(read_temp()):
        #      data["sensors"][counter]["value"] = temperature
        data["sensors"][0]["values"][0]["value"] = read_cpu_temp()
        data["sensors"][1]["values"][0]["value"] = None
        for sensor in data["sensors"]:
            for value in sensor["values"]:
                r = requests.post(URL + 'api/value-create/' +
                                            str(data['index']) + '/' + str(sensor["index"]) + '/', value)
                print(r.text)

        time.sleep(DELAY_TIME)



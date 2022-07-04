#!/usr/bin/env python3
import requests
import subprocess
import time


stationIsRunning = False
sensorIsRunning = False

time.sleep(1)
while True:
    if not stationIsRunning:
        station = subprocess.Popen(
            'sudo -H -u pi python3 /home/pi/Dev/djangostation2/spts/station.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if not sensorIsRunning:
        sensor = subprocess.Popen(
            'sudo -H -u pi python3 /home/pi/Dev/djangostation2/spts/ds18b20.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stationIsRunning = station.poll() is None
    sensorIsRunning = sensor.poll() is None

    time.sleep(10)

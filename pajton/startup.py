import time
import logging
import threading
import os


def startprgm():
    print("Thread 1: starting ds18b20")
    time.sleep(1)
    os.system("sudo python3.7 /home/pi/Dev/djangostation/pajton/ds18b20.py")

t = threading.Thread(target=startprgm)
t.start()


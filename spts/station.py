#!/usr/bin/env python3
import json
import sys
import struct
import time
import traceback
import pigpio
import subprocess
from spts import *
from nrf24 import *
URL = "http://127.0.0.1:8000/"


if __name__ == "__main__":
    hostname = 'localhost'
    port = 8888
    address = '1SNSR'
    encoding = 'utf-8'

    # Connect to pigpiod
    p = subprocess.Popen(
        'sudo pigpiod', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    # PLEASE NOTE: PA level is set to MIN, because test sender/receivers are often close to each other, and then MIN works better.
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100,
                data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    # Listen on the address specified as parameter

    nrf.show_registers()

    # if everything went correct send log to server that it is working
    sendLog("DEBUG", "station.py is now running")
    try:
        while True:

            count = 0
            is_data_being_received = True
            data = ''
            data_json = ''

            while is_data_being_received:
                nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)
                while nrf.data_ready():

                    payload = nrf.get_payload()

                    if len(payload) == 32 and payload[0] == 0x01:
                        values = struct.unpack(">B31s", payload)
                        data += values[1].decode(encoding)

                    if len(payload) == 32 and payload[0] == 0x64:
                        values = struct.unpack(">B31s", payload)
                        data += values[1].decode(encoding)

                    if len(payload) == 32 and payload[0] == 0xC8:
                        values = struct.unpack(">B31s", payload)
                        data_json = json.loads(data.strip().strip('\x00'))
                        data = ''
                        is_data_being_received = False

                    count += 1

                time.sleep(0.1)
            station_name = data_json['name']

            delay_time = getDelayTimeFromServer(data_json['id'])
            nrf.open_writing_pipe(RF24_RX_ADDR.P1, address)
            payload2 = struct.pack(">BiB", 0x01, delay_time, 0xC8)
            nrf.send(payload2)
            try:
                nrf.wait_until_sent()
            except TimeoutError:
                print('Timeout waiting for transmission to complete.')
                continue
            print()
            print(f'Receive from {address} {station_name}')
            sendLog("DEBUG", f'Receive data from {address} {station_name}')
            sendPayloadToStation(data_json, 0)
            print(data_json)
    except:
        sendLog("ERROR", traceback.format_exc())
        nrf.power_down()
        pi.stop()

#!/usr/bin/env python3
import json
import time
import requests
import sys

URL = "http://192.168.8.184:8000/"


def sendLog(logger, message):
    payload = {
        "logger": logger,
        "message": message,
    }
    r = requests.post(URL + 'api-log/', payload)
    print(r.text)


def getDataFromServer():
    delay_times = []
    r = requests.get(URL + 'api/station/')
    stations = r.json()
    for station in stations:
        delay_times.append(station['delay_time'])
    return delay_times

# station_type = 0 -> Stacja ; station_type = 1 -> Grzybiarnia


def sendPayloadToStation(payload, station_type):
    if station_type == 0:
        request = requests.get(
            URL + 'api/station/' + str(payload['index']) + '/')
        if payload['index'] == request.json()['index']:  # indeksy stacji sie zgadzają
            r_sensorIndexes = [r_sensor['index']
                               for r_sensor in request.json()['sensors']]

            validIndexes = [(count, p_sensor['index'])
                            for count, p_sensor in enumerate(payload['sensors']) if p_sensor['index'] in r_sensorIndexes]  # zapisuje id i index w tuplu(id,index)

            for validIndex in validIndexes:
                if payload['sensors'][validIndex[0]]['index'] == validIndex[1]:
                    for value in payload['sensors'][validIndex[0]]["values"]:
                        r = requests.post(URL + 'api/value-create/' +
                                          str(payload['index']) + '/' + str(validIndex[1]) + '/', value)
                        print(r.text)
    elif station_type == 1:
        request = requests.get(
            URL + '/api-mushfarm/mushstation/' + str(payload['index']) + '/')
        if payload['index'] == request.json()['index']:  # indeksy stacji sie zgadzają

            r_relayIndexes = [r_relay['index']
                              for r_relay in request.json()['relays']]

            validIndexes = [(count, p_relay['index']) for count, p_relay in enumerate(
                payload['relays']) if p_relay['index'] in r_relayIndexes]

            for validIndex in validIndexes:
                if payload['relays'][validIndex[0]]['index'] == validIndex[1]:
                    r = requests.post(URL + 'api-mushfarm/relay-update/' +
                                      str(payload['index']) + '/' + str(payload['relays'][validIndex[0]]['index']) + '/', payload['relays'][validIndex[0]])
                    print(r.text)

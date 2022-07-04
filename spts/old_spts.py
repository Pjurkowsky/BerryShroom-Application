import json
import time
import requests

import sys


# import serial

# ser = serial.Serial(

#     port='/dev/ttyS0',
#     baudrate=9600,
#     bytesize=serial.EIGHTBITS,
#     stopbits=serial.STOPBITS_ONE,
#     parity=serial.PARITY_NONE,
#     timeout=2,
# )

URL = "http://192.168.8.184:8000/"


# with open('/home/pi/Dev/djangostation2/spts/config.json', 'r') as f:
#     config = json.load(f)


def sendLog(logger, message):
    payload = {
        "logger": logger,
        "message": message,
    }
    r = requests.post(URL + 'api-log/', payload)
    print(r.text)


# def getPayload():
#     with open('/home/pi/Dev/djangostation2/spts/data.json', 'r') as f:
#         payload2 = json.load(f)
#     return payload2
#     # return json.loads(ser.readline())


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

# funkcja do pobierania z serwera delay_tajmu


def getDataFromServer():
    delay_times = []

    r = requests.get(URL + 'api/station/')
    stations = r.json()
    for station in stations:
        delay_times.append(station['delay_time'])
    return delay_times


# def listen():
#     n = 0
#     end = 0
#     end1 = 0
#     isDataReceived = False
#     try:
#         while True:
#             try:
#                 start1 = time.time()
#                 if(start1 - end1 >= 5):
#                     payload = getPayload()
#                     end1 = time.time()

#                 if isDataReceived:
#                     isDataReceived = False
#                 if 'index' in payload:
#                     isDataReceived = True
#                     print()
#                     print("Data was received from " + payload['name'])
#                     print()
#                     # print(payload)
#                     print()
#                     print("Sending it to the server")
#                     if 'sensors' in payload:
#                         sendPayloadToStation(payload, 0)
#                         print("Data sent (sensors)")
#                     elif 'relays' in payload:
#                         sendPayloadToStation(payload, 1)
#                         print("Data sent (relays)")

#                     payload.pop('index')
#                 pass
#             except Exception as e:
#                 print(e)
#                 continue
#             start = time.time()
#             if start - end > 1 and not isDataReceived:
#                 end = start
#                 n = n % 3 + 1
#                 dots = n * '.' + (3-n) * ' '
#                 sys.stdout.write(
#                     '\rListening for payload(Press CTRL-C to kill loop)' + dots)
#                 sys.stdout.flush()
#                 if n >= 3:
#                     n = 0
#     except KeyboardInterrupt:
#         pass


# # ta funkcja powinna wysylac delay_tajm do odpowiednej stacji
# def send():
#     data = getDataFromServer()


# def printMenu():
#     print('[1] AutoStart:', config['settings']['auto_on'])
#     print('[2] Listen for payload')
#     print('[3] Exit')


# def menuInput():
#     try:
#         i = int(input('Enter your option: '))
#         return i
#     except ValueError:
#         print()
#         print('Please type an integer value')
#         return -1


# def menu():
#     printMenu()
#     if config['settings']['auto_on']:
#         option = 2
#     else:
#         option = menuInput()

#     while option != 0:
#         if option == 1:
#             input_var = input('Do you want to change AutoStart to ' +
#                               str(not config['settings']['auto_on']) + ' (y/N)')
#             if input_var in ['y', 'Y']:
#                 config['settings']['auto_on'] = not config['settings']['auto_on']
#                 with open('config.json', 'w') as f:
#                     json.dump(config, f)
#         elif option == 2:
#             print('Listening for payload(Press CTRL-C to kill loop)', end='\r')
#             listen()
#             print()
#         elif option == 3:
#             exit()

#         print()
#         printMenu()
#         option = menuInput()


# if __name__ == "__main__":
#     menu()

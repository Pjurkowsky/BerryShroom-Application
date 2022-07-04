import serial
import json

from datetime import datetime

initialize_payload = {
    "name": "WeatherStation",
    "delay_time": 10,
    "date": "",
    "new_day": False
}

if __name__ == '__main__':
    ser = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_NONE,
        timeout=2,
    )
    ser.flush()
    while True:
        try:
            now = datetime.now()
            if ser.in_waiting > 0:
                line = ser.readline()
                payload = json.loads(line)
                initialize_payload["date"] = now.strftime("%H:%M:%S")
                ser.write(json.dumps(initialize_payload) + "\n")
                print(payload)
            if now.strftime("%H:%M:%S") == "00:00:00":
                initialize_payload["new_day"] = True
            else:
                initialize_payload["new_day"] = False
            print(initialize_payload["new_day"])
        except Exception as e:
            print(str(e))
            continue

import json
import time
import random

with open('data.json', 'r') as f:
    payload = json.load(f)


def randomize_data():
    for sensor in payload['sensors']:
        sensor['values'].clear()
        sensor['values'].append({"value": round(random.uniform(20, 25), 2)})
        print(sensor['values'])
    with open('data.json', 'w') as f:
        json.dump(payload, f)


if __name__ == "__main__":
    while(True):
        randomize_data()
        time.sleep(10)

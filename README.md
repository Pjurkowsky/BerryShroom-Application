# BerryShroom-Application
This project is about gathering the data from the diffrent enviroments and controlling it if needed. I'm using it to gather the data from blueberry plantation and mushroom cultivation room.

### How its build
The whole project sits on raspberry pi, which is the main brain of everything here. It is hosting the server, receives data from stations, etc. It communicates with stations via NRF24 module which is 2.4Ghz transciver. Stations are build on top of arduino nano in which sensors are connected. There are few types of sensors like temperature, humidity, or voltage level of battery (for now).


### How it looks like
#### Dashboard
![image](https://user-images.githubusercontent.com/77162184/177606929-e6978f9b-b584-4aad-98f8-5f89be15eb1e.png)
#### Relay controls
![image](https://user-images.githubusercontent.com/77162184/177607893-765a3c93-3937-419b-a357-7bafa7a02817.png)
#### Sensor settings
![image](https://user-images.githubusercontent.com/77162184/177608070-030ec8db-1244-4ab5-bef4-09ff5dadb9d3.png)
#### Logs 
![image](https://user-images.githubusercontent.com/77162184/177608163-7fb89ab5-2f84-41ca-8628-9452b2a6014c.png)
#### Settings
![image](https://user-images.githubusercontent.com/77162184/177608238-8760dcd8-f99e-449d-8923-d113ab1ea0f0.png)

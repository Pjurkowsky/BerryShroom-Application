# 1 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino"
# 2 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 3 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 4 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 5 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 6 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 7 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 8 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 9 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino" 2
# 34 "c:\\Users\\mruto\\Desktop\\BerryShroom\\arduinko\\nrf24\\nrf24.ino"
RF24 radio(7 /* CE PIN for RF24 module.*/, 8 /* CSN PIN for RF24 module.*/); // using pin 7 for the CE pin, and pin 8 for the CSN pin
OneWire oneWire(2);
DallasTemperature thermometers(&oneWire);
DeviceAddress thermometer;
DHT dht(3, 22 /**< DHT TYPE 22 */);

int delay_time = 300;

byte rf24_tx[6] = "1SNSR";
byte rf24_rx[6] = "1SNST";

char result[400];
byte payload[32];

void serialize_and_send();
void receive_and_deserialize();
void sleep();

void nrf24_setup()
{
    radio.begin();
    radio.enableDynamicPayloads();
    radio.setAutoAck(true);
    radio.setPALevel(RF24_PA_MIN /* RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX*/);
    radio.setRetries(5 /* Delay bewteen retries, 1..15.  Multiples of 250µs.*/, 15 /* Number of retries, 1..15.*/);
    radio.setDataRate(RF24_250KBPS /* RF24_2MBPS, RF24_1MBPS, RF24_250KBPS*/);
    radio.setChannel(100 /* 0 ... 125*/);
    radio.setCRCLength(RF24_CRC_16 /* RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit*/);
    radio.setPayloadSize(32 /* Max. 32 bytes.*/);
    radio.openWritingPipe(rf24_tx);
    radio.openReadingPipe(0, rf24_rx);
    radio.stopListening();
}

void setup()
{
    Serial.begin(9600);
    printf_begin();

    pinMode(7, 0x1);
    pinMode(6, 0x0);
    pinMode(4, 0x1);

    thermometers.begin();
    dht.begin();

    nrf24_setup();

    if (!thermometers.getAddress(thermometer, 0))
        Serial.println("Unable to find address for Device 0");
    thermometers.setResolution(thermometer, 12);
}

void loop()
{
    serialize_and_send();
    sleep(delay_time);
    receive_and_deserialize();
}

void serialize_data()
{
    StaticJsonDocument<400> doc;
    doc["name"] = "Grzybiarnia";
    doc["delay_time"] = delay_time;
    doc["index"] = 0;
    JsonArray sensors = doc.createNestedArray("sensors");

    thermometers.requestTemperatures();

    JsonObject Sensor_0 = sensors.createNestedObject();
    Sensor_0["name"] = "DS18B20";
    Sensor_0["index"] = 0;
    Sensor_0["type"] = "temperature";
    Sensor_0["values"][0]["value"] = thermometers.getTempC(thermometer);

    JsonObject Sensor_1 = sensors.createNestedObject();
    Sensor_1["name"] = "DHT22";
    Sensor_1["index"] = 1;
    Sensor_1["type"] = "temperature";
    Sensor_1["values"][0]["value"] = dht.readTemperature();

    JsonObject Sensor_2 = sensors.createNestedObject();
    Sensor_2["name"] = "DHT22";
    Sensor_2["index"] = 2;
    Sensor_2["type"] = "humidity";
    Sensor_2["values"][0]["value"] = dht.readHumidity();

    JsonObject Sensor_3 = sensors.createNestedObject();
    Sensor_3["name"] = "battery";
    Sensor_3["index"] = 3;
    Sensor_3["type"] = "voltage";
    Sensor_3["values"][0]["value"] = analogRead(A0) * (5 / 1024.0);
    serializeJson(doc, result);
    Serial.println(result);
}

void serialize_and_send()
{
    int offset = 0;
    int counter = 0;
    int payload_number = 0;
    const byte start_protocol = 0X01;
    const byte ongoing_protocol = 0X64;
    const byte end_protocol = 0XC8;

    serialize_data(); // zmienna result dostaje dane

    payload_number = ceil((float)sizeof(result) / (float)32 /* Max. 32 bytes.*/); // ile jest payloadow

    memcpy(payload, (byte *)&start_protocol, sizeof(start_protocol));
    offset = 32 /* Max. 32 bytes.*/ - sizeof(start_protocol);
    memcpy(payload + sizeof(start_protocol), (byte *)result, offset);

    radio.stopListening();
    do
    {
        Serial.println("essa");
        Serial.println(radio.write(payload, sizeof(payload)));
        // if (radio.write(payload, sizeof(payload)))
        // {
        //     Serial.println(F("Transmission successful!"));
        //     Serial.print("Protocol:");
        //     Serial.println((int)payload[0]);
        //     // Serial.println(String((char *)payload));
        // }

        // else
        // Serial.println(F("Transmission failed or timed out"));

        counter++;

        if (counter > 0 && counter < payload_number - 1)
        {
            strncpy((char *)payload, (char *)&ongoing_protocol, sizeof(ongoing_protocol));
            strncpy((char *)payload + sizeof(ongoing_protocol), result + (offset * counter), offset);
        }
        else if (counter == payload_number - 1)
        {
            strncpy((char *)payload, (char *)&end_protocol, sizeof(end_protocol));
            strncpy((char *)payload + sizeof(end_protocol), result + (offset * counter), offset);
        }
    } while (counter < payload_number);
}

void receive_and_deserialize()
{
    const byte start_protocol = 0X01;
    const byte ongoing_protocol = 0X64;
    const byte end_protocol = 0XC8;
    int counter = 0;
    StaticJsonDocument<64> doc;
    radio.startListening();
    while (radio.available())
    {
        radio.read(&payload, sizeof(payload));
        if (payload[0] == start_protocol)
            counter++;
    }
    DeserializationError error = deserializeJson(doc, payload);
    if (doc["name"] == "Stacja 1")
        delay_time = doc["delay_time"];
}

void sleep(int timeout)
{
    digitalWrite(4, 0x0);
    timeout = timeout / 10;
    for (int i = 0; i < timeout; i++)
    {
        LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
        LowPower.powerDown(SLEEP_2S, ADC_OFF, BOD_OFF);
    }
}

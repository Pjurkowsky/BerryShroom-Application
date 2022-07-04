#include <SPI.h>
#include <ArduinoJson.h>

#include "printf.h"
#include "RF24.h"

#define trigPin 7
#define echoPin 6
#define ONE_WIRE_BUS 2
#define TEMPERATURE_PRECISION 12
#define DHTPIN 3
#define DHTTYPE DHT22 // Type of DHT sensor: DHT11, DHT12, DHT21, DHT22 (AM2302), AM2301
#define NRF24PIN 4
#define PIN_RF24_CSN 8 // CSN PIN for RF24 module.
#define PIN_RF24_CE 7  // CE PIN for RF24 module.

#define NRF24_CHANNEL 100            // 0 ... 125
#define NRF24_CRC_LENGTH RF24_CRC_16 // RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit
#define NRF24_DATA_RATE RF24_250KBPS // RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
#define NRF24_DYNAMIC_PAYLOAD 1
#define NRF24_PAYLOAD_SIZE 32      // Max. 32 bytes.
#define NRF24_PA_LEVEL RF24_PA_MIN // RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
#define NRF24_RETRY_DELAY 5        // Delay bewteen retries, 1..15.  Multiples of 250µs.
#define NRF24_RETRY_COUNT 15       // Number of retries, 1..15.

#define START_PROTOCOL 0X01
#define ONGOING_PROTOCOL 0X64
#define END_PROTOCOL 0XC8

RF24 radio(PIN_RF24_CE, PIN_RF24_CSN); // using pin 7 for the CE pin, and pin 8 for the CSN pin

int numberOfDevices;
int delay_time = 60;

byte rf24_tx[6] = "1SNSR";

char result[200];
byte payload[32];

void serialize_and_send();
void receive_and_deserialize();
void sleep();

void nrf24_setup()
{
  radio.begin();
  radio.enableDynamicPayloads();
  radio.setAutoAck(true);
  radio.setPALevel(NRF24_PA_LEVEL);
  radio.setRetries(NRF24_RETRY_DELAY, NRF24_RETRY_COUNT);
  radio.setDataRate(NRF24_DATA_RATE);
  radio.setChannel(NRF24_CHANNEL);
  radio.setCRCLength(NRF24_CRC_LENGTH);
  radio.setPayloadSize(NRF24_PAYLOAD_SIZE);
  radio.openWritingPipe(rf24_tx);
  radio.stopListening();
}

void setup()
{
  Serial.begin(9600);
  printf_begin();

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(NRF24PIN, OUTPUT);

  nrf24_setup();
}

void loop()
{
  Serial.println("essa");
  radio.stopListening();
  serialize_and_send();
  radio.startListening();

  delay(5000);
}

void serialize_data()
{
  StaticJsonDocument<400> doc;
  doc["name"] = "Grzybiarnia";
  doc["delay_time"] = delay_time;
  JsonArray sensors = doc.createNestedArray("sensors");

  JsonObject Sensor_0 = sensors.createNestedObject();
  Sensor_0["name"] = "DS18B20";
  Sensor_0["index"] = 0;
  Sensor_0["type"] = "temperature";
  Sensor_0["values"][0]["value"] = 12;

  JsonObject Sensor_1 = sensors.createNestedObject();
  Sensor_1["name"] = "DHT22";
  Sensor_1["index"] = 1;
  Sensor_1["type"] = "temperature";
  Sensor_1["values"][0]["value"] = 12;

  serializeJson(doc, result);
}

void serialize_and_send()
{
  int offset = 0;
  int counter = 0;
  int payload_number = 0;
  const byte start_protocol = START_PROTOCOL;
  const byte ongoing_protocol = ONGOING_PROTOCOL;
  const byte end_protocol = END_PROTOCOL;

  float temperature = 1;
  float humidity = 2;

  memcpy(payload + offset, (byte *)(&start_protocol), sizeof(start_protocol));
  offset += sizeof(start_protocol);
  memcpy(payload + offset, (byte *)(&temperature), sizeof(temperature));
  offset += sizeof(temperature);
  memcpy(payload + offset, (byte *)(&humidity), sizeof(humidity));
  offset += sizeof(humidity);

  if (radio.write(payload, offset))
  {
    Serial.print("Payload sent successfully. Retries=");
    Serial.println(radio.getARC());
  }
  else
  {
    Serial.print("Failed to send payload. Retries=");
    Serial.println(radio.getARC());
  }
}

// void receive_and_deserialize()
//{
//   radio.startListening();
//   uint8_t pipe;
//   if (radio.available(&pipe))
//   {
//     StaticJsonDocument<64> doc;
//     String payload;
//
//     radio.read(&payload, sizeof(doc));
//     Serial.print(pipe);
//     Serial.print(F(": "));
//     Serial.println(payload);
//
//     DeserializationError error = deserializeJson(doc, payload);
//     if (doc["name"] == "Stacja 1")
//       delay_time = doc["delay_time"];
//   }
// }

// void sleep(int timeout)
// {
//   digitalWrite(NRF24PIN, LOW);
//   timeout = timeout / 10;
//   for (int i = 0; i < timeout; i++)
//   {
//     LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
//     LowPower.powerDown(SLEEP_2S, ADC_OFF, BOD_OFF);
//   }
// }
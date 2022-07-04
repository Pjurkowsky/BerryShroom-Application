# 1 "c:\\Users\\mruto\\Desktop\\arduinko\\arduino_nano_dummy_mega\\arduino_nano_dummy_mega.ino"

// RF24, version 1.3.9, by TMRh20
# 4 "c:\\Users\\mruto\\Desktop\\arduinko\\arduino_nano_dummy_mega\\arduino_nano_dummy_mega.ino" 2
# 5 "c:\\Users\\mruto\\Desktop\\arduinko\\arduino_nano_dummy_mega\\arduino_nano_dummy_mega.ino" 2
# 21 "c:\\Users\\mruto\\Desktop\\arduinko\\arduino_nano_dummy_mega\\arduino_nano_dummy_mega.ino"
                                              // Python 1: "<Bff"


                                              // DHT11, DHT12, DHT21, DHT22 (AM2302), AM2301

// Cretate NRF24L01 radio.
RF24 radio(7 /* CE PIN for RF24 module.*/, 8 /* CSN PIN for RF24 module.*/);


byte rf24_tx[6] = "1SNSR"; // Address used when transmitting data.
byte payload[32]; // Payload bytes. Used both for transmitting and receiving

unsigned long last_reading; // Milliseconds since last measurement was read.
unsigned long ms_between_reads = 1000;

void setup() {

  // Initialize serial connection.
  Serial.begin(115200);
  printf_begin();
  delay(100);

  // Show that program is starting.
  Serial.println("\n\nNRF24L01 Arduino Simple Sender.");

  // Configure the NRF24 tranceiver.
 // Serial.println("Configure NRF24 ...");
  nrf24_setup();

  // Show debug information for NRF24 tranceiver.
  radio.printDetails();



  // Take the current timestamp. This means that the next (first) measurement will be read and
  // transmitted in "ms_between_reads" milliseconds.
  last_reading = 0;
}

void loop() {

  if (millis() - last_reading > ms_between_reads) {
    // Read sensor values every "ms_between_read" milliseconds.



    // Stop listening on the radio (we can't both listen and send).
    radio.stopListening();

    // Send the data ...
    send_reading(0x01 /* 0x01 (byte), temperature (float), humidity (float)*/, 2, 3);

    // Start listening again.
    radio.startListening();

    // Register that we have read the temperature and humidity.
    last_reading = millis();
  }
}

void send_reading(byte protocol, float temperature, float humidity)
{
  int offset = 0;
  //Serial.println("Preparing payload.");
  memcpy(payload + offset, (byte *)(&protocol), sizeof(protocol)); offset += sizeof(protocol);
  memcpy(payload + offset, (byte *)(&temperature), sizeof(temperature)); offset += sizeof(temperature);
  memcpy(payload + offset, (byte *)(&humidity), sizeof(humidity)); offset += sizeof(humidity);
 // Serial.print("Bytes packed: "); Serial.println(offset);

  // if (radio.write(payload, offset)) {
  //   Serial.print("Payload sent successfully. Retries="); Serial.println(radio.getARC());
  // }
  // else {
  //   Serial.print("Failed to send payload. Retries="); Serial.println(radio.getARC());
  // }   
}

void nrf24_setup()
{
  radio.begin();
  radio.enableDynamicPayloads();
  radio.setAutoAck(true);
  radio.setPALevel(RF24_PA_MIN /* RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX    */);
  radio.setRetries(5 /* Delay bewteen retries, 1..15.  Multiples of 250µs.*/, 15 /* Number of retries, 1..15.*/);
  radio.setDataRate(RF24_250KBPS /* RF24_2MBPS, RF24_1MBPS, RF24_250KBPS*/);
  radio.setChannel(100 /* 0 ... 125*/);
  radio.setCRCLength(RF24_CRC_16 /* RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16 for 16-bit*/);
  radio.setPayloadSize(32 /* Max. 32 bytes.*/);
  radio.openWritingPipe(rf24_tx);
  radio.stopListening();
}

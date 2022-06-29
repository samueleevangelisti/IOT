#ifndef GLOBALS_H
#define GLOBALS_H

int PIN_DHT11 = 0;

int PIN_MQ2_AO = 34;
int PIN_MQ2_DO = 35;

int SAMPLE_FREQUENCY = 2000; // frequenza di campionamento. DHT11 sampling rate is 1HZ.
int MIN_GAS_VALUE = 200; // valore minimo del gas
int MAX_GAS_VALUE = 10000; // valore massimo del gas
int COMMUNICATION_PROTOCOL = 0; // protocollo di comunicazione, 0: MQTT, 1: COAP, 2: HTTP

int wifi_rssi; // RSSI rilevato

float dht11_temperature; // temperatura rilevata
float dht11_humidity; // umidità rilevata

int mq2_gas_ppm; // gas ppm
int mq2_aqi; // air quality index

// dati in formato append
String get_data_string() {
  return String(ESP32_ID) + String("|") + String(ESP32_LATITUDE, 6) + String("|") + String(ESP32_LONGITUDE, 6) + String("|") + String(wifi_rssi) + String("|") + String(dht11_temperature) + String("|") + String(dht11_humidity) + String("|") + String(mq2_gas_ppm) + String("|") + String(mq2_aqi);
}

#endif

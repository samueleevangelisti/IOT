#ifndef GLOBALS_H
#define GLOBALS_H

#define PIN_DHT11 0

#define PIN_MQ2_AO 34
#define PIN_MQ2_DO 35

int SAMPLE_FREQUENCY = 2000; // frequenza di campionamento. DHT11 sampling rate is 1HZ.
int MIN_GAS_VALUE = 200; // valore minimo del gas
int MAX_GAS_VALUE = 10000; // valore massimo del gas
int communication_protocol = 0; // protocollo di comunicazione, 0: MQTT, 1: HTTP

int wifi_rssi; // RSSI rilevato

float dht11_temperature; // temperatura rilevata
float dht11_humidity; // umidità rilevata

int mq2_gas_ppm; // gas ppm
int mq2_aqi; // air quality index

#endif

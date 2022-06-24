#ifndef GLOBALS_H
#define GLOBALS_H

// pin per DHT11
#define PIN_DHT11 0

// pin per MQ2
#define PIN_MQ2_AO 34
#define PIN_MQ2_DO 35

// configurazioni globali
char* ESP32_ID = "ESP32"; // id del dispositivo
int SAMPLE_FREQUENCY = 2000; // frequenza di campionamento. DHT11 sampling rate is 1HZ.

int wifi_rssi; // RSSI rilevato

float dht11_temperature; // temperatura rilevata
float dht11_humidity; // umidità rilevata

int mq2_gas; // gas rilevato
int mq2_gas_ppm; // gas ppm
boolean mq2_isGas; // allarme per il gas
String mq2_isGas_string; // stringa di allarme per il gas

#endif

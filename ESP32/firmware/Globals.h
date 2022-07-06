#ifndef GLOBALS_H
#define GLOBALS_H

int PIN_DHT11 = 0;

int PIN_MQ2_AO = 34;
int PIN_MQ2_DO = 35;

int SAMPLE_FREQUENCY = 2000; // frequenza di campionamento. DHT11 sampling rate is 1HZ.
int MIN_GAS_VALUE = 200; // valore minimo del gas
int MAX_GAS_VALUE = 10000; // valore massimo del gas
int COMMUNICATION_PROTOCOL = 0; // protocollo di comunicazione, 0: MQTT, 1: COAP, 2: HTTP

extern char MQTT_SERVER[];
char MQTT_USER[20] = "IoT"; // user per mqtt
char MQTT_PASSWORD[20] = "IoT"; // password per mqtt
char MQTT_TOPIC[20] = "sensor"; // topic per l'invio dei dati

extern IPAddress COAP_SERVER;
char COAP_URL[20] = "sensor"; // url per l'identificazione dei dati

char HTTP_SEND_URL[50]; // url per l'invio dei dati

int wifi_rssi; // RSSI rilevato
int wifi_packet_sent = 0; // pacchetti inviati dall'ultima ricezione corretta
int wifi_packet_timestamp_start = 0; // timestamp di invio pacchett
int wifi_packet_delay = 0; // delay tra invio da ESP32 e ricezione nel proxy del pacchetto

float dht11_temperature; // temperatura rilevata
float dht11_humidity; // umidità rilevata

int mq2_gas_ppm; // gas ppm
int mq2_aqi; // air quality index

// dati in formato append
String get_data_string() {
  return String(ESP32_ID) + String("|") + String(ESP32_LATITUDE, 6) + String("|") + String(ESP32_LONGITUDE, 6) + String("|") + String(wifi_rssi) + String("|") + String(wifi_packet_sent) + String("|") + String(wifi_packet_delay) + String("|") + String(dht11_temperature) + String("|") + String(dht11_humidity) + String("|") + String(mq2_gas_ppm) + String("|") + String(mq2_aqi);
}

// dati in formato json serializzato
String get_dashboard_json() {
  return String("{")
    + String("\"PIN_DHT11\":") + String(PIN_DHT11) + String(",")
    + String("\"PIN_MQ2_AO\":") + String(PIN_MQ2_AO) + String(",")
    + String("\"PIN_MQ2_DO\":") + String(PIN_MQ2_DO) + String(",")
    + String("\"ESP32_ID\":\"") + String(ESP32_ID) + String("\",")
    + String("\"ESP32_LATITUDE\":") + String(ESP32_LATITUDE, 6) + String(",")
    + String("\"ESP32_LONGITUDE\":") + String(ESP32_LONGITUDE, 6) + String(",")
    + String("\"SAMPLE_FREQUENCY\":") + String(SAMPLE_FREQUENCY) + String(",")
    + String("\"MIN_GAS_VALUE\":") + String(MIN_GAS_VALUE) + String(",")
    + String("\"MAX_GAS_VALUE\":") + String(MAX_GAS_VALUE) + String(",")
    + String("\"COMMUNICATION_PROTOCOL\":") + String(COMMUNICATION_PROTOCOL) + String(",")
    + String("\"MQTT_SERVER\":\"") + String(MQTT_SERVER) + String("\",")
    + String("\"MQTT_USER\":\"") + String(MQTT_USER) + String("\",")
    + String("\"MQTT_PASSWORD\":\"") + String(MQTT_PASSWORD) + String("\",")
    + String("\"MQTT_TOPIC\":\"") + String(MQTT_TOPIC) + String("\",")
    + String("\"COAP_SERVER\":\"") + COAP_SERVER.toString() + String("\",")
    + String("\"COAP_URL\":\"") + String(COAP_URL) + String("\",")
    + String("\"HTTP_SEND_URL\":\"") + String(HTTP_SEND_URL) + String("\"")
  + String("}");
}

#endif

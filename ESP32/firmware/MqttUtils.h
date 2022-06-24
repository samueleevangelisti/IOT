#ifndef MQTTUTILS_H
#define MQTTUTILS_H

#include <PubSubClient.h>

#include "MqttAuth.h"

char* MQTT_USER = "IoT"; // user per mqtt
char* MQTT_PASSWORD = "IoT"; // password per mqtt
char* TOPIC_RSSI = "sensor/rssi"; // topic della temperatura
char* TOPIC_TEMPERATURE = "sensor/temperature"; // topic della temperatura
char* TOPIC_HUMIDITY = "sensor/humidity"; // topic dell'umidità
char* TOPIC_GAS = "sensor/gas"; // topic della temperatura
PubSubClient mqtt;
boolean mqtt_connected;
boolean mqtt_publish_result;

// inizializzazione connessione al broker MQTT
void mqtt_init() {
  Serial.println("MQTT -> initialization");
  mqtt.setClient(wifi_client);
  mqtt.setServer(MQTT_SERVER, 1883);
  mqtt.setBufferSize(400);
}

// connessione al broker MQTT
void mqtt_connect() {
  Serial.println("MQTT -> connection");
  mqtt_connected = mqtt.connect(ESP32_ID, MQTT_USER, MQTT_PASSWORD);
  if(mqtt_connected) {
    Serial.println("MQTT -> connected");
  } else {
    Serial.println("MQTT -> [ERROR] unable to connect");
  }
}

// core per le funzioni di pubblicazione
void mqtt_publish_core(char* topic, const char* payload) {
  Serial.print("MQTT -> ");
  mqtt_publish_result = mqtt.publish(topic, payload);
  mqtt.loop();
  if(mqtt_publish_result) {
    Serial.print("[OK] ");
  } else {
    Serial.print("[ERROR] ");
  }
  Serial.println(topic);
}

// pubblicazione dei dati sul broket MQTT
void mqtt_publish() {
  mqtt_connected = mqtt.connected();
  if(!mqtt_connected) {
    mqtt_connect();
  }
  if(mqtt_connected) {
    mqtt_publish_core(TOPIC_RSSI, String(wifi_rssi).c_str());
    mqtt_publish_core(TOPIC_TEMPERATURE, String(dht11_temperature).c_str());
    mqtt_publish_core(TOPIC_HUMIDITY, String(dht11_humidity).c_str());
    mqtt_publish_core(TOPIC_GAS, String(mq2_gas_ppm).c_str());
  } else {
    Serial.println("MQTT -> [ERROR] unable to send data");
  }
}

#endif

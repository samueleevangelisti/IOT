#ifndef MQTTUTILS_H
#define MQTTUTILS_H

#include "MqttAuth.h"

char* MQTT_USER = "IoT"; // user per mqtt
char* MQTT_PASSWORD = "IoT"; // password per mqtt
char* MQTT_TOPIC = "sensor"; // topic per l'invio dei dati
PubSubClient mqtt;
boolean mqtt_connected;
boolean mqtt_publish_result;

// inizializzazione connessione al broker MQTT
void mqtt_init() {
  Serial.println("MQTT  -> [WAIT] initialization");
  mqtt.setClient(wifi_client);
  mqtt.setServer(MQTT_SERVER, 1883);
  mqtt.setBufferSize(400);
  Serial.println("MQTT  -> [OK  ] initialization");
}

// connessione al broker MQTT
void mqtt_connect() {
  Serial.println("MQTT  -> [WAIT] connection");
  mqtt_connected = mqtt.connect(ESP32_ID, MQTT_USER, MQTT_PASSWORD);
  if(mqtt_connected) {
    Serial.println("MQTT  -> [OK  ] connected");
  } else {
    Serial.println("MQTT  -> [ERR ] unable to connect");
  }
}

// pubblicazione dei dati sul broket MQTT
void mqtt_publish() {
  mqtt_connected = mqtt.connected();
  if(!mqtt_connected) {
    mqtt_connect();
  }
  if(mqtt_connected) {
    String json = String("{")
      + String("\"measurement\":\"sensor\",")
      + String("\"tags\":{")
        + String("\"id\":\"") + String(ESP32_ID) + String("\",")
        + String("\"latitude\":") + String(ESP32_LATITUDE, 6) + String(",")
        + String("\"longitude\":") + String(ESP32_LONGITUDE, 6)
      + String("},")
      + String("\"fields\":{")
        + String("\"rssi\":") + String(wifi_rssi) + String(",")
        + String("\"temperature\":") + String(dht11_temperature) + String(",")
        + String("\"humidity\":") + String(dht11_humidity) + String(",")
        + String("\"gas\":") + String(mq2_gas_ppm) + String(",")
        + String("\"aqi\":") + String(mq2_aqi)
      + String("}")
    + String("}");
    mqtt_publish_result = mqtt.publish(MQTT_TOPIC, json.c_str());
    mqtt.loop();
    if(mqtt_publish_result) {
      Serial.println("MQTT  -> [OK  ] data sent to broker");
    } else {
      Serial.println("MQTT  -> [ERR ] unable to send data");
    }
  }
}

#endif

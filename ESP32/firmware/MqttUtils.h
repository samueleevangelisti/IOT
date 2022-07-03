#ifndef MQTTUTILS_H
#define MQTTUTILS_H

#include "MqttAuth.h"

PubSubClient mqtt;
boolean mqtt_connected;
boolean mqtt_publish_result;

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

// inizializzazione connessione al broker MQTT
void mqtt_init() {
  Serial.println("MQTT  -> [WAIT] initialization");
  mqtt.setClient(wifi_client);
  mqtt.setServer(MQTT_SERVER, 1883);
  mqtt.setBufferSize(400);
  Serial.println("MQTT  -> [OK  ] initialization");
  mqtt_connect();
}

// pubblicazione dei dati sul broket MQTT
void mqtt_publish() {
  mqtt_connected = mqtt.connected();
  if(!mqtt_connected) {
    mqtt_connect();
  }
  if(mqtt_connected) {
    mqtt_publish_result = mqtt.publish(MQTT_TOPIC, get_data_string().c_str());
    if(mqtt_publish_result) {
      Serial.println("MQTT  -> [OK  ] data sent to broker");
    } else {
      Serial.println("MQTT  -> [ERR ] unable to send data");
    }
  }
}

#endif

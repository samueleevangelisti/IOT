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
  wifi_packet_sent++;
  mqtt_connected = mqtt.connected();
  if(!mqtt_connected) {
    mqtt_connect();
  }
  if(mqtt_connected) {
    wifi_packet_timestamp_start = millis();
    mqtt_publish_result = mqtt.publish(MQTT_TOPIC, get_data_string().c_str());
    if(mqtt_publish_result) {
      wifi_packet_delay = millis() - wifi_packet_timestamp_start;
      Serial.println("MQTT  -> [OK  ] data sent to broker");
      wifi_packet_sent = 0;
    } else {
      Serial.println("MQTT  -> [ERR ] unable to send data");
    }
  } else {
    wifi_packet_timestamp_start = 0;
    wifi_packet_delay = 0;
  }
}

#endif

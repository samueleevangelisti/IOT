#ifndef DASHBOARD_H
#define DASHBOARD_H

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
    + String("\"COAP_URL\":\"") + String(COAP_URL) + String("\"")
  + String("}");
}

#endif

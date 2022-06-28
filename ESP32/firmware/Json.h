#ifndef JSON_H
#define JSON_H

StaticJsonDocument<200> json_document;
DeserializationError json_deserialization_error;

// deserializzazione di un json
void json_deserialize(String json_string) {
  json_deserialization_error = deserializeJson(json_document, json_string);
}

// dati in formato json serializzato
String json_get_data_json_string() {
  return String("{")
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
}

#endif

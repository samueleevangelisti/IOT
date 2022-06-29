#ifndef JSON_H
#define JSON_H

StaticJsonDocument<200> json_document;
DeserializationError json_deserialization_error;

// deserializzazione di un json
void json_deserialize(String json_string) {
  json_deserialization_error = deserializeJson(json_document, json_string);
}

#endif

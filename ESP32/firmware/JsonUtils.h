#ifndef JSONUTILS_H
#define JSONUTILS_H

StaticJsonDocument<1000> json_document;
DeserializationError json_deserialization_error;

// deserializzazione di un json
void json_deserialize(String json_string) {
  json_deserialization_error = deserializeJson(json_document, json_string);
}

#endif

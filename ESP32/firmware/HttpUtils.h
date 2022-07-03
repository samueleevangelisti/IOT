#ifndef HTTPUTILS_H
#define HTTPUTILS_H

WebServer http_web_server(80);
HTTPClient http_client;
int http_response_code;

// risposta alla ricerca dei dispositivi iot
void http_handle_iot_find() {
  Serial.println("HTTP  -> [LOG ] iot find request");
  http_web_server.send(200, "application/json", String("{")
    + String("\"success\":true,")
    + String("\"ip\":\"") + WiFi.localIP().toString() + String("\",")
    + String("\"port\":80")
  + String("}"));
}

// gestione richiesta dei dati
void http_handle_dashboard() {
  switch(http_web_server.method()) {
    case HTTP_GET:
      Serial.println("HTTP  -> [LOG ] dashboard  request");
      http_web_server.send(200, "application/json", String("{")
        + String("\"success\":true,")
        + String("\"data\":") + get_dashboard_json()
      + String("}"));
      break;
    case HTTP_POST:
      json_deserialize(http_web_server.arg(0));
      if(json_deserialization_error) {
        Serial.println("JSON  -> [ERR ] deserialization");
        http_web_server.send(200, "application/json", String("{")
          + String("\"success\":false")
        + String("}"));
      } else {
        strcpy(ESP32_ID, (const char*) json_document["ESP32_ID"]);
        strcpy(MQTT_SERVER, (const char*) json_document["MQTT_SERVER"]);
        strcpy(MQTT_USER, (const char*) json_document["MQTT_USER"]);
        strcpy(MQTT_PASSWORD, (const char*) json_document["MQTT_PASSWORD"]);
        strcpy(MQTT_TOPIC, (const char*) json_document["MQTT_TOPIC"]);
        COAP_SERVER.fromString(String((const char*) json_document["COAP_SERVER"]));
        strcpy(COAP_URL, (const char*) json_document["COAP_URL"]);
        strcpy(HTTP_SEND_URL, (const char*) json_document["HTTP_SEND_URL"]);
        Serial.println("HTTP  -> [LOG ] new subscribe url -> " + String(HTTP_SEND_URL));
        http_web_server.send(200, "application/json", String("{")
          + String("\"success\":true")
        + String("}"));
      }
      break;
  }
}

void http_init() {
  Serial.println("HTTP  -> [WAIT] initialization");
  http_web_server.on("/iotfind", http_handle_iot_find);
  http_web_server.on("/dashboard", http_handle_dashboard);
  http_web_server.begin();
  Serial.println("HTTP  -> [OK  ] initialization");
}

// gestione delle chiamate da evadere
void http_loop() {
  http_web_server.handleClient();
}

// invio dei dati
void http_send() {
  http_client.begin(HTTP_SEND_URL);
  http_client.addHeader("Content-type", "application/json");
  http_response_code = http_client.POST(String("{\"data\":\"") + get_data_string() + String("\"}"));
  if(http_response_code > 0) {
    Serial.println("HTTP  -> [OK  ] data sent to server");
  } else {
    Serial.println("HTTP  -> [ERR ] unable to send data");
  }
  http_client.end();
}

#endif

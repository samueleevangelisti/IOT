#ifndef HTTPUTILS_H
#define HTTPUTILS_H

#include "Dashboard.h"

WebServer http_web_server(80);
HTTPClient http_client;
String http_send_url;
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
      http_web_server.send(200, "application/json", get_dashboard_json());
      break;
    case HTTP_POST:
      break;
  }
}

// gestione della sottoscrizione dell'observer
void http_handle_subscribe() {
  json_deserialize(http_web_server.arg(0));
  if(json_deserialization_error) {
    Serial.println("JSON  -> [ERR ] deserialization");
    http_web_server.send(200, "application/json", String("{")
      + String("\"success\":false")
    + String("}"));
  } else {
    http_send_url = String((const char *) json_document["url"]);
    Serial.println("HTTP  -> [LOG ] new send url -> " + String(http_send_url));
    http_web_server.send(200, "application/json", String("{")
      + String("\"success\":true")
    + String("}"));
  }
}

// gestione della modifica di protocollo
void http_handle_protocol() {
  json_deserialize(http_web_server.arg(0));
  if(json_deserialization_error) {
    Serial.println("JSON  -> [ERR ] deserialization");
    http_web_server.send(200, "application/json", String("{")
      + String("\"success\":false")
    + String("}"));
  } else {
    COMMUNICATION_PROTOCOL = (int) json_document["protocol"];
    Serial.println("HTTP  -> [LOG ] new communication protocol -> " + String(COMMUNICATION_PROTOCOL));
    http_web_server.send(200, "application/json", String("{")
      + String("\"success\":true")
    + String("}"));
  }
}

void http_init() {
  Serial.println("HTTP  -> [WAIT] initialization");
  http_web_server.on("/iotfind", http_handle_iot_find);
  http_web_server.on("/dashboard", http_handle_dashboard);
  http_web_server.on("/subscribe", http_handle_subscribe);
  http_web_server.on("/protocol", http_handle_protocol);
  http_web_server.begin();
  Serial.println("HTTP  -> [OK  ] initialization");
}

// gestione delle chiamate da evadere
void http_loop() {
  http_web_server.handleClient();
}

// invio dei dati
void http_send() {
  http_client.begin(http_send_url);
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

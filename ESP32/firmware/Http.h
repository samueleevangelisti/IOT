#ifndef HTTP_H
#define HTTP_H

WebServer http_server(80);
HTTPClient http_client;
String http_send_url;
int http_response_code;

// risposta alla ricerca dei dispositivi iot
void http_handle_iot_find() {
  Serial.println("HTTP  -> [LOG ] iot find request");
  http_server.send(200, "application/json", String("{")
    + String("\"success\":true,")
    + String("\"ip\":\"") + WiFi.localIP() + String("\",")
    + String("\"port\":80")
  + String("}"));
}

// gestione della sottoscrizione dell'observer
void http_handle_subscribe() {
  json_deserialize(http_server.arg(0));
  if(json_deserialization_error) {
    Serial.println("JSON  -> [ERR ] deserialization");
    http_server.send(200, "application/json", String("{")
      + String("\"success\":false")
    + String("}"));
  } else {
    http_send_url = String((const char *) json_document["url"]);
    Serial.println("HTTP  -> [LOG ] new send url -> " + String(http_send_url));
    http_server.send(200, "application/json", String("{")
      + String("\"success\":true")
    + String("}"));
  }
}

void http_init() {
  Serial.println("HTTP  -> [WAIT] initialization");
  http_server.on("/iotfind", http_handle_iot_find);
  http_server.on("/subscribe", http_handle_subscribe);
  http_server.begin();
  Serial.println("HTTP  -> [OK  ] initialization");
}

// invio dei dati
void http_send() {
  http_client.begin(http_send_url);
  http_client.addHeader("Content-type", "application/json");
  http_response_code = http_client.POST(json_get_data_json_string());
  if(http_response_code > 0) {
    Serial.println("HTTP  -> [OK  ] data sent to server");
  } else {
    Serial.println("HTTP  -> [ERR ] unable to send data");
  }
  http_client.end();
}

#endif

#ifndef WIFIUTILS_H
#define WIFIUTILS_H

WiFiClient wifi_client;

void wifi_init() {
  Serial.println("WIFI  -> [WAIT] initialization");
  WiFi.softAP(ESP32_ID, WIFI_AP_PASSWORD);
  Serial.println("WIFI  -> [LOG ] ap ip: " + WiFi.softAPIP().toString());
  Serial.println("WIFI  -> [OK  ] initialization");
}

// connessione alla rete WiFi
void wifi_connect(const char* ssid, const char* password) {
  WiFi.disconnect();
  if(strlen(ssid) == 0) {
    Serial.println("WIFI  -> [LOG ] ssid not set");
  } else {
    WiFi.begin(ssid, password);
    while(WiFi.status() != WL_CONNECTED) {
      Serial.println("WIFI  -> [WAIT] connection");
      delay(1000);
    }
    Serial.println("WIFI  -> [OK  ] connected");
    Serial.println("WIFI  -> [LOG ] ip: " + WiFi.localIP().toString());
  }
}

// connessione alla rete wifi
void wifi_connect() {
  wifi_connect(WIFI_SSID, WIFI_PASSWORD);
}

// lettura del RSSI
void wifi_read() {
  wifi_rssi = WiFi.RSSI();
  Serial.println("WIFI  -> [LOG ] rssi: " + String(wifi_rssi));
}

#endif

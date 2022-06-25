#ifndef WIFIUTILS_H
#define WIFIUTILS_H

#include "WifiAuth.h"

WiFiClient wifi_client;

// connessione alla rete WiFi
void wifi_connect() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while(WiFi.status() != WL_CONNECTED) {
    Serial.println("WIFI  -> [WAIT] connection");
    delay(1000);
  }
  Serial.println("WIFI  -> [OK  ] connected");
  Serial.print("WIFI  -> [LOG ] ip: ");
  Serial.println(WiFi.localIP());
}

// lettura del RSSI
void wifi_read() {
  wifi_rssi = WiFi.RSSI();
  Serial.println("WIFI  -> [LOG ] rssi: " + String(wifi_rssi));
}

#endif

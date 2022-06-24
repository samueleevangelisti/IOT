#ifndef WIFIUTILS_H
#define WIFIUTILS_H

#include <WiFi.h>

#include "WifiAuth.h"

WiFiClient wifi_client;

// connessione alla rete WiFi
void wifi_connect() {
  Serial.print("WIFI -> connection");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while(WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.println("WIFI -> connected");
  Serial.print("WIFI -> IP: ");
  Serial.println(WiFi.localIP());
}

// lettura del RSSI
void wifi_read() {
  Serial.print("WIFI -> rssi: ");
  wifi_rssi = WiFi.RSSI();
  Serial.println(wifi_rssi);
}

#endif

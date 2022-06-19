// IMPORTANT: After opening the serial monitor, click on the RST button in your esp32 device to establish a connection
#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

void initWiFi() {
  //ESP32 connects to an acces point
  WiFi.mode(WIFI_STA);
  //Set the connection with credentials
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  initWiFi();
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
}

void loop() {
  // put your main code here, to run repeatedly:
}

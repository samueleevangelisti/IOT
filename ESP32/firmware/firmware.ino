#include <WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <DHT.h>

#include "Globals.h"
#include "GlobalsAuth.h"
#include "WifiUtils.h"
#include "Json.h"
#include "MqttUtils.h"
//#include "CoAP.h"
#include "Http.h"
#include "Communication.h"
#include "Dht11Utils.h"
#include "Mq2Utils.h"

void setup() {
  Serial.println("SYS   -> [WAIT] initialization");
  pinMode(PIN_MQ2_DO, INPUT);
  Serial.begin(115200);
  wifi_connect();
  communication_init();
  dht11_init();
  Serial.println("SYS   -> [OK  ] initialization");
}

void loop() {
  Serial.println("==================================================");
  wifi_read();
  dht11_read();
  mq2_read();
  communication_send();
  delay(SAMPLE_FREQUENCY);
}

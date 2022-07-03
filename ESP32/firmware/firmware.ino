#include <WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiUdp.h>
#include <coap-simple.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <DHT.h>

#include "GlobalsAuth.h"
#include "Globals.h"
#include "WifiUtils.h"
#include "JsonUtils.h"
#include "MqttUtils.h"
#include "CoapUtils.h"
#include "HttpUtils.h"
#include "Communication.h"
#include "Dht11Utils.h"
#include "Mq2Utils.h"

void setup() {
  pinMode(PIN_MQ2_DO, INPUT);
  Serial.begin(115200);
  Serial.println("SYS   -> [WAIT] initialization");
  wifi_connect();
  communication_init();
  dht11_init();
  Serial.println("SYS   -> [OK  ] initialization");
}

void loop() {
  Serial.println("==================================================");
  communication_loop();
  wifi_read();
  dht11_read();
  mq2_read();
  communication_send();
  delay(SAMPLE_FREQUENCY);
}

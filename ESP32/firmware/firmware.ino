#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#include "Globals.h"
#include "GlobalsAuth.h"
#include "WifiUtils.h"
#include "MqttUtils.h"
#include "Dht11Utils.h"
#include "Mq2Utils.h"
#include "CoAP.h"
void setup() {
  Serial.println("SYS   -> [WAIT] initialization");
  pinMode(PIN_MQ2_DO, INPUT);
  Serial.begin(115200);
  wifi_connect();
  //mqtt_init();
  //mqtt_connect();
  dht11_init();
  coap_setup();
  Serial.println("SYS   -> [OK  ] initialization");
}

void loop() {
  Serial.println("==================================================");
  wifi_read();
  dht11_read();
  mq2_read();
  //mqtt_publish();
  coap_process();
  delay(SAMPLE_FREQUENCY);
}

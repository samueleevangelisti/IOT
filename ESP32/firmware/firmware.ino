#include "Globals.h"
#include "WifiUtils.h"
#include "MqttUtils.h"
#include "Dht11Utils.h"
#include "Mq2Utils.h"

void setup() {
  Serial.println("==================================================");
  pinMode(PIN_MQ2_DO, INPUT);
  Serial.begin(115200);
  wifi_connect();
  mqtt_init();
  mqtt_connect();
  dht11_init();
}

void loop() {
  Serial.println("==================================================");
  wifi_read();
  dht11_read();
  mq2_read();
  mqtt_publish();
  delay(SAMPLE_FREQUENCY);
}

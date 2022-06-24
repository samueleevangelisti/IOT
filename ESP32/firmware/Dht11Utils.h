#ifndef DHT11UTILS_H
#define DHT11UTILS_H

#include <DHT.h>

DHT dht11(PIN_DHT11, DHT11);

// inizializzazione del sensore DHT11
void dht11_init() {
  dht11.begin();
}

// lettura dei dati di DHT11
void dht11_read() {
  Serial.print("DHT11 -> ");
  dht11_temperature = dht11.readTemperature();
  dht11_humidity = dht11.readHumidity();
  Serial.print("temperature: ");
  Serial.print(dht11_temperature);
  Serial.print("*C humidity: ");
  Serial.print(dht11_humidity);
  Serial.println("%");
}

#endif

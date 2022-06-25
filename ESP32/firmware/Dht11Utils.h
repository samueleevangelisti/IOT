#ifndef DHT11UTILS_H
#define DHT11UTILS_H

DHT dht11(PIN_DHT11, DHT11);

// inizializzazione del sensore DHT11
void dht11_init() {
  Serial.println("DHT11 -> [WAIT] initialization");
  dht11.begin();
  Serial.println("DHT11 -> [OK  ] initialization");
}

// lettura dei dati di DHT11
void dht11_read() {
  dht11_temperature = dht11.readTemperature();
  dht11_humidity = dht11.readHumidity();
  Serial.println("DHT11 -> [LOG ] temperature: " + String(dht11_temperature) + "*C humidity: " + String(dht11_humidity) + "%");
}

#endif

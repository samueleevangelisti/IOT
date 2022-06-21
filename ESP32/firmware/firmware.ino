#include <SimpleDHT.h>

#define PIN_DHT11 0

#define PIN_MQ2_AO 34
#define PIN_MQ2_DO 35

// DHT11 sampling rate is 1HZ.
int SAMPLE_FREQUENCY;

SimpleDHT11 dht11(PIN_DHT11);
float dht11_temperature;
float dht11_humidity;
int dht11_status;

int mq2_gas;
int mq2_gas_percentage;
boolean mq2_isGas;
String mq2_isGas_string;

void setup() {
  SAMPLE_FREQUENCY = 1000;
  pinMode(PIN_MQ2_DO, INPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println("==================================================");
  
  Serial.print("DHT11 ->   ");
  dht11_status = dht11.read2(&dht11_temperature, &dht11_humidity, NULL);
  if (dht11_status == SimpleDHTErrSuccess) {
    Serial.print("temperature: ");
    Serial.print(dht11_temperature);
    Serial.print("*C   humidity: ");
    Serial.print(dht11_humidity);
    Serial.println("%");
  } else {
    Serial.print("error: ");
    Serial.print(SimpleDHTErrCode(dht11_status));
    Serial.print(" duration: ");
    Serial.println(SimpleDHTErrDuration(dht11_status));
  }

  Serial.print("MQ2   ->   ");
  mq2_gas = analogRead(PIN_MQ2_AO);
  mq2_gas_percentage = map(mq2_gas, 0, 4095, 0, 100);
  mq2_isGas = digitalRead(PIN_MQ2_DO);
  if(mq2_isGas) {
    mq2_isGas_string = "No";
  } else {
    mq2_isGas_string = "Yes";
  }
  Serial.print("gas: ");
  Serial.print(mq2_gas_percentage);
  Serial.print("%   alert: ");
  Serial.println(mq2_isGas_string);
  
  delay(SAMPLE_FREQUENCY);
}

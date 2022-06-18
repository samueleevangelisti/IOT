#include "DHT.h"
#define DHT11PIN 21
DHT dht(DHT11PIN, DHT11);

/*MQ2*/
int Buzzer = 32;       /*NON MODIFICARE*/
int Gas_analog = 35;    /*AO*/
int Gas_digital = 27;   /*DO*/

void setup()
{
  
  Serial.begin(115200);
/* Start the DHT11 Sensor */
  dht.begin();
  
  pinMode(Buzzer, OUTPUT);      
  pinMode(Gas_digital, INPUT);
}

void loop()
{
  /*DHT11*/
  float humi = dht.readHumidity();
  float temp = dht.readTemperature();
  
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print("ºC ");
  Serial.print("Humidity: ");
  Serial.println(humi);

  /*MQ2*/
  int gassensorAnalog = analogRead(Gas_analog);
  int gassensorDigital = digitalRead(Gas_digital);

  Serial.print("Gas Sensor: ");
  Serial.print(gassensorAnalog);
  Serial.print("\t");
  Serial.print("Gas Class: ");
  Serial.print(gassensorDigital);
  Serial.print("\t");
  Serial.print("\t");
  
  if (gassensorAnalog > 1000) {
    Serial.println("Gas\n");
    digitalWrite (Buzzer, HIGH) ; //send tone
    delay(1000);
    digitalWrite (Buzzer, LOW) ;  //no tone
  }
  else {
    Serial.println("No Gas\n");
  }
  
  delay(1000);
}

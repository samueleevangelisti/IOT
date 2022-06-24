#ifndef MQ2UTILS_H
#define MQ2UTILS_H

void mq2_read() {
  Serial.print("MQ2 -> ");
  mq2_gas = analogRead(PIN_MQ2_AO);
  mq2_gas_ppm = map(mq2_gas, 0, 4095, 200, 10000);
  mq2_isGas = digitalRead(PIN_MQ2_DO);
  if(mq2_isGas) {
    mq2_isGas_string = "No";
  } else {
    mq2_isGas_string = "Yes";
  }
  Serial.print("gas: ");
  Serial.print(mq2_gas_ppm);
  Serial.print("ppm is gas: ");
  Serial.println(mq2_isGas_string);
}

#endif

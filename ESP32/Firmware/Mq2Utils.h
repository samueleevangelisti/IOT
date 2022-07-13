#ifndef MQ2UTILS_H
#define MQ2UTILS_H

#define MQ2_AQI_ARR_MAX_LENGTH 5 // dimensione della moving average window

int mq2_gas; // gas rilevato
boolean mq2_isGas; // allarme per il gas
String mq2_isGas_string; // stringa di allarme per il gas
int mq2_aqi_arr[MQ2_AQI_ARR_MAX_LENGTH]; // array con le rilevazioni per AQI
int mq2_aqi_arr_length = 0; // lunghezza attuale dell'array per AQI
float mq2_aqi_tmp; // variabile temporanea per il calcolo di AQI

// inserimento di un nuovo valore nell'arrai per il calcolo di AQI
void mq2_arr_push() {
  if(mq2_aqi_arr_length < MQ2_AQI_ARR_MAX_LENGTH) {
    mq2_aqi_arr[mq2_aqi_arr_length] = mq2_gas_ppm;
    mq2_aqi_arr_length++;
  } else {
    for(int i = 1; i < MQ2_AQI_ARR_MAX_LENGTH; i++) {
      mq2_aqi_arr[i - 1] = mq2_aqi_arr[i];
    }
    mq2_aqi_arr[MQ2_AQI_ARR_MAX_LENGTH - 1] = mq2_gas_ppm;
  }
}

// calcolo di AQI
void mq2_aqi_calc() {
  mq2_aqi_tmp = 0;
  for(int i = 0; i < mq2_aqi_arr_length; i++) {
    mq2_aqi_tmp += mq2_aqi_arr[i];
  }
  mq2_aqi_tmp /= mq2_aqi_arr_length;
  if(mq2_aqi_tmp >= MAX_GAS_VALUE) {
    mq2_aqi = 0;
  } else if(mq2_aqi_tmp >= MIN_GAS_VALUE) {
    mq2_aqi = 1;
  } else {
    mq2_aqi = 2;
  }
}

// lettura dei dati di MQ2
void mq2_read() {
  mq2_gas = analogRead(PIN_MQ2_AO);
  mq2_gas_ppm = map(mq2_gas, 0, 4095, 200, 10000);
  mq2_isGas = digitalRead(PIN_MQ2_DO);
  if(mq2_isGas) {
    mq2_isGas_string = "No";
  } else {
    mq2_isGas_string = "Yes";
  }
  mq2_arr_push();
  mq2_aqi_calc();
  Serial.println("MQ2   -> [LOG ] gas: " + String(mq2_gas_ppm) + "ppm alert: " + String(mq2_isGas_string));
}

#endif

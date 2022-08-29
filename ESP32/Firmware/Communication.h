#ifndef COMMUNICATION_H
#define COMMUNICATION_H

// inizializzazione dei protocolli
void communication_init() {
  mqtt_init();
  coap_init();
  http_init();
}

// gestione delle chiamate da evadere
void communication_loop() {
  mqtt_loop();
  coap_loop();
  http_loop();
}

// invio dei dati
void communication_send() {
  switch(COMMUNICATION_PROTOCOL) {
    case 0:
      mqtt_publish();
      break;
    case 1:
      coap_send();
      break;
    case 2:
      http_send();
      break;
  }
}

#endif

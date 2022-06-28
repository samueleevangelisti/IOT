#ifndef COMMUNICATION_H
#define COMMUNICATION_H

// inizializzazione dei protocolli
void communication_init() {
  mqtt_init();
  mqtt_connect();
}

// invio dei dati
void communication_send() {
  switch(communication_protocol) {
    case 0:
      mqtt_publish();
      break;
    case 1:
      break;
  }
}

#endif

#ifndef COMMUNICATION_H
#define COMMUNICATION_H

int communication_protocol = 0; // protocollo di comunicazione, 0: MQTT, 1: COAP, 2: HTTP

// inizializzazione dei protocolli
void communication_init() {
  mqtt_init();
  mqtt_connect();
  http_init();
}

// invio dei dati
void communication_send() {
  switch(communication_protocol) {
    case 0:
      mqtt_publish();
      break;
    case 1:
      break;
    case 2:
      http_send();
      break;
  }
}

#endif

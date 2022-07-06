#ifndef COAPUTILS_H
#define COAPUTILS_H

#include "CoapAuth.h"

WiFiUDP coap_wifi_udp;
Coap coap(coap_wifi_udp);

// CoAP client response callback
void callback_response(CoapPacket &packet, IPAddress ip, int port) {
  if(packet.type == COAP_ACK) {
    wifi_packet_delay = millis() - SAMPLE_FREQUENCY - wifi_packet_timestamp_start;
    Serial.println("COAP  -> [OK  ] data sent to server");
    wifi_packet_sent = 0;
  } else {
    Serial.println("COAP  -> [ERR ] unable to send data");
  }
}

// inizializzazione del protocollo
void coap_init() {
  Serial.println("COAP  -> [WAIT] initialization");
  coap.response(callback_response);
  coap.start();
  Serial.println("COAP  -> [OK  ] initialization");
}

// invio dei dati
void coap_send() {
  wifi_packet_sent++;
  wifi_packet_timestamp_start = millis();
  coap.put(COAP_SERVER, 5683, COAP_URL, get_data_string().c_str());
  Serial.println("COAP  -> [LOG ] sending data");
}

#endif

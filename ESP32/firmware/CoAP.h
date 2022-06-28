#include <WiFi.h>
#include <ArduinoJson.h>
//Include Thing.CoAP
#include "Thing.CoAP.h"

//Declare our CoAP server and the packet handler
Thing::CoAP::Server server;
Thing::CoAP::ESP::UDPPacketProvider udpProvider;


//----------------------DA FIXARE------------------------------------
//Change here your WiFi settings
char* ssid = "FASTWEB-D8119D";
char* password = "T9E47NCWMZ";
//-------------------------------------------------------------------

//Creation of json 
const int capacity = JSON_OBJECT_SIZE(192); 
StaticJsonDocument<capacity> doc; // Json 
char buffer_ff[sizeof(doc)]; // buffer for Json message


void coap_setup() {
  //Initializing the Serial
  Serial.println("COAP  -> [OK ] Initialization");

  //Configure our server to use our packet handler (It will use UDP)
  server.SetPacketProvider(udpProvider);

  server.CreateResource("DATA", Thing::CoAP::ContentFormat::TextPlain, true) //True means that this resource is observable
    .OnGet([](Thing::CoAP::Request & request) { //We are here configuring telling our server that, when we receive a "GET" request to this endpoint, run the the following code
     
      //Return the current state of our "LED".
      Serial.println("COAP  -> [LOG ] Received Request");

      
    String json = String("{")
      + String("\"measurement\":\"sensor\",")
      + String("\"tags\":{")
        + String("\"id\":\"") + String(ESP32_ID) + String("\",")
        + String("\"latitude\":") + String(ESP32_LATITUDE, 6) + String(",")
        + String("\"longitude\":") + String(ESP32_LONGITUDE, 6)
      + String("},")
      + String("\"fields\":{")
        + String("\"rssi\":") + String(wifi_rssi) + String(",")
        + String("\"temperature\":") + String(dht11_temperature) + String(",")
        + String("\"humidity\":") + String(dht11_humidity) + String(",")
        + String("\"gas\":") + String(mq2_gas_ppm) + String(",")
        + String("\"aqi\":") + String(mq2_aqi)
      + String("}")
    + String("}");

//set json data
  doc["id"] = ESP32_ID;
  doc["gps"]["lat"] = ESP32_LATITUDE;
  doc["gps"]["lng"] = ESP32_LONGITUDE;
  doc["rss"] = wifi_rssi;
  doc["temp"] = dht11_temperature;
  doc["hum"] = dht11_humidity;
  doc["gasv"]["gas"] = mq2_gas_ppm;
  doc["gasv"]["AQI"] = mq2_aqi;

  serializeJson(doc, buffer_ff); //Json serialization
  Serial.println(buffer_ff);
  
      return Thing::CoAP::Status::Content(json.c_str());
    });
    

    server.Start();
}


void coap_process() {
server.Process();
}

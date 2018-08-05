#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>

WiFiServer server(8080);
WiFiClient client;

void setup() 
{
  // WIFI_AP_STA mode sets the esp8266 to be able to act like both an accesspoint and a client
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP("hyx0822", "hyx109876");
  
  Serial.begin(115200);
  server.begin();
}
void loop()
{
    // If there is not client connected yet
    if (!client.connected()) {
        // try to connect to a new client
        client = server.available();
    } else {
    // read data from the connected client
        if (client.available() > 0) {
          byte inByte= client.read();
          //String in=(String) inChar;

            Serial.print(inByte); 
             
            // send back the response from the Arduino Due  
            if(Serial.available()){ 
              // I am not very sure if client.write() of client.print() should be used here, but both seem to work  
              client.write(Serial.read());
              // client.print(Serial.read());
            }
        }
    }

}

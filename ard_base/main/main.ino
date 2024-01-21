#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "ShortInt";
const char* password = "11111111";

const char* serverName = "http://192.168.166.210:1984/api/addARobot";

char jsonOutput[128];

unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

void createNew() {
  if(WiFi.status()== WL_CONNECTED){
    WiFiClient client;
    HTTPClient http;
    
    http.begin(client, serverName);

    http.addHeader("Content-Type", "application/json");

    const size_t CAPACITY = JSON_OBJECT_SIZE(1);
    StaticJsonDocument<CAPACITY> doc;

    JsonObject object  = doc.to<JsonObject>();
    object["lati"] = "21.42";
    object["long"] = "39.82";

    serializeJson(doc, jsonOutput);
      
    int httpResponseCode = http.POST(String(jsonOutput));
      
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  delay(5000);
  createNew();
}

void loop() {}

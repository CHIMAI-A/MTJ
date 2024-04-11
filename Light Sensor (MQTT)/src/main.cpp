#include <Arduino.h>
#define LIGHT_SENSOR_PIN 33  // ESP32's pin GPIO13 connected to DO pin of the ldr module
#define LED_PIN 25
//#define MOTION_SENSOR_PIN 16 

#include <WiFi.h>
#include <PubSubClient.h>

//int pinStateCurrent   = LOW;  // current state of pin
//int pinStatePrevious  = LOW;  // previous state of pin

const char* ssid = "";
const char* password = "";

const char* mqtt_broker = ""; // The IP address of your Mosquitto broker
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void reconnect();
void callback(char* topic, byte* payload, unsigned int length);
void setup_wifi() ;

void setup() {

  Serial.begin(115200);


    pinMode(LED_PIN, OUTPUT); // declare the ledPin as an OUTPUT
    //pinMode(MOTION_SENSOR_PIN, INPUT);
    setup_wifi();
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);

}

void loop() {

  if (!client.connected()) {
    reconnect();
    }
  client.loop();

   delay(10);
}
void setup_wifi() {
  delay(10);
  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("*");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  String topicStr = String(topic);
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);
if(topicStr == "esp32_S3_Box_ZoneOne/cam/detect"){
  int person = atoi( message.c_str() );

int lightValue = analogRead(LIGHT_SENSOR_PIN);
    Serial.println(lightValue);
    int brightness = map(lightValue, 0, 4095, 0, 255);

  if (person>0){

    
    analogWrite(LED_PIN, brightness);

  } else{
    if (lightValue>500){
       analogWrite(LED_PIN, 50);
    }else{
      analogWrite(LED_PIN, 0);
    }
    
  }
}

  Serial.println();
}

void reconnect() {   // for MQTT connection
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32_dev_ZoneOne_Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("esp32_dev_ZoneOne", " esp32_dev_ZoneOne is connected");
      // ... and resubscribe
      
      client.subscribe("esp32_S3_Box_ZoneOne/cam/detect");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

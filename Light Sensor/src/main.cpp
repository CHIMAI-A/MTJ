#include <Arduino.h>

#define LIGHT_SENSOR_PIN 45  // ESP32's pin GPIO13 connected to DO pin of the ldr module
#define LED_PIN 31



int pinStateCurrent   = LOW;  // current state of pin
int pinStatePrevious  = LOW;  // previous state of pin


void setup() {

  Serial.begin(115200);

    pinMode(LED_PIN, OUTPUT); // declare the ledPin as an OUTPUT
    

}

void loop() {
    

    int lightValue = analogRead(LIGHT_SENSOR_PIN);
    int brightness = map(lightValue, 0, 4095, 0, 255);

 
      //
      Serial.println(brightness);
      //
      analogWrite(LED_PIN, brightness);
      delay (10);
   

  

    analogWrite(LED_PIN, 0); 
   

  }

 
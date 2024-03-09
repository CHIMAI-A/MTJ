#include <Arduino.h>

#define PIN_RED    21 // The ESP32 pin GPIO25 connected to R pin of traffic light module
#define PIN_YELLOW 45 // The ESP32 pin GPIO26 connected to Y pin of traffic light module
#define PIN_GREEN  46 // The ESP32 pin GPIO27 connected to G pin of traffic light module

#define RED_TIME 2000     // RED time in millisecond
#define YELLOW_TIME 1000  // YELLOW time in millisecond
#define GREEN_TIME 2000   // GREEN time in millisecond

#define RED  0    // Index in array
#define YELLOW 1  // Index in array
#define GREEN  2  // Index in array

const int pins[] = { PIN_RED, PIN_YELLOW, PIN_GREEN };
const int times[] = { RED_TIME, YELLOW_TIME, GREEN_TIME };


// put function declarations here:
int myFunction(int, int);

void setup() {
  // put your setup code here, to run once:
  pinMode(PIN_RED, OUTPUT);
  pinMode(PIN_YELLOW, OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
  int result = myFunction(2, 3);
}

void trafic_light_on(int light) {
  for (int i = RED; i <= GREEN; i++) {
    if (i == light)
      digitalWrite(pins[i], HIGH);  // turn on
    else
      digitalWrite(pins[i], LOW);  // turn off
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  // red light on
  trafic_light_on(RED);
  delay(times[RED]);  // keep red light on during a period of time

  // yellow light on
  trafic_light_on(YELLOW);
  delay(times[YELLOW]);  // keep yellow light on during a period of time

  // green light on
  trafic_light_on(GREEN);
  delay(times[GREEN]);  // keep green light on during a period of time
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}


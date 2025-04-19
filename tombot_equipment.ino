#include "Arduino_SensorKit.h"
#define Environment Environment_I2C

const int trigPin = 9;
const int echoPin = 10;
long duration;
int distance;

const int totalReadings = 30;
int index = 0;

float distances[totalReadings];
bool lights[totalReadings];

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(5, INPUT);  // assuming light sensor is digital on pin 5

  Serial.begin(9600);
  Wire.begin();
  Environment.begin();
}

void loop() {
  // Read light sensor
  bool light_sens = digitalRead(5);

  // Read distance from ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // Store readings
  distances[index] = distance;
  lights[index] = light_sens;
  index = (index + 1) % totalReadings;

  // When buffer is full, compute stats
  if (index == 0) {
    float sum_distance = 0;
    float sum_lights = 0;

    for (int i = 0; i < totalReadings; i++) {
      sum_distance += distances[i];
      sum_lights += lights[i];  // true = 1.0, false = 0.0
    }

    float mean = sum_distance / totalReadings;

    float variance = 0;
    for (int i = 0; i < totalReadings; i++) {
      variance += (distances[i] - mean) * (distances[i] - mean);
    }
    float stdDev = sqrt(variance / totalReadings);

    // Temperature (convert to Fahrenheit)
    float tempF = (Environment.readTemperature() * 9.0 / 5.0) + 32;

    // Movement detection based on distance standard deviation
    bool movement = stdDev > 2.0;  // adjust threshold if needed

    // Light "median" detection: majority rules
    bool light_median = sum_lights > (totalReadings / 2);

    // 📤 Output
    Serial.print("Temperature:");
    Serial.print(tempF);
    Serial.print(",Distance:");
    Serial.print(movement ? 1 : 0);  // 1 = movement, 0 = none
    Serial.print(",Lights:");
    Serial.println(light_median ? 1 : 0);  // 1 = bright, 0 = dark
  }

  delay(250);  // Wait 0.5 sec between readings
}

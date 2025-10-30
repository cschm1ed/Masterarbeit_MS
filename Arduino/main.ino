#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;

void setup(void) {
  Serial.begin(115200);
  while (!Serial);

  if (!ina219.begin()) {
    Serial.println("Kein INA219-Sensor gefunden.");
    while (1);
  }

  ina219.setCalibration_32V_2A();
}

void loop(void) {
  float current_mA = ina219.getCurrent_mA();

  if (current_mA > 2000) {
    Serial.println("Ueberhitzung erkannt!");
  } else {
    Serial.println(current_mA);
  }

  delay(5);
}
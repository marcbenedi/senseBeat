#include <Arduino.h>
#include <Wire.h> // Importing the I2C library.

const int I2C_adress_MPU = 0x68; // I2C Address of the MPU6050.
int16_t Beschleunigung_x, Beschleunigung_y, Beschleunigung_z; // Variables for the Accelerometer sensor
int16_t gyro_x, gyro_y, gyro_z; // Variables for the Gyroscope
int16_t Temperatur; // Variable in which the temperature is saved
char tmp_str[7];
char * convert_int16_to_str(int16_t i) {
    sprintf(tmp_str, "%6d", i);
    return tmp_str;
}

void motion_setup() {
  Wire.begin();
  Wire.beginTransmission(I2C_adress_MPU); // Starting the I2C transmission
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}

void motion_loop() {
  Wire.beginTransmission(I2C_adress_MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(I2C_adress_MPU, 7 * 2, true);
  Beschleunigung_x = Wire.read() << 8 | Wire.read();
  Beschleunigung_y = Wire.read() << 8 | Wire.read();
  Beschleunigung_z = Wire.read() << 8 | Wire.read();
  Temperatur = Wire.read() << 8 | Wire.read();
  gyro_x = Wire.read() << 8 | Wire.read();
  gyro_y = Wire.read() << 8 | Wire.read();
  gyro_z = Wire.read() << 8 | Wire.read();
  Serial.print(convert_int16_to_str(Beschleunigung_x + 1100));
  Serial.print(",");
  Serial.print(convert_int16_to_str(Beschleunigung_y + 200));
  Serial.print(",");
  Serial.print(convert_int16_to_str(Beschleunigung_z + 16800 + 31800));
  Serial.print(",");
  Serial.print(convert_int16_to_str(gyro_x + 480));
  Serial.print(",");
  Serial.print(convert_int16_to_str(gyro_y - 80));
  Serial.print(",");
  Serial.print(convert_int16_to_str(gyro_z - 150));
  Serial.println(";");
}

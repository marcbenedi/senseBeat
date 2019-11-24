#include <Arduino.h>
#include <Wire.h> // Importing the I2C library. Motion sensor
#include <SoftwareSerial.h> //Bluetooth

SoftwareSerial MyBlue(2, 3); // RX | TX

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
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

  MyBlue.print(convert_int16_to_str(Beschleunigung_x + 1000));
  MyBlue.print(",");
  MyBlue.print(convert_int16_to_str(Beschleunigung_y -300));
  MyBlue.print(",");
  MyBlue.print(convert_int16_to_str(Beschleunigung_z - 17000 ));
  MyBlue.print(",");
  MyBlue.print(convert_int16_to_str(gyro_x + 480));
  MyBlue.print(",");
  MyBlue.print(convert_int16_to_str(gyro_y - 80));
  MyBlue.print(",");
  MyBlue.print(convert_int16_to_str(gyro_z - 150));
  MyBlue.println();
}
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
// void bluetooth_setup() {
//   MyBlue.begin(9600);
//   MyBlue.println("Ready to connect\nDefualt password is 1234 or 000");
// }

// void bluetooth_loop() {
//   // if (MyBlue.available())  {
//   //   Serial.println(MyBlue.read());
//   // } else {
//   //   Serial.println("empty");
//   // }
//   // if (Serial.available()) {
//   //   // Serial.write("Serial.read()");
//   //   MyBlue.write(Serial.read());
//   // }
//   // MyBlue.println("hello from arduino");
// }

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

void setup() {
    MyBlue.begin(9600);
    // Serial.begin(9600);
    motion_setup();
    // bluetooth_setup();
}

void loop() {
  motion_loop();
  // bluetooth_loop();
  delay(50);
}

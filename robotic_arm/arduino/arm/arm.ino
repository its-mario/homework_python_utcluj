#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <Servo.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int servoMin = 125;  // Minimum pulse length
int servoMax = 650;  // Maximum pulse length
Servo gripperServo;

void setup() {
  Serial.begin(9600);
  pwm.begin();
  delay(10);
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz

  gripperServo.attach(3);
}


int angleToPulse(int ang)  //gets angle in degree and returns the pulse width
{
  int pulse = map(ang, 0, 180, servoMin, servoMax);  // map angle of 0 to 180 to Servo min and Servo max
  return pulse;
}


int V_C = 10;

int j1_i = -1000;
int j2_i = -1000;
int j3_i = -1000;
int j4_i = -1000;
int gripp_i = -1000;

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');

    int comma1 = data.indexOf(',');
    int comma2 = data.indexOf(',', comma1 + 1);
    int comma3 = data.indexOf(',', comma2 + 1);
    int comma4 = data.indexOf(',', comma3 + 1);



    if (j1_i != -1000 && j2_i != -1000 && j3_i != -1000 && j4_i != -1000 && gripp_i != -1000) {
      int j1 = data.substring(0, comma1).toInt();
      int j2 = data.substring(comma1 + 1, comma2).toInt();
      int j3 = data.substring(comma2 + 1, comma3).toInt();
      int j4 = data.substring(comma3 + 1, comma4).toInt();
      int gripper = data.substring(comma4 + 1).toInt();
      if (j1 >= -90 && j1 <= 90 && j2 >= 0 && j2 <= 100 && j3 >= -90 && j3 <= 90 && j4 >= -90 && j4 <= 90 && gripper >= 0 && gripper <= 90) {  // validam unghiurile cerute
        j1 += 90;
        j2 = 180 - j2;
        j3 += 90;
        j4 += 90;
        gripper += 90;
        int a = (j1 - j1_i) / V_C;
        int b = (j2 - j2_i) / V_C;
        int c = (j3 - j3_i) / V_C;
        int d = (j4 - j4_i) / V_C;
        int e = (gripper - gripp_i) / V_C;
        for (int i = 1; i <= V_C; i++) {
          j1_i += a;
          j2_i += b;
          j3_i += c;
          j4_i += d;
          gripper += e;
          pwm.setPWM(12, 0, angleToPulse(j1_i));  // Q1 baza
          pwm.setPWM(13, 0, angleToPulse(j2_i));  // Q2
          pwm.setPWM(14, 0, angleToPulse(j3_i));  // Q3
          pwm.setPWM(15, 0, angleToPulse(j4_i));  // Q4
          gripperServo.write(angleToPulse(gripper));
          delay(5);
        }

        j1_i = j1;
        j2_i = j2;
        j3_i = j3;
        j4_i = j4;
        gripp_i = gripper;
      }

    }

    else {
      int j1 = data.substring(0, comma1).toInt();
      int j2 = data.substring(comma1 + 1, comma2).toInt();
      int j3 = data.substring(comma2 + 1, comma3).toInt();
      int j4 = data.substring(comma3 + 1, comma4).toInt();
      int gripper = data.substring(comma4 + 1).toInt();
      pwm.setPWM(12, 0, angleToPulse(j1 + 90));        // Q1 baza
      pwm.setPWM(13, 0, angleToPulse(180 - j2));       // Q2
      pwm.setPWM(14, 0, angleToPulse(j3 + 90));        // Q3
      pwm.setPWM(15, 0, angleToPulse(j4 + 90));        // Q4
      gripperServo.write(angleToPulse(gripper + 90));  // gripper
      delay(10);
      j1_i = j1 + 90;
      j2_i = 180 - j2;
      j3_i = j3 + 90;
      j4_i = j4 + 90;
      gripp_i = gripper + 90;
    }
  }
}
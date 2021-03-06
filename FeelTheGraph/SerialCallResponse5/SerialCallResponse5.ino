#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myStepper = AFMS.getStepper(200, 2);
// And connect a DC motor to port M1
Adafruit_DCMotor *motor = AFMS.getMotor(3);
Adafruit_DCMotor *motor1 = AFMS.getMotor(4);

// DC motor on M2
int motor_offset=80;
int inByte ; // incoming serial byte
int Moutx=0;
int Mouty=0;
char buffer1[11];
char read1[4];
char read2[4];
int val1=256;
int val2=256;
void setup() {
  // start serial port at 9600 bps:
  AFMS.begin(); 
  Serial.begin(19200);
  motor->setSpeed(200);
  motor->run(RELEASE);
  motor1->setSpeed(200);
  motor1->run(RELEASE);
}

void loop() {
  // if we get a valid byte, read analog ins:
 while (Serial.available()) {
 Serial.readBytes(buffer1,11);
      
  if (buffer1[0]=='a'){
      read1[0] = buffer1[1];
      read1[1] = buffer1[2];
      read1[2] = buffer1[3];
      read1[3] = '\0';
      val1=atoi(read1);
      read2[0] = buffer1[5];
      read2[1] = buffer1[6];
      read2[2] = buffer1[7];
      read2[3] = '\0';
      val2=atoi(read2);
      Serial.println(val1+val2);
//      
  }else{
    Serial.println(buffer1[0]);
  }
 }
      int red=val1-256;
      int green=val2-256;
       if (red>0){
          motor->run(FORWARD);
          Moutx=map(red,0,250,motor_offset,250);
          motor->setSpeed(Moutx);
       }else if(red<0){
          motor->run(BACKWARD);
           Moutx=map(-red,0,250,motor_offset,250);
          motor->setSpeed(Moutx);
       }else if(red==0){
          motor->run(RELEASE);
       }
       if (green>0){
          motor1->run(FORWARD);
          Mouty=map(green,0,250,motor_offset,250);
          motor1->setSpeed(Mouty);
       }else if(green<0){
          motor1->run(BACKWARD);
          Mouty=map(-green,0,250,motor_offset,250);
          motor1->setSpeed(Mouty);
       }else if(green==0){
          motor1->run(RELEASE);
       }
}


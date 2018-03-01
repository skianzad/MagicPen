#include <AFMotor.h>
// DC motor on M2
AF_DCMotor motor(2);
AF_DCMotor motor1(1);
int motor_offset=50;
int inByte ; // incoming serial byte
int Moutx=0;
int Mouty=0;
char buffer1[9];
char read1[4];
char read2[4];
int val1=356;
int val2=356;
void setup() {
  // start serial port at 9600 bps:
  Serial.begin(9600);
  motor.setSpeed(200);
  motor.run(RELEASE);
  motor1.setSpeed(200);
  motor1.run(RELEASE);
}

void loop() {
  // if we get a valid byte, read analog ins:
 while (Serial.available()) {
 Serial.readBytes(buffer1,9);
    if(true){
      int t=Serial.println(buffer1);
      Serial.println(t);
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
    }else{
      Serial.println("testtesttest");
    }
 }

      int red=val1-356;
      int green=val2-356;
       if (red>0){
          motor.run(FORWARD);
          Moutx=map(red,0,250,motor_offset,250);
          motor.setSpeed(Moutx);
       }else if(red<0){
          motor.run(BACKWARD);
           Moutx=map(-red,0,250,motor_offset,250);
          motor.setSpeed(Moutx);
       }else if(red==0){
          motor.run(RELEASE);
       }
       if (green>0){
          motor1.run(FORWARD);
          Mouty=map(green,0,250,motor_offset,250);
          motor1.setSpeed(Mouty);
       }else if(green<0){
          motor1.run(BACKWARD);
          Mouty=map(-green,0,250,motor_offset,250);
          motor1.setSpeed(Mouty);
       }else if(green==0){
          motor1.run(RELEASE);
       }
}


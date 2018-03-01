#include <AFMotor.h>
// DC motor on M2
AF_DCMotor motor(2);
AF_DCMotor motor1(1);
int motor_offset=50;
int inByte ; // incoming serial byte
int Moutx=0;
int Mouty=0;
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
 while (Serial.available() > 0) {
    int read1 = Serial.parseInt();
    // do it again:
    int read2 = Serial.parseInt();
    if (Serial.read() == '\n'){ 
      int red=read1-256;
      int green=read2-256;
       if (red>0&&red!=256){
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
       if (green>0&&green!=256){
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
       Serial.println(red+green);
    }
  }
}


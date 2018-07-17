/**
 ************************************************************************************************
 * @file       Haply_Arduino_Control.ino
 * @author     Steve Ding, Colin Gallacher
 * @version    V0.1.0
 * @date       27-February-2017
 * @brief      Haply board control for encoder read and torque write using on-board actuator
 *             ports
 ************************************************************************************************
 * @attention
 *
 *
 ************************************************************************************************
 */

/* includes ************************************************************************************/
#include <stdlib.h>
#include <Encoder.h>
#include <pwm01.h>
#include "Haply_Arduino_Control.h"



/* Actuator parameter declarations *************************************************************/
actuator 	Motor1;
actuator 	Motor2;
actuator 	Motor3;
actuator 	Motor4;


/* Actuator Status and Command declarations ****************************************************/

/* Address of device that sent data */
byte 		device_address;

/* communication interface control, defines type of instructions recieved */
byte 		cmd_code;  

/* Active actuators indicator */
byte 		motors_active[TOTAL_ACTUATORS]; 

/* Number of motors actively setup and used */
int  		number_of_motors;  

/* communication interface control, defines response to send */
byte 		reply_code = 3;


/* Iterator and debug definitions **************************************************************/
long 		lastPublish = 0;
int  		ledPin = 13;



/* main setup and loop block  *****************************************************************/

/**
 * @brief    Main setup function, defines parameters and hardware setup
 */
void setup() {
	pinMode(ledPin, OUTPUT);
	digitalWrite(ledPin, LOW);
	SerialUSB.begin(115200);
 pinMode(Lft, INPUT_PULLUP);
attachInterrupt(digitalPinToInterrupt(Lft), Right, CHANGE);
pinMode(Rht,INPUT_PULLUP);
attachInterrupt(digitalPinToInterrupt(Rht), Left, CHANGE);
pinMode(Up, INPUT_PULLUP);
attachInterrupt(digitalPinToInterrupt(Up), Upa, CHANGE);
pinMode(Dwn, INPUT_PULLUP);
attachInterrupt(digitalPinToInterrupt(Dwn), Down, CHANGE);
}


/**
 * @brief    Main loop function
 */
void loop() {
  
	if(micros() - lastPublish >= 50){
    
		lastPublish = micros();

		if(SerialUSB.available() > 0){
      
			cmd_code = command_instructions(SerialUSB.read(), &number_of_motors, motors_active);
			
			switch(cmd_code){
				case 0:
					device_address = setup_actuators(&Motor1, &Motor2, &Motor3, &Motor4, number_of_motors, motors_active);
					reply_code = 0;
					break;
				case 1:
					device_address = write_torques(&Motor1, &Motor2, &Motor3, &Motor4, number_of_motors, motors_active);
					reply_code = 1;
					break;
				default:
					break; 
			}
		}
		else{

			switch(reply_code){
				case 0:
					reply_code = 3;
					break;
				case 1:
					read_encoders(&Motor1, &Motor2, &Motor3, &Motor4, number_of_motors, device_address, motors_active);
					reply_code = 3;
					break;
				default:
					break; 
			} 
		}
	}
}



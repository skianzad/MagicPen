/**
 ***********************************************************************************************
 * @file       Haply_Arduino_Control.h
 * @author     Steve Ding, Colin Gallacher
 * @version    V0.1.0
 * @date       27-February-2017
 * @brief      constants and helper functions actuator control
 ***********************************************************************************************
 * @attention
 *
 *
 ***********************************************************************************************
 */


/* Data length definitons **********************************************************************/

/* maximim number of actuators available on board for control */
#define TOTAL_ACTUATORS         4 

/* number of control parameters per actuator */
#define ACTUATOR_PARAMETERS     2 
/* Encoder pin definitions **********************************************************************/

#define Lft								4
#define Rht 							5
#define Up 								2
#define Dwn 							3
int x_position =0;
int y_position=0;


  void Right() {
  x_position= ++x_position;
}
void Left() {
  x_position= --x_position;
}
void Upa() {
  y_position= ++y_position;
}
void Down() {
  y_position= --y_position;
}
/* Encoder pin definitions *********************************************************************/
#define ENCPIN1_1   			      28 // J2
#define ENCPIN1_2   			      29

#define ENCPIN2_1   			      24 // J3
#define ENCPIN2_2   			      25

#define ENCPIN3_1   			      36 // J4
#define ENCPIN3_2   			      37  

#define ENCPIN4_1   			      32 // J5
#define ENCPIN4_2   			      33 

/* PWM definitions block ***********************************************************************/
#define PWMPIN1					        9
#define DIRPIN1					        26

#define PWMPIN2					        8
#define DIRPIN2					        22

#define PWMPIN3					        6
#define DIRPIN3					        34

#define PWMPIN4					        7
#define DIRPIN4					        30

#define PWMFREQ					        40000


/* Actuator struct definitions *****************************************************************/
typedef struct motor{
	float Enc_offset;
	float Enc_resolution;

	int pwmPin;
	int dirPin;
	
	Encoder *Enc;
}actuator;


/* Receive function definitions ****************************************************************/
byte command_instructions(byte control, int *number, byte active[]);
byte receive_parameters(byte a1[], byte a2[], byte a3[], byte a4[], int number, byte actuators[]);
byte receive_torques(float *t1, float *t2, float *t3, float *t4, int number, byte actuators[]);


/* Send function definitions *******************************************************************/
void send_reply(byte device_address, byte motors_active[]);
void send_encoders_data(float a1, float a2, float a3, float a4, int number, byte device_address, byte actuators[]);


/* Device control function definitions *********************************************************/
byte setup_actuators(actuator *m1, actuator *m2, actuator *m3, actuator *m4, int number, byte active[]);
void initialize_actuator(actuator *mtr, byte parameters[], int pwm, int dir, int enc1, int enc2);

byte write_torques(actuator *m1, actuator *m2, actuator *m3, actuator *m4, int number, byte actuators[]);
void create_torque(actuator *mtr, float torque);

void read_encoders(actuator *m1, actuator *m2, actuator *m3, actuator *m4, int number, byte address, byte actuators[]);
float read_encoder(actuator *mtr);


/* Helper function definitions *****************************************************************/
void FloatToBytes(float val, byte segments[]);
float BytesToFloat(byte segments[]);
void ArrayCopy(byte src[], int src_index, byte dest[], int dest_index, int len );



/* Receive functions ***************************************************************************/
/**
 * @brief    Decypher command instructions
 * @note     updates, motors_active, number_of_motors, and cmd_code
 * @param    control: input header byte to be parsed
 * @param	 number: number of motors value to be manipulated
 * @param    motors_active: active motors array indicator
 * @return   command code indicating communication type 
 */
byte command_instructions(byte control, int *number, byte active[]){
  
  int j = 0;
  for(int i = 0; i < TOTAL_ACTUATORS; i++){
    
    active[i] = control &0x01;
    control = control >> 1;

    if(active[i] > 0){
      j++;
    }
  }

  *number = j;
  return control;
}


/**
 * @brief    Parses and receives initial encoder values 
 * @note     Will log active actuators for use
 * @param    a1: encoder 1 setup value
 * @param    a2: encoder 2 setup value
 * @param    a3: encoder 3 setup value
 * @param    a4: encoder 4 setup value
 * @param    number: number of motors active
 * @param    actuators: active actuator positions
 * @return   device_address 
 */
byte receive_parameters(byte a1[], byte a2[], byte a3[], byte a4[], int number, byte actuators[]){

	/* Determine incoming setup parameters datalength */
	int data_length = number * 4 * ACTUATOR_PARAMETERS + 1;

	/* Incoming parameters array */ 
	byte actuator_parameters[data_length];
  
	SerialUSB.readBytes(actuator_parameters, data_length);
	
	int j = 1;
	/* Cycle through all possible actuators and activate relevant actuators */
	for(int i = 0; i < TOTAL_ACTUATORS; i++){
      
		if(actuators[i] > 0){
      
			switch (i){
				case 0:
					ArrayCopy(actuator_parameters, j, a1, 0, 4*ACTUATOR_PARAMETERS);
					j = j + 4 * ACTUATOR_PARAMETERS;
					break;
				case 1:
					ArrayCopy(actuator_parameters, j, a2, 0, 4*ACTUATOR_PARAMETERS); 
					j = j + 4 * ACTUATOR_PARAMETERS;
					break;
				case 2:
					ArrayCopy(actuator_parameters, j, a3, 0, 4*ACTUATOR_PARAMETERS);
					j = j + 4 * ACTUATOR_PARAMETERS;
					break;
				case 3:
					ArrayCopy(actuator_parameters, j, a4, 0, 4*ACTUATOR_PARAMETERS);
					break;
			}	
		}  
	} 
	
	return actuator_parameters[0];	
}


/**
 * @brief    Parses and recieves torque values from simulation 
 * @note     Will log active actuators for use
 * @param    t1: torque1 value to be extracted
 * @param    t2: torque1 value to be extracted
 * @param    t3: torque1 value to be extracted
 * @param    t4: torque1 value to be extracted
 * @param    number: number of motors active
 * @param    actuators: active actuator positions
 * @return   device address 
 */
byte receive_torques(float *t1, float *t2, float *t3, float *t4, int number, byte actuators[]){

	int data_length = number * 4 + 1;;

	byte segments[4]; 
	byte torque_values[data_length];
	SerialUSB.readBytes(torque_values, data_length);
	
	int j = 1;

	for(int i = 0; i < TOTAL_ACTUATORS; i++){
    
		if(actuators[i] > 0){
			switch(i){
				case 0:
					ArrayCopy(torque_values, j, segments, 0, 4);
					*t1 = BytesToFloat(segments);
					j = j + 4;
					break;
         		case 1:
					ArrayCopy(torque_values, j, segments, 0, 4);
					*t2 = BytesToFloat(segments);
					j = j + 4;
					break;
				case 2:
					ArrayCopy(torque_values, j, segments, 0, 4);
					*t3 = BytesToFloat(segments);
					j = j + 4;
					break;
				case 3:
					ArrayCopy(torque_values, j, segments, 0, 4);
					*t4 = BytesToFloat(segments);
					break; 
			} 
		}
	}
	
	return torque_values[0];
}



/* Send functions ******************************************************************************/
/**
 * @brief    Formats and send verification reply after setup
 * @note     response to setup command
 * @param    device_address: address of device that setup board
 * @param    motors_active: number of motors currently in active state
 * @return   None 
 */
void send_reply(byte device_address, byte motors_active[]){
	
	byte outData[5];
	
	outData[0] = device_address;
	ArrayCopy(motors_active, 0, outData, 1, 4);

	SerialUSB.write(outData, 5);
}


/**
 * @brief    Formats and sends encoder values over Serial
 * @note     Will only send encoder values of active actuators
 * @param    a1: encoder 1 value
 * @param    a2: encoder 2 value
 * @param    a3: encoder 3 value
 * @param    a4: encoder 4 value
 * @param    number: number of motors active
 * @param    actuators: active actuator positions
 * @param	 device_address: address of device that requested data
 * @return   None 
 */
void send_encoders_data(float a1, float a2, float a3, float a4, int number, byte device_address, byte actuators[]){

	byte segments[4];
	byte outData[number*4+1];
	
	outData[0] = device_address;
	int j = 1;
  float b1 ;
  float b2 ;
	for(int i = 0; i < TOTAL_ACTUATORS; i++){
     
		if(actuators[i] > 0){

			switch(i){
				case 0:
					b1=(float)x_position;
					FloatToBytes(b1, segments);
					ArrayCopy(segments, 0, outData, j, 4);
					j = j + 4;
					break;
				case 1:
					b2=(float)y_position;
					FloatToBytes(b2, segments);
					ArrayCopy(segments, 0, outData, j, 4);
					j = j + 4;
					break;
				case 2:
					FloatToBytes(a3, segments);
					ArrayCopy(segments, 0, outData, j, 4);
					j = j + 4;
					break;
				case 3:
					FloatToBytes(a4, segments);
					ArrayCopy(segments, 0, outData, j, 4);
					break;
			}   
		}
   }

   SerialUSB.write(outData, number*4+1);
}



/* Device control functions ********************************************************************/
/**
 * @brief    Sets up actuators that are to be used based on initial activation command
 * @note     Function calls subsequent functions which individually sets up each actuator
 * @param    m1: actuator1 struct
 * @param    m2: actuator2 struct
 * @param	 m3: actuator3 struct
 * @param 	 m4: actuator4 struct
 * @param	 number: number of motors active
 * @param	 actuators: positions of motors active
 * @return   device_address: address of device sending setup data
 */
byte setup_actuators(actuator *m1, actuator *m2, actuator *m3, actuator *m4, int number, byte actuators[]){
	
	/* address for device */
	byte address;
	
	/* set pwm resolution to 12-bits */
	pwm_set_resolution(12);
	
	/* declare parameter array for each actuator */
	byte a1[4*ACTUATOR_PARAMETERS];
	byte a2[4*ACTUATOR_PARAMETERS];
	byte a3[4*ACTUATOR_PARAMETERS];
	byte a4[4*ACTUATOR_PARAMETERS];
	
	address = receive_parameters(a1, a2, a3, a4, number, actuators);
	
	for(int i = 0; i < TOTAL_ACTUATORS; i++){
		
		if(actuators[i] > 0){
			switch(i){
				case 0:
					initialize_actuator(m1, a1, PWMPIN1, DIRPIN1, ENCPIN1_1, ENCPIN1_2);
					break;
				case 1:
					initialize_actuator(m2, a2, PWMPIN2, DIRPIN2, ENCPIN2_1, ENCPIN2_2);
					break;
				case 2:
					initialize_actuator(m3, a3, PWMPIN3, DIRPIN3, ENCPIN3_1, ENCPIN3_2);
					break;
				case 3:
					initialize_actuator(m4, a4, PWMPIN4, DIRPIN4, ENCPIN4_1, ENCPIN4_2);
					break;
			}
		}
	}
	
	return address;
}


/**
 * @brief    Initialize an actuator and a corresponding Encoder for use 
 * @note     Currently under prototype
 * @param    *mtr: pointer to actuator struct for parameters access
 * @param    parameters[]: actuator input parameters for one actuator
 * @param    pwm: pin for PWM control
 * @param    dir: pin for direction control
 * @return   none
 */
 void initialize_actuator(actuator *mtr, byte parameters[], int pwm, int dir, int enc1, int enc2){
 
	int i = 0;
	byte actuator_value[4];
	
	mtr->pwmPin = pwm;
	mtr->dirPin = dir;
	
	pinMode(pwm, OUTPUT);
	pinMode(dir, OUTPUT);
	pwm_setup(pwm, PWMFREQ, 1);
	
	mtr->Enc = new Encoder(enc1, enc2);
	
	ArrayCopy(parameters, i, actuator_value, 0, 4);
	mtr->Enc_offset = BytesToFloat(actuator_value);
	i = i + 4;
	
	ArrayCopy(parameters, i, actuator_value, 0, 4);
	mtr->Enc_resolution = BytesToFloat(actuator_value);
	
	mtr->Enc->write(mtr->Enc_offset * mtr->Enc_resolution / 360);
 }

 
 /**
 * @brief    Write torque to be generated to motors 
 * @note     Will only write to active actuators
 * @param    m1: actuator1 struct
 * @param    m2: actuator2 struct
 * @param	 m3: actuator3 struct
 * @param 	 m4: actuator4 struct
 * @param	 number: number of motors active
 * @param	 actuators: positions of motors active
 * @return   device_address: address of device sending torque request
 */
 byte write_torques(actuator *m1, actuator *m2, actuator *m3, actuator *m4, int number, byte actuators[]){
	
	byte address;
	
	float torque1, torque2, torque3, torque4;
	
	address = receive_torques(&torque1, &torque2, &torque3, &torque4, number, actuators);
	
	for(int i = 0; i < TOTAL_ACTUATORS; i++){
		
		if(actuators[i] > 0){
			
			switch(i){
				case 0:
					create_torque(m1, torque1);
					break;
				case 1:
					create_torque(m2, torque2);
					break;
				case 2:
					create_torque(m3, torque3);
					break;
				case 3:
					create_torque(m4, torque4);
					break;
			}
		}
	}
	
	return address;
 }

 
/**
 * @brief    read a torque at the stated actuator
 * @note     Currently under prototype
 * @param    *mtr: pointer to actuator struct for parameters access
 * @param    torque: torque to be created
 * @return   None
 */
void create_torque(actuator *mtr, float torque){

	int duty;
  
	if(torque <= 0){
		digitalWrite(mtr->dirPin, HIGH);
	}
	else{
		digitalWrite(mtr->dirPin, LOW);
	}
	
	

	torque = abs(torque);

	if(torque > 1){
		torque = 1;
	}

	duty = 4095 * torque;
	
	pwm_write_duty(mtr->pwmPin, duty);
} 


/**
 * @brief    Determine current angle seen by encoders and send data 
 * @note     Will only read active actuator encoder values
 * @param    None
 * @return   None 
 */
void read_encoders(actuator *m1, actuator *m2, actuator *m3, actuator *m4, int number, byte address, byte actuators[]){
	
	float encoder1, encoder2, encoder3, encoder4;
	
	for(int i = 0; i < TOTAL_ACTUATORS; i++){
		
		if(actuators[i] > 0){
			
			switch(i){
				case 0:
					encoder1 = read_encoder(m1);
					break;
				case 1:
					encoder2 = read_encoder(m2);
					break;
				case 2:
					encoder3 = read_encoder(m3);
					break;
				case 3:
					encoder4 = read_encoder(m4);
					break;
			}
		}	
	}
	
	send_encoders_data(encoder1, encoder2, encoder3, encoder4, number, address, actuators);
 }

/**
 * @brief    read an individual encoder and parse data for byte transmission
 * @note     Currently under prototype
 * @param    *mtr: pointer to actuator struct for parameters access
 * @param    &Enc: Encoder object reference 
 * @return   th_degrees: angle detected by encoder
 */
float read_encoder(actuator *mtr){

	float th_degrees;
	th_degrees = 360.0 * mtr->Enc->read()/mtr->Enc_resolution;

	return th_degrees;
}
 
 
 
/* Helper functions ****************************************************************************/

/**
 * Union definition for floating point and integer representation conversion
 */
typedef union{
	long val_l;
	float val_f;
} ufloat;

/**
 * @brief    Translates a 32-bit floating point into an array of four bytes
 * @note     None
 * @param    val: 32-bit floating point
 * @param    segments: array of four bytes
 * @return   None 
 */
void FloatToBytes(float val, byte segments[]){
	ufloat temp;

	temp.val_f = val;

	segments[3] = (byte)((temp.val_l >> 24) & 0xff);
	segments[2] = (byte)((temp.val_l >> 16) & 0xff);
	segments[1] = (byte)((temp.val_l >> 8) & 0xff);
	segments[0] = (byte)((temp.val_l) & 0xff);
}


/**
 * @brief    Translates an array of four bytes into a floating point
 * @note     None
 * @param    segment: the input array of four bytes
 * @return   Translated 32-bit floating point 
 */
float BytesToFloat(byte segments[]){
	ufloat temp;

	temp.val_l = (temp.val_l | (segments[3] & 0xff)) << 8;
	temp.val_l = (temp.val_l | (segments[2] & 0xff)) << 8;
	temp.val_l = (temp.val_l | (segments[1] & 0xff)) << 8;
	temp.val_l = (temp.val_l | (segments[0] & 0xff)); 

	return temp.val_f;
}


/**
 * @brief    Copies elements from one array to another
 * @note     None
 * @param    src: The source array to be copied from
 * @param    src_index: The starting index of the source array
 * @param    dest: The destination array to be copied to
 * @param    dest_index: The starting index of the destination array
 * @param    len: Number of elements to be copied
 * @return   None 
 */
void ArrayCopy(byte src[], int src_index, byte dest[], int dest_index, int len ){
	for(int i = 0; i < len; i++){
		dest[dest_index + i] = src[src_index + i];
	}
}



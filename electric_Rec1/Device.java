/**
 **********************************************************************************************************************
 * @file       Device.java
 * @author     
 * @version    V0.1.0
 * @date       01-March-2017
 * @brief      Device class definition
 **********************************************************************************************************************
 * @attention
 *
 *
 **********************************************************************************************************************
 */
 
public class Device{

	public    DeviceType       device_type;
	public 	  byte 			       deviceID;
	
	public    Actuator[]    	 motors;	
	public    Sensor[]		     encoders;

	public 	  Board 	      	 deviceLink;
	public 	  Mechanisms 		   mechanisms;
	
	public    byte[] 			     actuator_positions   = {0, 0, 0, 0};
	public 	  byte[]			     encoder_positions    = {0, 0, 0, 0};
	private   byte 			       communicationType;
 	private   float[]   		   params;
	

  /**
   * Constructs a Device of the specified <code>DeviceType</code>, with the defined <code>deviceID</code>, 
   * connected on the specified <code>Board</code>
   *
   * @param    device_type the degrees of freedom type of device to be implemented
   * @param    deviceID ID 
   * @param    deviceLink: serial link used by device
   */
	public Device(DeviceType device_type, byte deviceID, Board deviceLink){
		this.device_type = device_type;
		this.deviceID = deviceID;
		this.deviceLink = deviceLink;
		
		switch(device_type){
  
	
			case HaplyTwoDOF:
				motors = new Actuator[2];
				encoders = new Sensor[2];
        mechanisms = new HaplyTwoDoFMech(); 
        device_component_auto_setup(); 
        params = new float[2];
				break;
     
			default:
				System.err.println("Error: Undefined device type!");
				break;
		}

   this.device_set_parameters();
	}
	

  /**
   * Automatic setup of actuators and encoders based on setup parameters
   */   
  private void device_component_auto_setup(){
     
      for(int i = 0; i < motors.length; i++){
        motors[i] = new Actuator();
      this.set_actuator_parameters(i+1, i+1);
         }
         
      for(int i = 0; i < encoders.length; i++){
        encoders[i] = new Sensor();
    
       this.set_encoder_parameters(i+1, (i+1)*180, 13824, i+1); 
    }
   }
   
   
  /**
   * Set the indicated actuator to use the specified motor port
   *
   * @param    actuator index of actuator that needs parameter to be set or updated
   * @param    port specified motor port to be used (motor ports 1-4 on the Haply board) 
   */
	public void set_actuator_parameters(int actuator, int port){
		
		if(port <=0 || port > 4){
			System.err.println("error: actuator position index out of bounds!");
		}
		else{
			switch(actuator){
  
				case 1:
					motors[0].set_port(port);
					actuator_assignment(actuator, motors[0]);
					break;
				case 2:
					motors[1].set_port(port);
					actuator_assignment(actuator, motors[1]);
					break;
				case 3:
					motors[2].set_port(port);
					actuator_assignment(actuator, motors[2]);
					break;
				case 4:
					motors[3].set_port(port);
					actuator_assignment(actuator, motors[3]);
					break;
				default:
					System.err.println("error: actuator index out of bound! refer to limit of constructed device");
					break;
			}
		}
	}

	
  /**
   * Set the indicated sensor (encoder) to use the initial offset, resolution, on the specified port
   *
   * @param    sensor index of sensor encoder that needs parameters to be set or updated
   * @param    offset initial offset in degrees that the encoder sensor should be initialized at
   * @param    resolution step resolution of the encoder sensor
   * @param    port specific motor port the encoder sensor is connect at (usually same as actuator)
   */
	public void set_encoder_parameters(int sensor, float offset, float resolution, int port){
		
		if(port <=0 || port > 4){
			System.err.println("error: encoder position index out of bounds!");
		}
		else{
			switch(sensor){
  
				case 1:
					encoders[0].set_offset(offset);
					encoders[0].set_resolution(resolution);
					encoders[0].set_port(port);
					encoder_assignment(sensor, encoders[0]);
					break;
				case 2:
					encoders[1].set_offset(offset);
					encoders[1].set_resolution(resolution);
					encoders[1].set_port(port);
					encoder_assignment(sensor, encoders[1]);
					break;
				case 3:
					encoders[2].set_offset(offset);
					encoders[2].set_resolution(resolution);
					encoders[2].set_port(port);
					encoder_assignment(sensor, encoders[2]);
					break;
				case 4:
					encoders[3].set_offset(offset);
					encoders[3].set_resolution(resolution);
					encoders[3].set_port(port);
					encoder_assignment(sensor, encoders[3]);
					break;
				default:
					System.err.println("error: actuator index out of bound! refer to limit of constructed device");
					break;
			}
		}
	}
	

  /**
   * Replaces the current Mechanisms that is being used with the specified Mechanisms
   *
   * @param    mechanisms new Mechanisms to replace the initialized or old Mechanisms currently in use
   */
	public void set_new_mechanism(Mechanisms mechanisms){
		this.mechanisms = mechanisms;
	}
  

  /**
   * Sets or updates device function parameters and loads frequency and amplitude vaues into params[]
   * (note* Hapkit specific function)
   *
   * @param    function device function to be carried out
   * @param    frequency frequency variable to be updated
   * @param    amplitude amplitude variable to be updated
   */
  public void set_parameters(byte function, float frequency, float amplitude){
    deviceID = function;
    params[0] = frequency;
    params[1] = amplitude;
  }
  
	
  /**
   * Gathers all encoder sensor setup inforamation of all encoder sensors that are initialized and 
   * sequentialy formats the data based on specified sensor index positions to send over serial port
   * interface for hardware device initialization
   */
	public void device_set_parameters(){
  
		communicationType = 0;
		float[] parameter_data = new float[2*encoders.length];
    
    
		int j = 0;
		for(int i = 0; i < encoder_positions.length; i++){
      
			if(actuator_positions[i] > 0){
				parameter_data[2*j] = encoders[actuator_positions[i]-1].get_offset();
				parameter_data[2*j+1] = encoders[actuator_positions[i]-1].get_resolution();
				j++;
			}
		}

		deviceLink.transmit(communicationType, deviceID, actuator_positions, parameter_data);	
	}
	
	
  /**
   * hardware setup verification function (currently not used)
   */
	public void device_set_verification(){
		
		communicationType = 0;
    
		if(deviceLink.data_available()){
			float[] recieve = deviceLink.receive(communicationType, deviceID, actuator_positions);
		}
	}
	
	
  /**
   * Requests encoder angle data from the hardware based on the initialized setup. function also
   * sends a torque output command of zero torque for each actuator in use
   */
	public void device_read_request(){
    communicationType = 1;
		
		float[] encoder_request = new float[motors.length];

    	int j = 0;
    	for(int i = 0; i < encoder_positions.length; i++){
      
      		if(actuator_positions[i] > 0){
        		encoder_request[j] = 0;
        		j++;
      		}
    	}
		
    	deviceLink.transmit(communicationType, deviceID, actuator_positions, encoder_request);
	}
	
	
  /**
   * Transmits specific torques that has been calculated and stored for each actuator over the serial
   * port interface
   */
	public void device_write_torques(){
		
    communicationType = 1;
    
		float[] device_torques = new float[motors.length];
		
    	int j = 0;
    	for(int i = 0; i < actuator_positions.length; i++){
      		if(actuator_positions[i] > 0){
        		device_torques[j] = motors[actuator_positions[i]-1].get_torque();
        		j++;
      		}
    	}

    	deviceLink.transmit(communicationType, deviceID, actuator_positions, device_torques);		
	}
	

  /**
   * Transmits the contents of the params[] array over the serial port interface
   */
  public void send_data(){
    communicationType = 1;
    deviceLink.transmit(communicationType, deviceID, actuator_positions, params);
  }
	

  /**
   * Receives angle position inforamation from the serial port interface and updates each indexed encoder sensor
   * to their respective received angle
   */
	public void device_read_angles(){
		
    communicationType = 1;
    
		float[] angle_data = deviceLink.receive(communicationType, deviceID, encoder_positions);
		
    	int j = 0;
    	for(int i = 0; i < encoder_positions.length; i++){
      		if(encoder_positions[i] > 0){
        		encoders[actuator_positions[i]-1].set_angle(angle_data[j]);
        		j++;
      		}
    	}
	}
	 

  /**
   * Receives data from the serial port interface and updates parameters in mechanisms
   */
  public void receive_data(){
    communicationType = 1;
    float data[] = deviceLink.receive(communicationType, deviceID, actuator_positions);
    mechanisms.set_mechanism_parameters(data);
  }
	

  /**
   * assigns actuator positions based on actuator port
   */
	private void actuator_assignment(int actuator, Actuator m){
		
		switch(m.get_port()){
			case 1:
				this.actuator_positions[0] = (byte)actuator;
				break; 
			case 2:
				this.actuator_positions[1] = (byte)actuator;
				break;
			case 3:
				this.actuator_positions[2] = (byte)actuator;
				break;
			case 4:
				this.actuator_positions[3] = (byte)actuator;
				break;
			default:
				System.err.println("Error, actuator position out of bound");
				break;
		}
		
	}
	
	
  /**
   * assigns encoder positions based on encoder port
   */
	private void encoder_assignment(int encoder, Sensor m){
		
		switch(m.get_port()){
			case 1:
				this.encoder_positions[0] = (byte)encoder;
				break; 
			case 2:
				this.encoder_positions[1] = (byte)encoder;
				break;
			case 3:
				this.encoder_positions[2] = (byte)encoder;
				break;
			case 4:
				this.encoder_positions[3] = (byte)encoder;
				break;
			default:
				System.err.println("Error, actuator position out of bound");
				break;
		}
		
	}


  /**
   * Reads and update angles information from device hardware to encoders
   *
   * @returns    angles information received from device hardware
   */
  public float[] get_device_angles(){
     
    this.device_read_angles();
    float[] angles = new float[encoders.length];  
      
    for(int i=0; i<encoders.length; i++){
      angles[i] = this.encoders[i].get_angle();
    }
      
    return angles; 
  }


  /**
   * Reads and update angles information from device hardware to encoders and performs physics calculations
   *
   * @returns    end-effector coordinate position
   */
  public float[] get_device_position(){
      
    this.device_read_angles();
    float[] angles = new float[encoders.length];  
      
    for(int i=0; i<encoders.length; i++){
      angles[i] = this.encoders[i].get_angle();
    }
      
    this.mechanisms.forwardKinematics(angles);
    float[] end_effector_position=  this.mechanisms.get_coordinate();
      
    return end_effector_position; 
  }


  /**
   * Performs physics calculations based on the given angle values
   *
   * @param      angles angles to be used for physics position calculation
   * @returns    end-effector coordinate position
   */
  public float[] get_device_position(float[] angles){
        
    this.mechanisms.forwardKinematics(angles);
    float[] end_effector_position=  this.mechanisms.get_coordinate();
      
    return end_effector_position; 
  }


  /**
   * Calculates the needed output torques based on forces input and updates each initialized actuator
   * respectively
   *
   * @param     forces forces that need to be generated
   */
  public void set_device_torques(float[] forces){
    this.mechanisms.torqueCalculation(forces);
    float[] torques = this.mechanisms.get_torque();
    
    for(int i=0; i<motors.length; i++){
      this.motors[i].set_torque(torques[i]);
    }
  }
  
}
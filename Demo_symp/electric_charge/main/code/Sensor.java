/**
 **********************************************************************************************************************
 * @file       Sensor.java
 * @author     
 * @version    V0.1.0
 * @date       01-March-2017
 * @brief      Sensor class definition
 **********************************************************************************************************************
 * @attention
 *
 *
 **********************************************************************************************************************
 */
 
public class Sensor{
	
	private float   encoder_offset	      = 0;
	private float   encoder_resolution    = 0;
	private float   angle 			          = 0;
	private int     encoder_port	 	      = 0;
	

  /**
   * Constructs a Sensor set using motor port position one
   */
	public Sensor(){
		this(0, 0, 1);
	}
	

  /**
   * Constructs a Sensor with the given motor port position, to be initialized with the given angular offset,
   * at the specified step resoluiton
   *
   * @param    offset initial offset in degrees that the encoder sensor should be initialized at
   * @param    resolution step resolution of the encoder sensor
   * @param    port specific motor port the encoder sensor is connect at (usually same as actuator)
   */
	public Sensor(float offset, float resolution, int port){
		this.encoder_offset = offset;
		this.encoder_resolution = resolution;
		this.encoder_port = port;
	}
	

  /**
   * Set offset parameter of sensor
   *
   * @param    offset initial angular offset in degrees
   */
	public void set_offset(float offset){
		encoder_offset = offset;
	}
	

  /**
   * Set resolution parameter of sensor
   *
   * @param    resolution step resolution of encoder sensor
   */
	public void set_resolution(float resolution){
		encoder_resolution = resolution;
	}
	

  /**
   * Set motor port position to be used by sensor
   *
   * @param    port motor port position (motor port connection on Haply board)
   */
	public void set_port(int port){
		encoder_port = port;
	}


  /**
   * Set angle variable to the specified angle
   *
   * @param    angle angle value
   */	
	public void set_angle(float angle){
		this.angle = angle;
	}
	

  /**
   * @return    current offset parameter
   */
	public float get_offset(){
		return encoder_offset;
	}
	

  /**
   * @return    encoder resolution of encoder sensor being used
   */
	public float get_resolution(){
		return encoder_resolution;
	}
	

  /**
   * @return    current motor port position
   */
	public int get_port(){
		return encoder_port;
	}
	

  /**
   * @return    current angle information
   */
	public float get_angle(){
		return angle;
	}
	
}
/**
 **********************************************************************************************************************
 * @file       Actuator.java
 * @author     
 * @version    V0.1.0
 * @date       01-March-2017
 * @brief      Actuator class definition
 **********************************************************************************************************************
 * @attention
 *
 *
 **********************************************************************************************************************
 */
 
public class Actuator{
	
	private float   torque             = 0;
	private int     actuator_port      = 0;
	
  /**
   * Creates an Actuator using motor port position 1
   */
	public Actuator(){
		this(1);
	}
	
  /**
   * Creates an Actuator using the given motor port position
   *
   * @param    port motor port position for actuator
   */
	public Actuator(int port){
		this.actuator_port = port;
	}
	

  /**
   * Sets motor port position to be used by Actuator
   * 
   * @param   port motor port position 
   */  	
	public void set_port(int port){
		actuator_port = port;
	}
	

  /**
   * Sets torque variable to the given torque value
   *
   * @param   torque new torque value for update
   */
	public void set_torque(float torque){
		this.torque = torque;
	}
	

  /**
   * @return   current motor port position in use
   */
	public int get_port(){
		return actuator_port;
	}
	

  /**
   * @return   current torque information
   */
	public float get_torque(){
		return torque;
	}
	
}
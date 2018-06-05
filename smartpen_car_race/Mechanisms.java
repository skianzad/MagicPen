/**
 **********************************************************************************************************************
 * @file       Mechanisms.java
 * @author     
 * @version    V0.1.0
 * @date       01-March-2017
 * @brief      Mechanisms abstract class designed for use as a template. Current blasses which extends the Mechanisms
 *             class includes:
 *                - HapticPaddle
 *                - HaplyOneDoFMech
 *                - HaplyTwoDoFMech/NewExampleMech
 *                - HaplyThreeDoFMech
 **********************************************************************************************************************
 * @attention
 *
 *
 **********************************************************************************************************************
 */

import static java.lang.Math.*;

public abstract class Mechanisms{
		
  /**
   * Performs the forward kinematics physics calculation of a specific physical mechanism
   *
   * @param    angles angular inpujts of physical mechanisms (array element length based
   *           on the degree of freedom of the mechanism in question)
   */
	public abstract void forwardKinematics(float[] angles);
	

  /**
   * Performs torque calculations that actuators need to output
   *
   * @param    force force values calculated from physics simulation that needs to be conteracted 
   *           
   */
	public abstract void torqueCalculation(float[] forces);

  public abstract float getTau1();
  
    public abstract float getTau2();
  
  /**
   * Performs force calculations
   */
	public abstract void forceCalculation();
	

  /**
   * Performs calculations for position control
   */
	public abstract void positionControl();
	

  /**
   * Performs inverse kinematics calculations
   */
	public abstract void inverseKinematics();
	
	
  /**
   * Initializes or changes mechanisms parameters
   *
   * @param    parameters mechanism parameters 
   */
	public abstract void set_mechanism_parameters(float[] parameters);
	

  /**
   * @return   end-effector coordinate position
   */
	public abstract float[] get_coordinate();

  /**
   * @return   torque values from physics calculations
   */	
	public abstract float[] get_torque();
	

  /**
   * @return   angle values from physics calculations
   */
	public abstract float[] get_angle();
	

}

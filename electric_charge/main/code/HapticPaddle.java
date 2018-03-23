import static java.lang.Math.*;

public class HapticPaddle extends Mechanisms{
 
  private float     rh       = 0.075f; // length of handle in m
  
  private float     angle;
  private float     torque; 
  private float     xh       = 0.0f;
   
  public HapticPaddle(){
  }
  
  public void forwardKinematics(float[] angles){
    xh = rh*angles[0];
  }
  
  public void torqueCalculation(float[] force){
  }
  
  public void forceCalculation(){
  }
  
  public void positionControl(){
  }
  
  public void inverseKinematics(){
  }
  
  
  public void set_mechanism_parameters(float[] parameters){
    angle = parameters[0]; 
    torque = parameters[1]; 
    
  }
  
  public float[] get_coordinate(){
    float temp[] = {angle};
    this.forwardKinematics(temp);
    
    float temp1[] = {xh};
        return temp1;
  }
  
  public float[] get_torque(){
         float temp[] = {torque};
        return temp;
  }
  
  public float[] get_angle(){
    float temp[] = {angle};
        return temp;
  }

}
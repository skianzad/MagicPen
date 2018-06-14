import processing.serial.*;

public class Dot {
  
  int x; //x-pos in screen coords
  int y; //y-pos in screen coords
  boolean offScreen;
  static final int scaling_factor = 1; 
  boolean type; //type is true if it the tau represented is tau1, false if tau2. Reminder: tau1 is horizontal force, tau2 is vertical force. 
  //bottom graph is vertical torque (type is false) side graph is type true
  
  public Dot(int x, int y, boolean type) {
    this.x = x;
    this.y = y;
    this.type = type;
    offScreen = false;
  }
  

  
  /* increase the x-coord by 1, if the dot is on the screen. If the dot is off the screen, then set offScreen to true */
  public void update(int screenWidth) {
    if (this.x > screenWidth) {
      offScreen = true;
    }
    else {
      if (type) {
        y--;
      }
      else {
        x++;
      }
    }
    
    

  }
    
    
  }
    
  
  

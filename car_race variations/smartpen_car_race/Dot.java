import processing.serial.*;

public class Dot {
  
  int x;
  int y;
  boolean offScreen;
  static final int scaling_factor = 1;
  boolean type; //type is true if it the tau represented is tau1, false if tau2. Reminder: tau1 is horizontal force, tau2 is vertical force.
  
  public Dot(int x, int y, boolean type) {
    this.x = x;
    this.y = y;
    this.type = type;
    offScreen = false;
  }
  

  
  /* increase the x-coord by 1, if the dot is on the screen. If the dot is off the screen, then set offScreen to true */
  public void update() {
    if (this.x > 1000) {
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
    
  
  

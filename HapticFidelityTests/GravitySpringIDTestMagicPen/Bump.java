import processing.core.PVector;

public class Bump { //as if it were two ramps side by side

  PVector position; //in scree coordinates (not Fisica coordinates)
  float rampWidth;
  float rampLength; // bump's actual length is twice this number
  float constant; //this is the constant that determines the force on the pen due to the bump.
  
  PVector upLeft; 
  PVector upRight;
  PVector lowLeft;
  PVector lowRight;
  
  
  public Bump(PVector position, float rampWidth, float rampLength) {
     this.position = position;
     this.rampWidth = rampWidth;
     this.rampLength = rampLength;
     constant = 2;
     upLeft = new PVector(position.x-rampWidth/2, position.y-rampLength);
     upRight = new PVector(position.x+rampWidth/2, position.y-rampLength);
     lowLeft = new PVector(position.x-rampWidth/2, position.y+rampLength);
     lowRight = new PVector(position.x+rampWidth/2, position.y+rampLength);
  }
  
  
}

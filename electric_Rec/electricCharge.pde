class ElectricCharge{

  int inner_radius;
  int c_radius;
  int x_pos; //what are the units?
  int y_pos;
  int sign;
  int q;
  int colour;
  
  FCircle body; //fisica body attached to the charge
  
  ElectricCharge(int tmpInnerRadius, int tmpCRadius, int tmpX, int tmpY, int tmpSign, FCircle body){
    inner_radius = tmpInnerRadius;
    c_radius = tmpCRadius;
    x_pos = tmpX;
    y_pos = tmpY;
    sign = tmpSign;
    this.body = body;
    
    if(tmpSign == 1) {
    //positive:
    colour = #FF0000;
    q =50;
    } else {
    //negative:
    colour = #0070FF;
    q = -50;
    }
  }
  
  public boolean equals(ElectricCharge other) {
     boolean b = (other != null) &&
                 this.getClass() == other.getClass() &&
                 this.inner_radius == other.inner_radius && 
                 this.c_radius == other.c_radius &&
                 this.x_pos == other.x_pos &&
                 this.y_pos == other.y_pos &&
                 this.sign == other.sign &&
                 this.q == other.q &&
                 this.colour == other.colour;
     return b;
                 
  }
  
  
}

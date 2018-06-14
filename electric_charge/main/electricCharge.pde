class ElectricCharge{

  int inner_radius;
  int c_radius;
  int x_pos;
  int y_pos;
  int sign;
  int q;
  int colour;
  
  ElectricCharge(int tmpInnerRadius, int tmpCRadius, int tmpX, int tmpY, int tmpSign){
    inner_radius = tmpInnerRadius;
    c_radius = tmpCRadius;
    x_pos = tmpX;
    y_pos = tmpY;
    sign = tmpSign;
    
    if(tmpSign == 1) {
    //positive:
    colour = #FF0000;
    q = 120;
    } else {
    //negative:
    colour = #0070FF;
    q = -120;
    }
  }
  
  
}

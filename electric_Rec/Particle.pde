class Particle {

  float ll = 1;
  float deltax, deltay;
  
  PVector loc;
  
ArrayList <PVector> centers = new ArrayList <PVector> ();
 
  Particle() {
    loc = new PVector(random(width), random(height));
    
  }
 
  void run() {
    
    if (loc.x > width || loc.x < 0 || loc.y > height || loc.y < 0) {
      loc = new PVector(random(width), random(height));
    } else {
      if (centers.size() != 0){
      loc.add(getDirection(loc));
      }
      //point(loc.x, loc.y);
      ellipse(loc.x, loc.y, 1, 1);
    }
  }
 
  void addCenter (float x, float y, int sign) {
    
  PVector new_center = new PVector(x,y, sign);
  centers.add(new_center);
  
  }
 
  PVector getDirection(PVector p) {
    
    ArrayList <PVector> effects = new ArrayList<PVector>();
    float total_ex = 0;
    float total_ey = 0;
    float total_e  = 0;
    
    for (PVector c : centers) {
    
    float dx = p.x - c.x;
    float dy = p.y - c.y;
    float d  = sqrt(dx*dx + dy*dy);
    
    //sign
    float E;
    if (c.z == 1) {
    E = qp/(d*d);
    } else {
    E = qn/(d*d);
    }
    
    float Ex = dx*E/d;
    float Ey = dy*E/d;
    
    PVector effect = new PVector(Ex, Ey);
    effects.add(effect);
      
    }
    
    for (PVector e : effects){
    
      total_ex += e.x;
      total_ey += e.y;
    
    }
    
    total_e = sqrt(total_ex * total_ex + total_ey * total_ey);
    
    deltax=ll * total_ex/total_e;
    deltay=ll * total_ey/total_e;
   
    return new PVector(deltax, deltay);
  }
}

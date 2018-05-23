void addMass(){

 poly = new FPoly();
 poly.setStrokeWeight(3);
 poly.setFill(120, 30, 90);
 poly.setBullet(false);
 poly.setDensity(1.05);
 poly.setRotatable(false);
 poly.setName("Mass");
 poly.setRestitution(0.1);
 for (int i = 0; i < tst.getVertexCount(); i++) {
     PVector v = tst.getVertex(i);
     poly.vertex(v.x,v.y);
}
TouchBody=poly.getTouching();
if(TouchBody!=null){ 
println("Touching bodies",TouchBody);
}
tst.endShape();
tst=createShape();
tst.beginShape();
if (poly!=null) {
   world.add(poly);
   poly = null;
  }
}
     
void addcharge(){

 poly = new FPoly();
 poly.setStrokeWeight(3);
 poly.setStaticBody(true);
  poly.setFill(255, 255, 255);
 poly.setDensity(1);
 poly.setRestitution(0.5);
 for (int i = 0; i < tst.getVertexCount(); i++) {
     PVector v = tst.getVertex(i);
     poly.vertex(v.x,v.y);
}
tst.endShape();
 tst=createShape();
 tst.beginShape();
  if (poly!=null) {
     world.add(poly);
     poly = null;
      }
     }
//**********************************************************************     
void addSpring1(){
int verc=tst.getVertexCount();
FBody[] steps = new FBody[floor(verc/10)];
//**************Making the parts of the spring*************
for (int i=0; i<steps.length; i++) {
  PVector v = tst.getVertex(i*10);
  steps[i] = new FBox(boxWidth, 2);
  steps[i].setPosition(v.x,v.y);
  steps[i].setNoStroke();
  steps[i].setGroupIndex(1);
  //steps[i].setStaticBody(true);
  steps[i].setFill(120, 200, 190);
  world.add(steps[i]);
}
//**************Making the hanging point 1*************
FCircle hang = new FCircle(10);  
hang.setStatic(true);
hang.setPosition(tst.getVertex(0).x,tst.getVertex(0).y-10);
hang.setDrawable(true);
hang.setGroupIndex(1);
hang.setBullet(true);
world.add(hang);
//**************connecting the first part of spring to the *************
FDistanceJoint juntaPrincipio = new FDistanceJoint(steps[0], hang);
juntaPrincipio.setAnchor1(-boxWidth/2, 0);
juntaPrincipio.setAnchor2(0, 0);
juntaPrincipio.setFrequency(frequency);
juntaPrincipio.setDamping(damping);
juntaPrincipio.calculateLength();
juntaPrincipio.setFill(0);
juntaPrincipio.setStrokeWeight(5);
//juntaPrincipio.setGroupIndex(1);
world.add(juntaPrincipio);  

//**************connecting the the sequences of spring together *************

for (int i=1; i<steps.length; i++) {
    FDistanceJoint junta = new FDistanceJoint(steps[i-1], steps[i]);
    junta.setAnchor1(boxWidth/2, 0);
    junta.setAnchor2(-boxWidth/2, 0);
    junta.setFrequency(frequency);
    junta.setDamping(damping);
    junta.setFill(1);
    junta.setStrokeWeight(5);
    junta.setNoFill();
    junta.calculateLength();
    //junta.setGroupIndex(1);
    world.add(junta);
  }
//**************connecting different points of spring to the hanger 1 *************

    for (int i=0; i<steps.length; i++) {
    FDistanceJoint junta = new FDistanceJoint(hang, steps[i]);
    junta.setAnchor1(boxWidth/2, 0);
    junta.setAnchor2(-boxWidth/2, 0);
    junta.setFrequency(frequency);
    junta.setDamping(damping);
    junta.setFill(0);
    junta.setDrawable(false);
    junta.calculateLength();
    //junta.setGroupIndex(1);
    world.add(junta);
  }
  //**************Creating hanger 2 and connecting different points of spring to the hanger 1 *************

  FCircle hanginv = new FCircle(10);
  hanginv.setStatic(true);
  hanginv.setPosition(tst.getVertex(0).x+30,tst.getVertex(0).y);
  hanginv.setDrawable(true);
  hanginv.setDensity(1);
  hanginv.setGroupIndex(1);

  world.add(hanginv);
  
  for (int i=1; i<steps.length; i++) {
    FDistanceJoint junta = new FDistanceJoint(hanginv, steps[i-1]);
    junta.setAnchor1(boxWidth/2, 10);
    junta.setAnchor2(-boxWidth/2, 10);
    junta.setFrequency(frequency);
    junta.setDamping(damping);
    junta.setFill(0);
    junta.setDrawable(false);
    junta.calculateLength();
    world.add(junta);
  }
int endv=(floor(verc/10))*10;
 
 FCircle endpoint = new FCircle(15);
 endpoint.setPosition(tst.getVertex(verc-1).x,tst.getVertex(endv-10).y+20);
 endpoint.setDrawable(true);
 endpoint.setFill(120, 30, 0);
 endpoint.setDensity(.02);
 endpoint.setBullet(true);
//endpoint.setGroupIndex(1);
endpoint.setName("EndF");
//endpoint.setStatic(true);
world.add(endpoint);
for (int i=1; i<steps.length; i++) {
  FDistanceJoint junta = new FDistanceJoint(endpoint, steps[i-1]);
  junta.setAnchor1(boxWidth/2, 0);
  junta.setAnchor2(-boxWidth/2, 0);
  junta.setFrequency(frequency);
  junta.setDamping(damping);
  junta.setFill(0);
  junta.setDrawable(false);
  junta.calculateLength();
  world.add(junta);
}
  FDistanceJoint junta = new FDistanceJoint(endpoint, steps[steps.length-1]);
  junta.setAnchor1(boxWidth/2, 0);
  junta.setAnchor2(-boxWidth/2, 0);
  junta.setFrequency(frequency);
  junta.setDamping(damping);
  junta.setFill(0);
  junta.setStrokeWeight(5);
  junta.setDrawable(true);
  junta.calculateLength();
  world.add(junta);

tst.endShape();
 tst=createShape();
 tst.beginShape();
  if (poly!=null) {
     world.add(poly);
     poly = null;
      }
 }

void addSpring(){
FloatList sppointsx= new FloatList();
FloatList sppointsy= new FloatList();
for (int i = 0; i < tst.getVertexCount(); i++) {
   PVector v = tst.getVertex(i);
   float vx=(v.x);
   float vy=v.y;
   sppointsx.append(vx);
   sppointsy.append(vy);
  }

 float FLength=sppointsy.max()-sppointsy.min();
 float FWidth=sppointsx.max()-sppointsx.min();
FBox hang = new FBox(FLength,FWidth);  
hang.setStatic(false);
hang.setPosition(tst.getVertex(0).x,tst.getVertex(0).y+FLength/2);
hang.setDrawable(true);
hang.setGroupIndex(1);
hang.setDensity(.0005*FWidth/FLength);
spring = loadImage("zigzag.png");
spring.resize(int(FWidth),int(FLength));
hang.attachImage(spring);
hang.setName("spring");
world.add(hang);
FCircle hanger = new FCircle(30);  
hanger.setStatic(true);
hanger.setPosition(tst.getVertex(0).x,tst.getVertex(0).y-5);
hanger.setDrawable(true);
hanger.setGroupIndex(1);
hanger.setName("pin"); 
hanger.setDensity(0.01);
hanger.setBullet(true);
world.add(hanger);
//**************connecting the first part of spring to the *************
FRevoluteJoint juntaPrincipio = new FRevoluteJoint(hanger, hang);

juntaPrincipio.setAnchor(tst.getVertex(0).x,tst.getVertex(0).y);
juntaPrincipio.setFill(0);
juntaPrincipio.setDrawable(false);;
world.add(juntaPrincipio);
 int verc=tst.getVertexCount();
 FCircle endpoint = new FCircle(30);
 endpoint.setPosition(hang.getX(),sppointsy.max());
 endpoint.setDrawable(true);
 endpoint.setFill(120, 30, 0);
 endpoint.setDensity(0.05);
//endpoint.setGroupIndex(1);
endpoint.setName("EndF");
//endpoint.setStatic(true);
world.add(endpoint);
FRevoluteJoint jp= new FRevoluteJoint(endpoint, hang);

jp.setAnchor(hang.getX(),sppointsy.max());
jp.setFill(0);
jp.setDrawable(false);;
world.add(jp);
//FDistanceJoint junta = new FDistanceJoint(hang, endpoint);
//  junta.setAnchor1(boxWidth/2, 0);
//  junta.setAnchor2(-boxWidth/2, 0);
//  junta.setFrequency(frequency);
//  junta.setDamping(damping);
//  junta.setFill(0);
//  junta.setStrokeWeight(5);
//  junta.setDrawable(true);
//  junta.calculateLength();
//  world.add(junta);
//println("Maxx",sppointsx.max(),"Minx",sppointsx.min());
//println("Maxy",sppointsy.max(),"Miny",sppointsy.min());
tst.endShape();
tst=createShape();
tst.beginShape();
}
  
     
          
/* library imports *****************************************************************************************************/ //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>//

import processing.serial.*;
import com.dhchoi.CountdownTimer;
import com.dhchoi.CountdownTimerService;

/* Device block definitions ********************************************************************************************/
Device            haply_2DoF;
byte              deviceID                   = 5;
Board             haply_board;
DeviceType        degreesOfFreedom;
boolean           rendering_force                 = false;


/* Simulation Speed Parameters ****************************************************************************************/
final long        SIMULATION_PERIOD          = 1; //ms
final long        HOUR_IN_MILLIS             = 36000000;
CountdownTimer    haptic_timer;
float             dt                        = SIMULATION_PERIOD/1000.0; 
/**********************************************************************************************************************/
/*Definfing the sketching Env*/
PGraphics pgDrawing;
PShape SIM;
ArrayList <PShape> bg;
PShape tst;
 
/* generic data for a 2DOF device */
/* joint space */
PVector           angles                    = new PVector(0, 0);
PVector           torques                   = new PVector(0, 0);

/* task space */
PVector           pos_ee                    = new PVector(0, 0);
PVector           pos_ee_last               = new PVector(0, 0); 
PVector           f_ee                      = new PVector(0, 0); 
Boolean trFlag;
/* drawing setup */
ArrayList <PVector> Pointlist;
ArrayList <PVector> Pointlists;
StringList xPoints;
StringList yPoints;
PVector P=new PVector(0, 0);
String pointSave;

/* Graphic objects */
float pixelsPerCentimeter= 40.0; //this is the resolution of my screen divided by the number of centimeters  i.e. a 1600px x 800px display with a 40 cm screen -> 40 pixels/cm
FWorld world; 
FBox b; 
FPoly p; 
FCircle g; 
FCircle e; 
int gindx=1;  //group index for drawing
FBody hovered ;
ArrayList <FBody> WorldBodies;
HVirtualCoupling s; 
PImage haply_avatar; 
PImage circle; 
PImage block; 

float worldWidth = 17.50;  
float worldHeight = 19.00; 


float edgeTopLeftX = 0.0; 
float edgeTopLeftY = 0.0; 
float edgeBottomRightX = worldWidth; 
float edgeBottomRightY = worldHeight; 

void setup() {
  
  size(700, 750); // (worldWidth*pixelsPerCentimeter, worldHeight*pixelsPerCentimeter) must input as number

  /* BOARD */
  haply_board = new Board(this, "COM4", 0); //Put your COM# port here

  /* DEVICE */
  haply_2DoF = new Device(degreesOfFreedom.HaplyTwoDOF, deviceID, haply_board);

  hAPI_Fisica.init(this); 
  hAPI_Fisica.setScale(pixelsPerCentimeter); 
  world = new FWorld();
  // Drawing
  Pointlists=new ArrayList();
  Pointlist=new ArrayList();
  yPoints= new StringList();
  xPoints= new StringList();
  tst=createShape();
  tst.beginShape();
  //Insert Box object
  b = new FBox(2.0, 2.0);  //<>//
  b.setPosition(edgeTopLeftX+worldWidth/3.0, edgeTopLeftY+worldHeight/2.0); 
  b.setDensity(5); 
  b.setFill(random(255),random(255),random(255));
  world.add(b);

  // Insert Different sized circle objects
  //FCircle e1 = new FCircle(0.60);
  //e1.setPosition(7, 7);
  //e1.setFill(random(255),random(255),random(255));
  //world.add(e1); 
  
  FCircle e2 = new FCircle(2.75);
  e2.setPosition(5, 5); 
  e2.setStatic(true);
  e2.setFill(random(255),random(255),random(255));
  circle=loadImage("circle.png"); 
  circle.resize((int)(hAPI_Fisica.worldToScreen(1))*3, (int)(hAPI_Fisica.worldToScreen(1))*3);
  e2.attachImage(circle);
  world.add(e2); 
 
  //Insert T-shaped Polygon
  //p= new FPoly(); 
  //p.vertex(-1.5, -1.0);
  //p.vertex( 1.5, -1.0);
  //p.vertex( 3.0/2.0, 0);
  //p.vertex( 1.0/2.0, 0);
  //p.vertex( 1.0/2.0, 4.0/2.0);
  //p.vertex(-1.0/2.0, 4.0/2.0);
  //p.vertex(-1.0/2.0, 0);
  //p.vertex(-3.0/2.0, 0);
  //p.setPosition(edgeTopLeftX+10, edgeTopLeftY+5); 
  //p.setDensity(5); 
  //p.setFill(random(255),random(255),random(255));
  //world.add(p);

 ////Insert Hard Blob object
 // FBlob bl = new FBlob();
 // float sca = random(4, 5);
 // sca= sca/2.0f; 
 // bl.setAsCircle(9, 3, sca, 30);
 // bl.setStroke(0);
 // bl.setStrokeWeight(2);
 // bl.setFill(255);
 // bl.setFriction(0);
 // bl.setDensity(.25); 
 // bl.setFill(random(255),random(255),random(255)); 
 // world.add(bl);
  
  //Insert soft Blob object
  //FBlob b2 = new FBlob();
  //float sca1 = random(2, 4);
  //sca= sca1/2.0f; 
  //b2.setAsCircle(13, 4, sca1, 100);
  //b2.setStroke(0);
  //b2.setStrokeWeight(2);
  //b2.setFill(255);
  //b2.setFriction(0);
  //b2.setDensity(1.5); 
  //b2.setFill(random(255),random(255),random(255)); 
  //world.add(b2);

// Setup the Virtual Coupling Contact Rendering Technique

  s= new HVirtualCoupling((1.75)); 
  s.h_avatar.setDensity(0.0001); 
  s.h_avatar.setFill(255,0,0); 
  s.init(world, edgeTopLeftX+worldWidth/2, edgeTopLeftY+2); 
  haply_avatar = loadImage("car.png"); 
  haply_avatar.resize((int)(hAPI_Fisica.worldToScreen(1)+10), (int)(hAPI_Fisica.worldToScreen(1))+30);
  s.h_avatar.attachImage(haply_avatar); 


  world.setGravity((0.0), (0)); //1000 cm/(s^2)
  world.setEdges((edgeTopLeftX), (edgeTopLeftY), (edgeBottomRightX), (edgeBottomRightY)); 
  world.setEdgesRestitution(.4);
  world.setEdgesFriction(0.5);
  
  world.draw();
  
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
  
  frameRate(60); 
}

void draw() {
  background(255); 
   shape(tst);
  if(!rendering_force){
    
    //s.drawContactVectors(this); 
    
   }
    world.draw();
    //world.drawDebug();  
}

/**********************************************************************************************************************
 * Haptics simulation event, engages state of physical mechanism, calculates and updates physics simulation conditions
 **********************************************************************************************************************/ 

void onTickEvent(CountdownTimer t, long timeLeftUntilFinish){
  
  rendering_force = true;
   
  if (haply_board.data_available()) {
    /* GET END-EFFECTOR STATE (TASK SPACE) */
        
    angles.set(haply_2DoF.get_device_angles()); 
    pos_ee.set( haply_2DoF.get_device_position(angles.array()));
    pos_ee.set(pos_ee.copy().mult(100)); 
    
  }

  s.setToolPosition(edgeTopLeftX+worldWidth/2-(pos_ee).x+1.0, edgeTopLeftY+(pos_ee).y); 
  s.updateCouplingForce();
 
  f_ee.set(-s.getVCforceX(), s.getVCforceY());
 
  f_ee.div(1000); //
  haply_2DoF.set_device_torques(f_ee.array());
  torques.set(haply_2DoF.mechanisms.get_torque());
  haply_2DoF.device_write_torques();
  
  
  world.step(1.0f/1000.0f);
  
  rendering_force = false;
}


/* Timer control event functions **************************************************************************************/

/**
 * haptic timer reset
 */
void onFinishEvent(CountdownTimer t){
  println("Resetting timer...");
  haptic_timer.reset();
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
}

void mouseDragged(){

     
  Pointlist.add(new PVector(mouseX, mouseY));
  Pointlists.add(new PVector(mouseX,mouseY));
 
  xPoints.append(str(mouseY));
  stroke(126);
  tst.vertex(mouseX,mouseY);
}

void mouseReleased(){

  gindx++;                          // increase the group index
  PVector v1=new PVector (0,0);     // location of first vertex
  PVector v2=new PVector (0,0);     // location of second vertex
  FCircle e2 = new FCircle(0.175);  // Make a circle body to select the line in order to delete it

  e2.setPosition(v1.x/40,v1.y/40); 
  e2.setStatic(true);
  e2.setFill(random(0),random(0),random(0));
  e2.setGroupIndex(gindx);
  world.add(e2); 
  for (int i=1;i<tst.getVertexCount();i++){ // Draw the line
    v1=(tst.getVertex(i-1));
    v2=(tst.getVertex(i));
    FLine myLine = new FLine(v1.x/40,v1.y/40, v2.x/40,v2.y/40);
    myLine.setGroupIndex(gindx);
    world.add(myLine); // add the line into the world
  }
   tst.endShape();     

   
   tst=createShape();
   tst.beginShape();
   
  }
  
  
  
  void keyPressed() {
  float x=mouseX/40.000; // Changing the mouse poition to the world framing
  float y=mouseY/40.000; // Changing the mouse poition to the world framing
  FBody hovered = world.getBody(x,y); // get the hovered body position
  if ( hovered != null  ) {
  int selectedLine= hovered.getGroupIndex();  // find the hovered group index
  WorldBodies=world.getBodies();              // get all the bodies of the world
  for (FBody tempbody : WorldBodies) {
      if (tempbody.getGroupIndex()==selectedLine){ // check if the temp body has the same index
        world.remove(tempbody);                    // delete the body
      }
    }
    println();
    }else{
    println("No line is being selected");
    }
      
  }

/* library imports *****************************************************************************************************/ //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>//

import processing.serial.*;
import com.dhchoi.CountdownTimer;
import com.dhchoi.CountdownTimerService;
import websockets.*;

/* WebSocket fields ****************************************************************************************************/
WebsocketServer ws;
int xFakeMouse;
int yFakeMouse;

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
//PShape tst;

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
ArrayList <PVector> Pointlist; //all points
ArrayList <PVector> currStroke; //only current stroke
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
HVirtualCoupling s; 
PImage haply_avatar; 
PImage circle; 
PImage block; 
int gindx=1;  //group index for drawing
ArrayList <FBody> WorldBodies;

float worldWidth = 17.50;  
float worldHeight = 19.00; 


float edgeTopLeftX = 3.75;//0.0;  // (graphwidth)/40
float edgeTopLeftY = 0.0;//0.0; 
float edgeBottomRightX = edgeTopLeftX + worldWidth; 
float edgeBottomRightY = edgeTopLeftY + worldHeight; 

/* Colours and other stuff for the graphs ************************************************************************************************/
color red = color(255, 0, 0);
color green = color(0, 255, 0);
color blue = color(0, 0, 255);
color hotpink = color(255,182,193);
color white = color(255, 255, 255);

float[] tau1_and_2 = new float[2];
ArrayList<Dot> tau1List = new ArrayList();
ArrayList<Dot> tau2List = new ArrayList();

int graphwidth = 150;
int centrex = graphwidth/2;
int centrey = 750+graphwidth/2;

boolean mouse_b = false;
float C = 40;



void setup() {
  
  
 
  
//  size(700+graphwidth, 750+graphwidth); // (worldWidth*pixelsPerCentimeter, worldHeight*pixelsPerCentimeter) must input as number
//  size(1000, 1050);
  size(850, 900);
  


  
  /* setup websocket */
  
  //Initiates the websocket server, and listens for incoming connections on ws://localhost:8025/john
  ws= new WebsocketServer(this, 8080,"/WebsocketHttpListenerDemo"); //ws://Localhost:8080/WebsocketHttpListenerDemo

  /* BOARD */
  haply_board = new Board(this, "COM4", 0); //Put your COM# port here

  /* DEVICE */
  haply_2DoF = new Device(degreesOfFreedom.HaplyTwoDOF, deviceID, haply_board);

  hAPI_Fisica.init(this); 
  hAPI_Fisica.setScale(pixelsPerCentimeter); 
  world = new FWorld();
  // Drawing
  currStroke=new ArrayList();
  Pointlist=new ArrayList();
  println("currstroke and pointlist was initialized");
  yPoints= new StringList();
  xPoints= new StringList();
//  tst=createShape();
//  tst.beginShape();
  //Insert Box object
  //b = new FBox(2.0, 2.0); 
  //b.setPosition(edgeTopLeftX+worldWidth/3.0, edgeTopLeftY+worldHeight/2.0); 
  //b.setDensity(5); 
  //b.setFill(random(255),random(255),random(255));
  //world.add(b);

  // Insert Different sized circle objects
  //FCircle e1 = new FCircle(0.60);
  //e1.setPosition(7, 7);
  //e1.setFill(random(255),random(255),random(255));
  //world.add(e1); 
  
  //Circle object
  //FCircle e2 = new FCircle(2.75);
  //e2.setPosition(8, 9);//(5, 5); 
  //e2.setStatic(true);
  //e2.setFill(random(255),random(255),random(255));
  //circle=loadImage("circle.png"); 
  //circle.resize((int)(hAPI_Fisica.worldToScreen(1))*3, (int)(hAPI_Fisica.worldToScreen(1))*3);
  //e2.attachImage(circle);
  //world.add(e2);
 
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
  s.h_avatar.setDensity(2); 
  s.h_avatar.setFill(255,0,0); 
  s.init(world, edgeTopLeftX+worldWidth/2, edgeTopLeftY+2); 
  haply_avatar = loadImage("car.png"); 
  haply_avatar.resize((int)(hAPI_Fisica.worldToScreen(1)+10), (int)(hAPI_Fisica.worldToScreen(1))+30);
  s.h_avatar.attachImage(haply_avatar); 


  world.setGravity((0.0), (0)); //1000 cm/(s^2)
  world.setEdges((edgeTopLeftX), (edgeTopLeftY), (edgeBottomRightX), (edgeBottomRightY)); 
 //world.setEdges();
  world.setEdgesRestitution(.4);//(.4);
  world.setEdgesFriction(0.5);
  
  world.draw();
  
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
  
  frameRate(60); 

}

void draw() {

  
  background(255);
  
  world.draw();
  
  fill(0);
  stroke(0);
  rect(0, 0, graphwidth, 750+graphwidth);
  rect(0, 750, 750+graphwidth, graphwidth);
  
  stroke(red);
  line(graphwidth/2, 0, graphwidth/2, 750+graphwidth);
  stroke(0);
  
  stroke(red);
  line(0, 750+graphwidth/2, 700+graphwidth, 750+graphwidth/2);
  stroke(0);
  
  // Drawing the dots //
   //<>//
   
  tau2List.add(new Dot(centrex, centrey + floor(tau1_and_2[1]*20), false)); //make a new dot for the current torque
  tau1List.add(new Dot(centrex + floor(tau1_and_2[0]*20), centrey, true)); //make a new dot for the current torque
  
  for (Dot dot : tau2List) { //update the two lists
    dot.update();
  } 
  for (Dot dot : tau1List) {
    dot.update();
  } 
  
  for (Dot each : tau1List) {
    drawDot(each, green);
  }
  
  for (Dot each : tau2List) {
 //   if (each != null) {
    drawDot(each, hotpink);
 //   System.out.println("dotx = " + each.x);
 //   }
  }
  
  fill(white);
  textSize(32);
  text("Horizontal", 10, 30);
  text("Torque", 30, 62);
  fill(0);
  
  fill(white);
  textSize(32);
  text("Vertical Torque", 580, 750+graphwidth/10);
  fill(0);
  
  //if (tst != null) {
  //   shape(tst);
  //}
  if(!rendering_force){
    
    //s.drawContactVectors(this); 
    
   }
 //   world.draw();
    
    //world.drawDebug();  
    
  //  System.out.println("xFakeMouse = " + str(xFakeMouse));
  //  System.out.println("yFakeMouse = " + str(yFakeMouse));

    // pen strokes //
    
    /*
   listOfStrokes.add(new Line(xFakePrev, yFakePrev, xFakeMouse, yFakeMouse));
   
   for (Line each : listOfStrokes) {
     renderStroke(each);
   }*/

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
  
  tau1_and_2 = haply_2DoF.set_device_torques(f_ee.array()); //array of floats (2 spots, first one is tau1, second is tau2)
  
  // These are the Dot operations //
  
//  System.out.println("tau1 = " + Float.toString(tau1_and_2[0])); //printouts
//  System.out.println("tau2 = " + Float.toString(tau1_and_2[1]));
 
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
  /*
  mouse_b = true;
  System.out.println("mouseDragged, mouse_b is true");

  
  Pointlist.add(new PVector(mouseX, mouseY));
  Pointlists.add(new PVector(mouseX,mouseY));
 
  xPoints.append(str(mouseY));
  stroke(126);
  tst.vertex(mouseX,mouseY);
  */
}

void mouseReleased(){
  
  mouse_b = false;
  //System.out.println("mouseReleased, mouse_b is false");

  
//  ArrayList<PVector> spacedPoints = new ArrayList();
//  resample(tst, spacedPoints, 100);
  
endStroke();


  }
  
  //void resample(PShape tst, ArrayList<PVector> points, int n) {
    
  //  float I = pathLength(tst) / (n-1);
  //  float D = 0;
  //  points.add(tst.getVertex(0));
    
  //  PVector v1;
  //  PVector v2;
    
  //  for (int i = 1; i < tst.getVertexCount(); i++) {
  //    v1 = tst.getVertex(i-1);
  //    v2 = tst.getVertex(i);
  //    float d = PVector.dist(v1, v2);
  //    if (D + d >= I) {
  //       PVector q = new PVector (v1.x + ((I-D)/d)*(v2.x - v1.x), v1.y + ((I-D)/d)*(v2.y - v1.y));
  //       points.add(q);
         
         
  //    }
      
  //  }
    
    
  //}
  
  int pathLength(PShape p) {
    
    return 0;
    
  }
  
  void mousePressed() {
    
    mouse_b = true;
    //System.out.println("mousePressed, mouse_b is true");
    
 //   listOfStrokes.add(new PShape());
    
  }
void webSocketServerEvent(String msg){
  //println(msg);
  
//String string = "004-034556";
if (!msg.equals("pen-up") && mousePressed) { //TODO only react to left button
  
   String[] parts = msg.split(" ");

   xFakeMouse = round(Float.parseFloat(parts[0])*10)+graphwidth; // 004
   yFakeMouse = round(Float.parseFloat(parts[1])*10); // 034556
   boolean toAdd = false;
   
   PVector fakemouse = new PVector(xFakeMouse,yFakeMouse);

   // Pointlists.add(new PVector(xFakeMouse,yFakeMouse));
   if (Pointlist != null) {
     //println("pointlist not null");

      if (!contains(Pointlist, fakemouse)) { //if pointlist does not already contain that dot, draw it
         println("added to currstroke: ", fakemouse);
         stroke(126);
         currStroke.add(fakemouse);
         toAdd = true;
      }
      if (toAdd) {
         Pointlist.add(fakemouse); //add it to pointlist then
      }
      toAdd = false;
   }
   else { //println("pointlist was null and no dot was added to currstroke"); 
 }

  }
  else if (!msg.equals("pen-up") && !mousePressed) { //if it's a dot but mouse is not pressed, do nothing
     //do nothing
  }
  else {
    endStroke();
  }
}

public boolean contains(ArrayList<PVector> list, PVector v) {
  for (PVector p : list) {
    if ((p.x == v.x) && (p.y == v.y)) {
       return true;
    }
  }
  return false;
}

  


  /* Draws the dot at (x, y) with colour c. resets stroke to black after */
public void drawDot(Dot d, color c) {
    stroke(c);
    point(d.x, d.y);
    stroke(0);
  }

//public void renderStroke(Line l) {
//    stroke(0);
//    line(l.xprev, l.yprev, l.xcurr, l.ycurr);
//}

public void endStroke() {
  println("endstroke called");
// if (tst != null && tst.getVertexCount() > 0) { //check for if tst is null
 if (currStroke != null && currStroke.size() > 0) {
   println("endstroke: currstroke not null");
   
  PVector v1=new PVector (0,0);     // location of first vertex
  PVector v2=new PVector (0,0);     // location of second vertex
  
        gindx++;                          // increase the group index

  
  ArrayList<PVector> pruned_points = new ArrayList();
    
    for (int i=0;i<currStroke.size();i=i+1){ //running average
       pruned_points.add(avg(currStroke, i, i+10));
       //pruned_points.add(currStroke.get(i));
    }
    
    PVector v = pruned_points.get(0); //first vertex
    println("first vertex: ", v);
    
    int count = 0;
    
    for (int i = 1;i < pruned_points.size();i=i+1){ //only adds a line between points if the distance is bigger than something
      v1 = pruned_points.get(i);
      //println("v1: ", v1);
      if (PVector.dist(v, v1) > C) {
         //println("dist: ", PVector.dist(v, v1));
         FLine myLine = new FLine(v.x/40,v.y/40, v1.x/40,v1.y/40);
         println("gindx: ", gindx, " v1: ", v1.x, ", ", v1.y);
         myLine.setGroupIndex(gindx);
         world.add(myLine);
         v = v1;
         
         count++;
         
      }
    }
    
    println("lines: ", count);
    
    //for (int i = 0; i < pruned_points.size()-2; i++) { // draws lines with all points in pruned_points.
    //   v1 = pruned_points.get(i);
    //   v2 = pruned_points.get(i+1);
    //   FLine myLine = new FLine(v1.x/40,v1.y/40, v2.x/40,v2.y/40);
    //   myLine.setGroupIndex(gindx);
    //   world.add(myLine);
    //}
    


  FCircle e2 = new FCircle(0.175);  // Make a circle body to select the line in order to delete it
  v1=pruned_points.get(0);
  e2.setPosition(v1.x/40,v1.y/40);
  e2.setStatic(true);
  e2.setFill(random(0),random(0),random(0));
  e2.setGroupIndex(gindx);
  world.add(e2); 
  
  

  /*
  if (PVector.dist(v, v1) > C ) { //only adds first and last vertices, this basically works
       //println("dist: ", PVector.dist(v, v1));

       FLine myLine = new FLine(v.x/40,v.y/40, v1.x/40,v1.y/40);
       println("gindx: ", gindx, " v1: ", v1.x, ", ", v1.y);
       myLine.setGroupIndex(gindx);
       world.add(myLine);
       //v = v1;
    }
  */
  
  
      /*
  for (int i=1;i<tst.getVertexCount();i=i+1){ //only adds a line between points if the distance is bigger than something
    v1=(tst.getVertex(i));
    if (PVector.dist(v, v1) > C ) {
       //println("dist: ", PVector.dist(v, v1));
       FLine myLine = new FLine(v.x/40,v.y/40, v1.x/40,v1.y/40);
       println("gindx: ", gindx, " v1: ", v1.x, ", ", v1.y);
       myLine.setGroupIndex(gindx);
       world.add(myLine);
       v = v1;
    }
    }
    */
    /*
  for (int i=1;i<tst.getVertexCount()-1;i=i+1){ //adds every point
    v1=(tst.getVertex(i-1));
    v2=(tst.getVertex(i));
    if (PVector.dist(v1, v2) > C ) {
    FLine myLine = new FLine(v1.x/40,v1.y/40, v2.x/40,v2.y/40);
    world.add(myLine);
    }
    }
*/
//   tst.endShape(); //tst is a placeholder thing for a shape
  }
   
  // tst=createShape();
  // tst.beginShape();
  
  //currStroke.clear();
  currStroke = new ArrayList();
}

PVector avg(ArrayList<PVector> a, int start, int end) {
  
  int sumx = 0;
  int sumy = 0;
  if (a != null) {
  
  for (int i = start; i < min(end, a.size()); i++) {
    sumx += a.get(i).x;
    sumy += a.get(i).y;
  }
  sumx /= min(end, a.size()) - start;
  sumy /= min(end, a.size()) - start;
  }
  return new PVector(sumx, sumy);
  
}

public void keyPressed() {
  
  
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
  

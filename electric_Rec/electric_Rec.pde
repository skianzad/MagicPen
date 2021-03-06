

/* library imports *****************************************************************************************************/
import processing.serial.*;
import com.dhchoi.CountdownTimer;
import com.dhchoi.CountdownTimerService;
import grafica.*;
import java.util.Random;
import ddf.minim.*;
import ddf.minim.ugens.*;
import de.voidplus.dollar.*;
import processing.svg.*;
import processing.pdf.*;
//import geomerative.*;
import websockets.*;
import fisica.*;
AudioPlayer player;
Minim minim;//audio context


/* Device block definitions ********************************************************************************************/
Device            haply_2DoF;
byte              deviceID             = 5;
Board             haply_board;
DeviceType        device_type;


/* Animation Speed Parameters *****************************************************************************************/
long              baseFrameRate        = 250; 
long              count                = 0; 
int               pixelsPerMeter       = 10000; 
PVector           offset               =new PVector(0, 0);

/* Simulation Speed Parameters ****************************************************************************************/
final long        SIMULATION_PERIOD    = 1; //ms
final long        HOUR_IN_MILLIS       = 36000000;
CountdownTimer    haptic_timer;

/* generic data for a 2DOF device */
/* joint space */
PVector           angles               = new PVector(0, 0);

PVector           torques              = new PVector(0, 0);
PVector           device_origin        = new PVector (0, 0) ; 
/* task space */
PVector           pos_ee               = new PVector(0, 0);
PVector           lastpos_ee           = new PVector(0, 0);
PVector           f_ee                 = new PVector(0, 0); 



int qp=120, qn=-120;
float[] F={0,0};
float K=8.99;
float Dx,Dy,DD,F1x,F1y,FT;
float x2,y2;
Random r = new Random();

int highlight = #6673b2;

PVector pos_btn = new PVector(500, 700);
PVector neg_btn = new PVector(700, 700);
float   btn_width = 30;
int draw_sign = 2;

int     selected_obj;
//0: nothing selected
//1: pos_btn selected
//2: neg_btn selected
//3: a charge selected

boolean mouse_ctrl = true;

ElectricCharge current_charge;
ElectricCharge hovered_charge;

PVector force_vector;

GPlot graph;
GPointsArray points = new GPointsArray(1000);

//set up electric fields
ArrayList <Particle> particles = new ArrayList <Particle> ();
int particle_size = 0;

//set up electric charges
ArrayList <ElectricCharge> charges = new ArrayList <ElectricCharge> ();


//*******************************************************************************************************
FWorld world;
FPoly poly;
FCircle circle;
FBody ava;
FBlob blob;
PImage spring;
FloatList sppointsx;
FloatList sppointsy;
ArrayList<FBody> TouchBody;
ArrayList<FJoint> Joints;
  //*****
  float frequency = 5;
  float damping = 10;
  float puenteY;
  int boxWidth=4;
//********************************************************************************************************
OneDollar one;
// Training setup:
ArrayList <PVector> Pointlist;
ArrayList <PVector> Pointlists;
StringList xPoints;
StringList yPoints;
PVector Po;
String pointSave;
Table table;
Table train;
char lable='N';
PVector po;
Boolean trFlag;
int[] candidate;
/**********************************************************************************************************************/
/*Definfing the sketching Env*/
PGraphics pgDrawing;
PShape SIM;
ArrayList <PShape> bg;
PShape tst;
//RShape grp;
int NP=1;
//float x=width/2;
//float y=height/2;
boolean flag= true;
int selected;
boolean avatar=false;


void setup() {
  
  //websocketSetup();
  
  size(1200, 800, P2D);
  background(255);
  minim = new Minim(this);
  player = minim.loadFile("fl1.mp3", 2048);
  player.loop();
  player.setGain(-60);
  player.play();
  //size(1200, 800, P2D);
  smooth(16);
  background(255);
  strokeWeight(0.75);
  frameRate(baseFrameRate);
  createGraph();
   PVector offset=new PVector(0,0);
  
  
  /* Initialization of the Board, Device, and Device Components */
  
  /* BOARD */
     haply_board =new Board(this, "COM4", 0); //Put your COM# port here

  /* DEVICE */
  haply_2DoF = new Device(device_type.HaplyTwoDOF, deviceID, haply_board);
  device_origin.add((width/2), (height/5) );
   /* haptics event timer, create and start a timer that has been configured to trigger onTickEvents */
  /* every TICK (1ms or 1kHz) and run for HOUR_IN_MILLIS (1hr), then resetting */
  //haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
  
  

  trFlag=true;
  table=loadTable("table.csv","header");
  
// Training setup:
train=new Table();
Pointlists=new ArrayList();
Po=new PVector();
yPoints= new StringList();
xPoints= new StringList();
println(table.getRowCount() + " total rows in table"); 
if (table.getRowCount()==0){
table= new Table();
table.addColumn("X/Y");  
table.addColumn("Lable");
candidate= new int[3];}
// *************************
 /*Making the drawing objects*/
  pgDrawing = createGraphics(1057, 1057, SVG, "test1.svg");
  pgDrawing.beginDraw();
  pgDrawing.beginShape();
  tst=createShape();
  tst.beginShape();
  bg=new ArrayList<PShape>();
  //bg.add(new PShape());
  //bg.get(0)=createShape();
  SIM=createShape(GROUP);
  
//*************************** making the phyiscal word
Fisica.init(this);
FBody ava;
  world = new FWorld();
  TouchBody=new ArrayList();
  world.setGravity(0, 800);
  world.setEdges();
  //world.remove(world.left);
  //world.remove(world.right);
  //world.remove(world.top);
  world.setEdgesRestitution(0.5);

//***************************
  po= new PVector();
  Pointlist=new ArrayList();
  one = new OneDollar(this);
  one.setVerbose(false);
  println(one);
  
  
  one.setMinSimilarity(65);

  // Data-Pre-Processing:
  one.setMinDistance(100).enableMinDistance();  
  one.setMaxTime(600000).enableMaxTime();
  //one.setMinSpeed(3).enableMinSpeed();

  // Algorithm settings:
  one.setFragmentationRate(100);
  one.setRotationStep(3);
  one.setRotationAngle(20);
  one.setBoundingBox(200);
  println(one);
  // All templates:
  //one.learn("triangle", new int[] {137,139,135,141,133,144,132,146,130,149,128,151,126,155,123,160,120,166,116,171,112,177,107,183,102,188,100,191,95,195,90,199,86,203,82,206,80,209,75,213,73,213,70,216,67,219,64,221,61,223,60,225,62,226,65,225,67,226,74,226,77,227,85,229,91,230,99,231,108,232,116,233,125,233,134,234,145,233,153,232,160,233,170,234,177,235,179,236,186,237,193,238,198,239,200,237,202,239,204,238,206,234,205,230,202,222,197,216,192,207,186,198,179,189,174,183,170,178,164,171,161,168,154,160,148,155,143,150,138,148,136,148} );
  one.learn("c", new int[] {127,141,124,140,120,139,118,139,116,139,111,140,109,141,104,144,100,147,96,152,93,157,90,163,87,169,85,175,83,181,82,190,82,195,83,200,84,205,88,213,91,216,96,219,103,222,108,224,111,224,120,224,133,223,142,222,152,218,160,214,167,210,173,204,178,198,179,196,182,188,182,177,178,167,170,150,163,138,152,130,143,129,140,131,129,136,126,139} );
  one.learn("r", new int[] {78,149,78,153,78,157,78,160,79,162,79,164,79,167,79,169,79,173,79,178,79,183,80,189,80,193,80,198,80,202,81,208,81,210,81,216,82,222,82,224,82,227,83,229,83,231,85,230,88,232,90,233,92,232,94,233,99,232,102,233,106,233,109,234,117,235,123,236,126,236,135,237,142,238,145,238,152,238,154,239,165,238,174,237,179,236,186,235,191,235,195,233,197,233,200,233,201,235,201,233,199,231,198,226,198,220,196,207,195,195,195,181,195,173,195,163,194,155,192,145,192,143,192,138,191,135,191,133,191,130,190,128,188,129,186,129,181,132,173,131,162,131,151,132,149,132,138,132,136,132,122,131,120,131,109,130,107,130,90,132,81,133,76,133} );
  //one.learn("x", new int[] {87,142,89,145,91,148,93,151,96,155,98,157,100,160,102,162,106,167,108,169,110,171,115,177,119,183,123,189,127,193,129,196,133,200,137,206,140,209,143,212,146,215,151,220,153,222,155,223,157,225,158,223,157,218,155,211,154,208,152,200,150,189,148,179,147,170,147,158,147,148,147,141,147,136,144,135,142,137,140,139,135,145,131,152,124,163,116,177,108,191,100,206,94,217,91,222,89,225,87,226,87,224} );
  //one.learn("check", new int[] {91,185,93,185,95,185,97,185,100,188,102,189,104,190,106,193,108,195,110,198,112,201,114,204,115,207,117,210,118,212,120,214,121,217,122,219,123,222,124,224,126,226,127,229,129,231,130,233,129,231,129,228,129,226,129,224,129,221,129,218,129,212,129,208,130,198,132,189,134,182,137,173,143,164,147,157,151,151,155,144,161,137,165,131,171,122,174,118,176,114,177,112,177,114,175,116,173,118} );
  //one.learn("caret", new int[] {79,245,79,242,79,239,80,237,80,234,81,232,82,230,84,224,86,220,86,218,87,216,88,213,90,207,91,202,92,200,93,194,94,192,96,189,97,186,100,179,102,173,105,165,107,160,109,158,112,151,115,144,117,139,119,136,119,134,120,132,121,129,122,127,124,125,126,124,129,125,131,127,132,130,136,139,141,154,145,166,151,182,156,193,157,196,161,209,162,211,167,223,169,229,170,231,173,237,176,242,177,244,179,250,181,255,182,257} );
  one.learn("s", new int[] {307,216,333,186,356,215,375,186,399,216,418,186} );
  //one.learn("arrow", new int[] {68,222,70,220,73,218,75,217,77,215,80,213,82,212,84,210,87,209,89,208,92,206,95,204,101,201,106,198,112,194,118,191,124,187,127,186,132,183,138,181,141,180,146,178,154,173,159,171,161,170,166,167,168,167,171,166,174,164,177,162,180,160,182,158,183,156,181,154,178,153,171,153,164,153,160,153,150,154,147,155,141,157,137,158,135,158,137,158,140,157,143,156,151,154,160,152,170,149,179,147,185,145,192,144,196,144,198,144,200,144,201,147,199,149,194,157,191,160,186,167,180,176,177,179,171,187,169,189,165,194,164,196} );
  //one.learn("leftsquarebracket", new int[] {140,124,138,123,135,122,133,123,130,123,128,124,125,125,122,124,120,124,118,124,116,125,113,125,111,125,108,124,106,125,104,125,102,124,100,123,98,123,95,124,93,123,90,124,88,124,85,125,83,126,81,127,81,129,82,131,82,134,83,138,84,141,84,144,85,148,85,151,86,156,86,160,86,164,86,168,87,171,87,175,87,179,87,182,87,186,88,188,88,195,88,198,88,201,88,207,89,211,89,213,89,217,89,222,88,225,88,229,88,231,88,233,88,235,89,237,89,240,89,242,91,241,94,241,96,240,98,239,105,240,109,240,113,239,116,240,121,239,130,240,136,237,139,237,144,238,151,237,157,236,159,237} );
  //one.learn("rightsquarebracket", new int[] {112,138,112,136,115,136,118,137,120,136,123,136,125,136,128,136,131,136,134,135,137,135,140,134,143,133,145,132,147,132,149,132,152,132,153,134,154,137,155,141,156,144,157,152,158,161,160,170,162,182,164,192,166,200,167,209,168,214,168,216,169,221,169,223,169,228,169,231,166,233,164,234,161,235,155,236,147,235,140,233,131,233,124,233,117,235,114,238,112,238} );
  //one.learn("v", new int[] {89,164,90,162,92,162,94,164,95,166,96,169,97,171,99,175,101,178,103,182,106,189,108,194,111,199,114,204,117,209,119,214,122,218,124,222,126,225,128,228,130,229,133,233,134,236,136,239,138,240,139,242,140,244,142,242,142,240,142,237,143,235,143,233,145,229,146,226,148,217,149,208,149,205,151,196,151,193,153,182,155,172,157,165,159,160,162,155,164,150,165,148,166,146} );
  //one.learn("delete", new int[] {123,129,123,131,124,133,125,136,127,140,129,142,133,148,137,154,143,158,145,161,148,164,153,170,158,176,160,178,164,183,168,188,171,191,175,196,178,200,180,202,181,205,184,208,186,210,187,213,188,215,186,212,183,211,177,208,169,206,162,205,154,207,145,209,137,210,129,214,122,217,118,218,111,221,109,222,110,219,112,217,118,209,120,207,128,196,135,187,138,183,148,167,157,153,163,145,165,142,172,133,177,127,179,127,180,125} );
  //one.learn("leftcurlybrace", new int[] {150,116,147,117,145,116,142,116,139,117,136,117,133,118,129,121,126,122,123,123,120,125,118,127,115,128,113,129,112,131,113,134,115,134,117,135,120,135,123,137,126,138,129,140,135,143,137,144,139,147,141,149,140,152,139,155,134,159,131,161,124,166,121,166,117,166,114,167,112,166,114,164,116,163,118,163,120,162,122,163,125,164,127,165,129,166,130,168,129,171,127,175,125,179,123,184,121,190,120,194,119,199,120,202,123,207,127,211,133,215,142,219,148,220,151,221} );
  //one.learn("rightcurlybrace", new int[] {117,132,115,132,115,129,117,129,119,128,122,127,125,127,127,127,130,127,133,129,136,129,138,130,140,131,143,134,144,136,145,139,145,142,145,145,145,147,145,149,144,152,142,157,141,160,139,163,137,166,135,167,133,169,131,172,128,173,126,176,125,178,125,180,125,182,126,184,128,187,130,187,132,188,135,189,140,189,145,189,150,187,155,186,157,185,159,184,156,185,154,185,149,185,145,187,141,188,136,191,134,191,131,192,129,193,129,195,129,197,131,200,133,202,136,206,139,211,142,215,145,220,147,225,148,231,147,239,144,244,139,248,134,250,126,253,119,253,115,253} );
  //one.learn("star", new int[] {75,250,75,247,77,244,78,242,79,239,80,237,82,234,82,232,84,229,85,225,87,222,88,219,89,216,91,212,92,208,94,204,95,201,96,196,97,194,98,191,100,185,102,178,104,173,104,171,105,164,106,158,107,156,107,152,108,145,109,141,110,139,112,133,113,131,116,127,117,125,119,122,121,121,123,120,125,122,125,125,127,130,128,133,131,143,136,153,140,163,144,172,145,175,151,189,156,201,161,213,166,225,169,233,171,236,174,243,177,247,178,249,179,251,180,253,180,255,179,257,177,257,174,255,169,250,164,247,160,245,149,238,138,230,127,221,124,220,112,212,110,210,96,201,84,195,74,190,64,182,55,175,51,172,49,170,51,169,56,169,66,169,78,168,92,166,107,164,123,161,140,162,156,162,171,160,173,160,186,160,195,160,198,161,203,163,208,163,206,164,200,167,187,172,174,179,172,181,153,192,137,201,123,211,112,220,99,229,90,237,80,244,73,250,69,254,69,252} );
  //one.learn("pigtail", new int[] {81,219,84,218,86,220,88,220,90,220,92,219,95,220,97,219,99,220,102,218,105,217,107,216,110,216,113,214,116,212,118,210,121,208,124,205,126,202,129,199,132,196,136,191,139,187,142,182,144,179,146,174,148,170,149,168,151,162,152,160,152,157,152,155,152,151,152,149,152,146,149,142,148,139,145,137,141,135,139,135,134,136,130,140,128,142,126,145,122,150,119,158,117,163,115,170,114,175,117,184,120,190,125,199,129,203,133,208,138,213,145,215,155,218,164,219,166,219,177,219,182,218,192,216,196,213,199,212,201,211} );
  // http://depts.washington.edu/aimgroup/proj/dollar/unistrokes.gif

  one.bind("triangle circle rectangle x check zigzag arrow leftsquarebracket rightsquarebracket v delete leftcurlybrace righttcurlybrace star pigtail", "detected");

}


void detected(String gesture, float percent, int startX, int startY, int centroidX, int centroidY, int endX, int endY){
  println("Gesture: "+gesture+", "+startX+"/"+startY+", "+centroidX+"/"+centroidY+", "+endX+"/"+endY);
}



void draw(){
  background(255); 
 //   btnPanel();
  
  //Drawing the fluid dynamics
  //flow();
  world.step();
  world.draw(this);
  shape(tst);
   if ( ava != null  ) {
       println("force in x",ava.getX(),"Force in Y direction",ava.getY());
 }
drawing();
  //background(255);  
  //one.draw();
}
//one.track
void mouseDragged(){
  
  FBody hovered = world.getBody(mouseX, mouseY);
      if ( hovered == null  ) {
  Pointlist.add(new PVector(mouseX, mouseY));
  Pointlists.add(new PVector(mouseX,mouseY));
  xPoints.append(str(mouseX));
  xPoints.append(str(mouseY));
  stroke(126);
  tst.vertex(mouseX,mouseY);
      }
      
  //if (force_vector != null){
  //  drawVector();
  //}
      
      
}
void mouseReleased(){
 //   mouse_b = false;
  if (trFlag==false){
    FBody hovered = world.getBody(mouseX, mouseY); //add the points
     if ( hovered == null  ) {
        if (Pointlist.size()>=40){
          for (int i=1;i<Pointlist.size();i++){
            po=Pointlist.get(i);
            one.track(po.x,po.y);
            }
        }
     }
   Pointlist.clear();
   String res=one.checkGlobalCallbacks();
   //println("the result is",res.charAt(0));
   if(res!=""){ 
       switch (res.charAt(0)){
       case 'r':
       println("A Mass is detected");
       addMass();
       //addElement(); //we're trying to make it so if a mass or charge is detected, a generic object is drawn, and then the person can decide which one they want. To reverse, comment in addMass
                     //and addcharge, and comment out addElement()
       break;
       case 'c':
       println("A Charge is detected");
       addcharge();
       //addElement();
       break;
       case 's':
       println("A Spring is detected");
       addSpring();
       break;
       default:
       tst.endShape();
       tst=createShape();
       tst.beginShape();
       break;
         }  
       }
       else{
         tst.endShape();
         tst=createShape();
         tst.beginShape();
       };
}
else {
    String[] ResultX=xPoints.array();
    xPoints.clear();
    pointSave=join(ResultX,",");
     String[] list = split(pointSave, ' ');
     TableRow row = table.addRow();
     row.setString("X/Y", pointSave);
     row.setString("Lable", str(lable));
     saveTable(table,"table.csv"); 
  }

}

void keyPressed() {
  
  
lable=key;
  switch(key){

    case 32:
     trFlag=true;
     train=loadTable("table.csv","header");
     table=train;
     for (int i=0;i<(table.getRowCount());i++){
         TableRow row = train.getRow(i);
         String ps=(row.getString("X/Y"));
         String la=row.getString("Lable");
         
         println("la: ", la);
           if ((la.charAt(0) =='N')||( la.charAt(0) ==32)){
               table.removeRow(i);
               saveTable(table,"table.csv"); 
           } else{   
             String[] pts=split(ps,',');
             int[]points=int(pts);
               if (points.length<=5){
                 table.removeRow(i);
                 saveTable(table,"table.csv"); 
               }else{
                 one.addGesture(la,points);
                 println("LERANING NEW STROKES...");
                 println(la);
                 one.bind(la,la);
               }
        }
       }
    break;
    case 113:
      println("******************************************************************");  
      println("SYSTEM IS READY");
      trFlag=false;
    break;
    case 't':
    println("Mass");
    lable=key;
    trFlag=true;
    break;
    case 's':
      println("spring");
      lable=key;
      trFlag=true;
      break;
    case 'r':
      println("Mass");
      lable=key;
      trFlag=true;
      break;
    case (BACKSPACE):
      println("Backspace");
        FBody hovered = world.getBody(mouseX, mouseY);
        if ( hovered != null  ) {
         //int gind;
          //gind=hovered.getGroupIndex();
          //if (gind==1){
          //      println("Spring is removed");
          //  }else{
          
          if (hovered_charge != null && hovered_charge != current_charge) {
              charges.remove(hovered_charge);
              world.remove(hovered);
          }
            //}
        }
      break;
      case (TAB):         // this changes the colour of the hovered charge
        //println("hovered charge pos: ", hovered_charge.x_pos, ", ", hovered_charge.y_pos);
        println("mouse: ", mouseX, ", ", mouseY);
        if (hovered_charge != null) {
        
        hovered_charge.sign = -hovered_charge.sign;
        if (hovered_charge.sign != 1) {
        hovered_charge.colour = #0070FF; //blue
        hovered_charge.q = qn;
        }
        else {
          hovered_charge.colour = #FF0000; //red
          hovered_charge.q = qp;
        }
        }
      break;
  }
      switch(keyCode) {
      case (UP): //increase q of hovered charge (and size of charge)

        if (hovered_charge != null && hovered_charge.q == 1) { //for a positive charge, increase q
              println("UP");
          //hovered_charge.q = 50 + hovered_charge.q;
         // hovered_charge.c_radius = 50 + hovered_charge.c_radius;
          println("hovered_charge: ", hovered_charge);
          println("hov charge: q = ", hovered_charge.q, ", c_radius = ", hovered_charge.c_radius);
          //hovered_charge.inner_radius += 10; 
        }
      break;
      case (DOWN): //decrease q of hovered charge (and size of charge)
      break;
      
      
    //default: 
    //lable=key;
    //trFlag=false;

    ////trFlag=true;
    //break;
  }
} 


void drawElement(){
  bg.add(tst);
  flag=false;
  SIM.addChild(tst);
  tst.endShape();
  //pgDrawing.shape(SIM);
  //pgDrawing.endShape();
  pgDrawing.endDraw();
  pgDrawing.dispose();
  pgDrawing.beginDraw();
  pgDrawing.beginShape();
 // shape(SIM);
 println(bg.size());
   for (int i=0;i<bg.size();i++)
    {   shape(SIM.getChild(i),0,0); 
  }////
  //P++;
  PVector v=new PVector (0,0);
    for (int i = 0; i < SIM.getChild(0).getVertexCount(); i++) {
        v = SIM.getChild(0).getVertex(i);
      //println((v.x-(width/2))/4000-pos_ee.x, ((height/5)+v.y)/4000-pos_ee.y);
       //println(pos_ee.x*4000,pos_ee.y*4000);
      }
     tst=createShape();
     tst.beginShape();
}
void contactEnded(FContact c) {  
  FBody b = (FBody)c.getBody1();
  FBody a = (FBody)c.getBody2();
  //println(a.getName());
  //println(a.getName());
  if ((a.getName()=="EndF")&&(b.getName()=="Mass")){
      b.setName("Joint");
      //a.setName("Joint");
      FRevoluteJoint jp= new FRevoluteJoint(a, b);

      jp.setAnchor(mouseX,mouseY);
      jp.setFill(0);
      jp.setDrawable(false);;
      world.add(jp);

      //FCompound result = new FCompound();
      
      //result.addBody(a);
      ////b.setPosition(a.getX(),a.getY()+20);
      //result.addBody(b);
      //world.remove(b);
      //world.add(result);
      //FDistanceJoint junta = new FDistanceJoint(a,result);
      //junta.setAnchor1(boxWidth/2, 0);
      //junta.setAnchor2(-boxWidth/2, 0);
      //junta.setFrequency(frequency);
      //junta.setDamping(damping);
      //junta.setFill(0);
      //junta.setStrokeWeight(5);
      //junta.setDrawable(true);
      ////junta.calculateLength();
      //world.add(junta);

      //result=null;
  
  }else if((a.getName()=="EndF")&&(b.getName()=="Joint")){
     b.setName("Joint");
      a.setName("Joint");
      FRevoluteJoint jp= new FRevoluteJoint(a, b);

      jp.setAnchor(mouseX,mouseY);
      jp.setFill(0);
      jp.setDrawable(false);;
      world.add(jp);
  }else if((a.getName()=="pin")&&(b.getName()=="EndF")){
      
      println("two joint");
      Joints=a.getJoints();
      println(Joints.get(1).getBody1().getName());
      println("spring",Joints.get(1).getBody2().getName());
      //if (a.isStatic()){
      world.remove(a);
      //}
      FRevoluteJoint jp= new FRevoluteJoint(Joints.get(1).getBody2(), b);

      jp.setAnchor(mouseX,mouseY);
      jp.setFill(0);
      jp.setDrawable(false);;
      world.add(jp);
  }else if((a.getName()=="pin")&&(b.getName()=="Joint")){
      
      println("two joint");
      //b.setName("MCenter");
      Joints=a.getJoints();
      a.setName("null");
      world.remove(a);
     // println(Joints.get(1).getBody1().getName());
      println("spring",Joints.get(1).getBody2().getName());
      //if (a.isStatic()){
      
      //}
      FRevoluteJoint jp= new FRevoluteJoint(Joints.get(1).getBody2(), b);

      jp.setAnchor(mouseX,mouseY);
      jp.setFill(0);
      jp.setDrawable(false);;
      world.add(jp);
  }
 //} else if((a.getName()=="pin")&&(b.getName()=="Joint")){
 //     a.setName("Joint");
 //     b.setName("Joint");
 //     a.setStatic(false);
 //     FRevoluteJoint jp= new FRevoluteJoint(a, b);

 //     jp.setAnchor(mouseX,mouseY);
 //     jp.setFill(0);
 //     jp.setDrawable(false);;
 //     world.add(jp);
 //}
 }
 void mouseClicked(){
 if (mouseButton == RIGHT) {
  ava = world.getBody(mouseX, mouseY);
      if ( ava != null  ) {
       println("avatar is being selected");
       }
   }
 }




void drawing() {
  
  //println("drawing() called");
  
  //btnPanel();
    onHover();
  
  //Drawing the fluid dynamics
  flow();
  
  if (charges.size() == 0) {
    particle_size = 150;
  } else if (charges.size() == 1){
    particle_size = 1000;
  } else if (charges.size() == 2){
    particle_size = 1250;
  } else if (charges.size() == 3){
    particle_size = 1500;
  } else if (charges.size() == 4){
    particle_size = 1725;
  } else if (charges.size() == 5){
    particle_size = 2000;
  }
  
  while (particles.size () < particle_size) { 
    Particle p = new Particle();
    particles.add(p); 
  }

  if (frameCount % 0.8 == 0) {
    noStroke();
    fill(#3c4677, 10);
    //fill(255,8);
    rect(0, 0, width, height);
   }
   
     if (frameCount % 10 == 0) {

    ArrayList<Particle> temp = new ArrayList<Particle>();
   for (int i = particles.size()/2; i < particles.size(); i++){
     temp.add(particles.get(i));
   }
   
   particles = temp;
  }
  
  ArrayList<Particle> temp = new ArrayList<Particle>(); 
  
  stroke(#9cadb5);
  //stroke(0,128);
  stroke(150);
  for (Particle p : particles) {
     if(!stuck(p.loc)){
       p.run();
       temp.add(p);
     }
  }
  
  particles = temp;
  
  for (ElectricCharge e : charges) { //update the x_position and y_pos of each charge that's not the current charge so that it is where its body is
    if (!e.equals(current_charge)) {
       e.x_pos = round(e.body.getX());

       e.y_pos = round(e.body.getY());
    }
  }
  
  
  for( ElectricCharge e : charges) {
    for (int i = 0; i < e.c_radius; i+=5) {
      fill(e.colour, 3*i/4); //change to color of its sign
      stroke(#000000);
      noStroke();
      ellipse(e.x_pos, e.y_pos, e.c_radius - i, e.c_radius - i);
      
      if (e.equals(current_charge)) { //a circle in the centre indicates that the charge is the current charge
        stroke(#000000);
        point(current_charge.x_pos, current_charge.y_pos);
        pushMatrix();
        translate(current_charge.x_pos,current_charge.y_pos);
        ellipse(0, 0, 10, 10);
        popMatrix();
      }

    }
  }
  
  //if (force_vector != null){
    //println("drawVector() called by drawing()");
    drawVector();
  //}
    if (current_charge != null) {
    println("curr charge: ", current_charge.x_pos, ", ", current_charge.y_pos);
    println("curr charge body: ", current_charge.body.getX(), ", ", current_charge.body.getY());
    }
    
    if (hovered_charge != null) {
    println("hov charge: ", hovered_charge.x_pos, ", ", hovered_charge.x_pos);
    println("hov charge body: ", hovered_charge.body.getX(), ", ", hovered_charge.body.getY());
    }
    //println("pos_ee: ", pos_ee.x*pixelsPerMeter, ", ", pos_ee.y*pixelsPerMeter);
 // graph.beginDraw();
  //graph.drawBox();

 // graph.drawPoints();
  //graph.endDraw();
  
}

void btnPanel(){
  //set up control panel
  fill(#3c4677);
  stroke(highlight);
  rect(450, 675, 300, 50, 7);
  
  fill(#FF0000);
  if (selected_obj == 1){ 
    fill(highlight);
  }
  stroke(#FF0000);
  ellipse(pos_btn.x, pos_btn.y, btn_width, btn_width);
  
  textSize(21);
  fill(#FF0000);
  text("+", pos_btn.x -7, pos_btn.y +5.5);
  
  
  fill(#0070FF);
  if (selected_obj == 2){ 
    fill(highlight);
  }
  stroke(#0070FF);
  ellipse(neg_btn.x, neg_btn.y, btn_width, btn_width);
  
  textSize(23);
  fill(#0070FF);
  text("-", neg_btn.x -6, neg_btn.y +5.5);
  
  onHover();
}


//1) change the current object under control
//2) highlight the selected object
void onHover(){
  //println("onHover called");
  selected_obj = 0;
  
  if( inCircle(pos_btn.x, pos_btn.y, mouseX, mouseY, btn_width) ) {
     selected_obj = 1; 
  }
  
  if( inCircle(neg_btn.x, neg_btn.y, mouseX, mouseY, btn_width) ) {
     selected_obj = 2; 
  }
  
  for (ElectricCharge c : charges) {
    if( inCircle(c.x_pos, c.y_pos, mouseX, mouseY, c.c_radius) ) {
      selected_obj = 3;
      hovered_charge = c;
      break;
    }
  }
}

boolean inCircle(float x1, float y1, float x2, float y2, float diameter) {
  float dis_x = x1 - x2;
  float dis_y = y1 - y2;
  
  if( sqrt(sq(dis_x) + sq(dis_y)) < diameter/2) {
  return true;
  }

  return false;
}

boolean inRect(float x, float y, float w, float h) {
  //stub
  return false;
}

void mousePressed() {
 // mouse_b = true;
  mouse_ctrl = true;
  
  force_vector = null;
  if(selected_obj == 1){
    draw_sign = 1;
  }
  else if(selected_obj == 2){
    draw_sign = 0;
  }
  else if(selected_obj == 3 && mouseButton == RIGHT){
    
    current_charge = hovered_charge;
    //change the offset here
    offset.set(current_charge.x_pos -(pos_ee.x)*pixelsPerMeter, current_charge.y_pos -(pos_ee.y)*pixelsPerMeter);
    //offset.set((pos_ee.x)*pixelsPerMeter, -(pos_ee.y)*pixelsPerMeter);
    

  }
  else if (charges.size() < 5){
    
    if (draw_sign == 1 ){
      addCharge(1);

    }
    
    if (draw_sign == 0){
      addCharge(0);
    }
  } 

}

ElectricCharge addCharge(int sign){
   if (haply_board.data_available()) {
        //  /* GET END-EFFECTOR STATE (TASK SPACE) */
        
        angles.set(haply_2DoF.get_device_angles()); 
        pos_ee.set( haply_2DoF.get_device_position(angles.array()));
   }

offset.set(mouseX + (pos_ee.x)*pixelsPerMeter, mouseY -(pos_ee.y)*pixelsPerMeter);

// FCircle (FBody) attached to the electric charge
  circle = new FCircle(60);
  circle.setStrokeWeight(1);
  circle.setFill(0, 0, 0);
  circle.setBullet(true);
  circle.setDensity(0.005);
  circle.setRotatable(false);
  circle.setName("charge");
  circle.setRestitution(0.7);
  circle.setStatic(true);
  circle.setGrabbable(false); //upon creation the charge cannot be dragged, because it is the avatar charge.

  ElectricCharge c = new ElectricCharge(10, 100, mouseX, mouseY, sign, circle); //make the charge
  charges.add(c); // add to list of charges

  current_charge = c; //set the current charge
  
      // Here, update the "grabbable" fields of all other charges (so that they are grabbable and the current charge isn't
    
    for (ElectricCharge e : charges) { 
      if (!e.equals(current_charge)) {
        e.body.setGrabbable(true);
      }
      else {
          e.body.setGrabbable(false);
      }
    }
    
  ArrayList<PVector> v_list = computeEachForce();
  computeTotalForce(v_list);
  

TouchBody=  circle.getTouching();
if(TouchBody!=null){ 
println("Touching bodies",TouchBody);
}
tst.endShape();
tst=createShape();
tst.beginShape();
if (  circle!=null) {
     circle.setPosition(current_charge.x_pos, current_charge.y_pos);
     //circle.setPosition(0, -30);
   //println("curr charge: ", current_charge.x_pos, ", ", current_charge.y_pos);
     world.add(  circle);
     circle = null;
  }
  

  
  return current_charge;
  
  
  
  
 

}

void flow(){
  for (ElectricCharge e : charges) {
      for (Particle p : particles) {
         p.addCenter(e.x_pos, e.y_pos, e.sign);
      }
     
  }
}

ArrayList<PVector> computeEachForce() {
    ArrayList<PVector> vectors = new ArrayList<PVector>();   
  
   for(ElectricCharge c : charges){
     if (c != current_charge){
       float dx = c.x_pos - current_charge.x_pos;
       float dy = c.y_pos - current_charge.y_pos;
       float dd = sqrt( dx*dx + dy*dy);
       
       float ft = -K* current_charge.q * c.q/(dd*dd); // current_charge.q * c.q = qp*qn    
       PVector vector = new PVector(ft*dx/dd, ft*dy/dd);
       vectors.add(vector);
     }
   }
   
  return vectors;
}

void computeTotalForce(ArrayList<PVector> vectors){
  float fx_total = 0;
  float fy_total = 0;
  
  for(PVector v : vectors) {
       fx_total += v.x;
       fy_total += v.y;
       //println(fx_total,fy_total);
      
       //if((abs(f_ee.x))>5){
       //      f_ee.x=0;
       //      f_ee.y=0;
       //      println("too close");
       //      //|abs(f_ee.y)>5
       //}
       //if (fx_total==0&fy_total==0){
       // player.setGain(-60);
       //}
       //else{
           f_ee.x=-fx_total/25;
           f_ee.y=fy_total/25;
           //println(abs(-fx_total),abs(fy_total));
           if((30<=abs(fx_total)&abs(fx_total)<50)|30<=abs(fy_total)&abs(fy_total)<50) {
             f_ee.x=0;
             f_ee.y=0;
              player.setGain(1);
           }
           else if((50<=abs(fx_total))|50<=abs(fy_total)) {
            f_ee.x=.571*fx_total/(abs(fx_total));
             f_ee.y=-.571*fy_total/(abs(fy_total));
             //f_ee.x=0;
             //f_ee.y=0;
              player.setGain(1);
           }else{
             f_ee.x=-fx_total/25;
             f_ee.y=fy_total/25;
             player.setGain(-10/(fy_total*fy_total+fx_total*fx_total));
         }
     
       
  }
  
  force_vector = new PVector(5*fx_total, 5*fy_total);
}

void drawVector() {
  if (current_charge != null) {
  if (force_vector != null) {
  x2=(force_vector.x*30);
  y2=(force_vector.y*30);

  stroke(#000000);
  line(current_charge.x_pos, current_charge.y_pos, current_charge.x_pos+x2,current_charge.y_pos+y2);
  pushMatrix();
  translate(current_charge.x_pos+x2,current_charge.y_pos+y2);
  float a = atan2(-x2, y2);
  rotate(a);
    line(0, 0, -10, -10);
    line(0, 0, 10, -10);
  popMatrix();
  }
  }
}

void createGraph(){
  for (int i = 0; i < 1000; i++) {
    float x = 10 + random(200);
    float y = 10 * exp(0.015 * x);
    float xErr = 2*((float) r.nextGaussian());
    float yErr = 2*((float) r.nextGaussian());
    points.add(x + xErr, y + yErr);
  }
  
  graph = new GPlot(this);
  graph.setPos(750, 450);
  graph.setDim(150, 150);
  graph.setBoxBgColor(#3c4677);
  graph.setBoxLineColor(highlight);
  
  graph.setLogScale("x");
  graph.setInvertedXScale(true);
  
  graph.setPoints(points);
  graph.setPointColor(color(100, 100, 255, 50));
}

boolean stuck(PVector position) {
   
    for (ElectricCharge e : charges){
     if (inCircle(position.x, position.y, e.x_pos, e.y_pos, e.c_radius)){
      return true;
      }
    }
    return false;
}


  /* Timer control event functions **************************************************************************************/
void onTickEvent(CountdownTimer t, long timeLeftUntilFinish){    //this gets called when the haptic device moves

  //println("onTick called");
  
  /* check if new data is available from physical device */
  if (haply_board.data_available()) {
   
    PVector tempAngle = new PVector(angles.x, angles.y);
    

    /* GET END-EFFECTOR POSITION (TASK SPACE) */
    angles.set(haply_2DoF.get_device_angles()); 
    
    if (angles.x == tempAngle.x && angles.y == tempAngle.y) {
      mouse_ctrl = true;
    } else {
        mouse_ctrl = false;
    }
    
    if (mouse_ctrl == false){
      PVector tempPos = new PVector(pos_ee.x, pos_ee.y);
    pos_ee.set( haply_2DoF.get_device_position(angles.array()));
    pos_ee.set(device2graphics(pos_ee));    
    
    //println(pos_ee.x*pixelsPerMeter,pos_ee.y*pixelsPerMeter);
    //current_charge.x_pos=int((pos_ee.x-lastpos_ee.x)*pixelsPerMeter+400);
    //current_charge.y_pos=int((pos_ee.y-lastpos_ee.y)*pixelsPerMeter-200);
    
    current_charge.x_pos =  int(( pos_ee.x)*pixelsPerMeter)+int(offset.x);
    current_charge.y_pos = int((pos_ee.y )*pixelsPerMeter)+int( offset.y);
    
    //println("curr charge: ", current_charge.x_pos, ", ", current_charge.y_pos);
    //println("pos_ee: ", pos_ee.x, ", ", pos_ee.y);
    
    ArrayList<PVector> v_list = computeEachForce();
    computeTotalForce(v_list);
    
    }
    
    }
    
    //update the position of the FCircle of the current charge to match the current charge's position
    
    //current_charge.body.setPosition(current_charge.x_pos, current_charge.y_pos);
    if (current_charge != null && current_charge.body != null) {
       current_charge.body.setPosition(current_charge.x_pos, current_charge.y_pos);
    }
    
  //    if (current_charge != null && force_vector != null){
  //  drawVector();
  //}
  
  
//f_ee.set(-10,-10);
    haply_2DoF.set_device_torques(f_ee.array());
    torques.set(haply_2DoF.mechanisms.get_torque());
    haply_2DoF.device_write_torques();
   
}

PVector device2graphics(PVector deviceFrame){
   
  return deviceFrame.set(-deviceFrame.x, deviceFrame.y);  
  
}

/**
 * haptic timer reset
 */
void onFinishEvent(CountdownTimer t){
  println("Resetting timer...");
  haptic_timer.reset();
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
}

/* Connection to the smartpen ***************** Copy paste this into the bottom of a file. Be sure to write "import websockets.*;" at the top **********/
/* HOW TO USE: open the Sample App in Visual studio. Deploy the app. Run this sketch. Then run the Sample App on Local Machine */
/* other instructions: set mouse_b to true when mouse is pressed, false when released. comment out mouseDragged. call websocketSetup in setup.*/

//// Fields //

//WebsocketServer ws;
//int xFakeMouse;
//int yFakeMouse;


//// Methods //

//void webSocketServerEvent(String msg){
//  println(msg);
  
//if (!msg.equals("pen-up") && mousePressed) {
  
//   String[] parts = msg.split(" "); //parsing the message

//   xFakeMouse = round(Float.parseFloat(parts[0])*10);
//   yFakeMouse = round(Float.parseFloat(parts[1])*10);
   
//   PVector fakemouse = new PVector(xFakeMouse,yFakeMouse); //stroke of fake mouse
   
//   // ADD THE BODY OF MOUSEDRAGGED HERE, replacing mouseX and mouseY with the fakemouse equivalents. COMMENT OUT MOUSEDRAGGED //

//        FBody hovered = world.getBody(xFakeMouse, yFakeMouse);
//      if ( hovered == null  ) {
//  Pointlist.add(fakemouse);
//  Pointlists.add(fakemouse);
//  xPoints.append(str(xFakeMouse));
//  xPoints.append(str(yFakeMouse));
//  stroke(126);
//  tst.vertex(xFakeMouse, yFakeMouse);
//      }
//  }
//  else {
//    mouseReleased();
 
//}
//}

///**
// * Ends the pen/mouse stroke
// */
 
//public void endStroke() {
// if (tst != null && tst.getVertexCount() > 0) { //check for if tst is null
      
//  PVector v1=new PVector (0,0);
//  PVector v2=new PVector (0,0);
  
//  PVector v = new PVector (0, 0);
//  v = (tst.getVertex(0));
  
      
//  for (int i=1;i<tst.getVertexCount();i=i+1){ //this is the part that adds the lines to the world
//    v1=(tst.getVertex(i));
//    if (PVector.dist(v, v1) > C ) {
//       FLine myLine = new FLine(v1.x/40,v1.y/40, v.x/40,v.y/40);
//       world.add(myLine);
//       v = v1;
//    }
//    }
    
//   tst.endShape(); //tst is a placeholder thing for a shape
//  }
   
//   tst=createShape();
//   tst.beginShape();
//}

//public boolean contains(ArrayList<PVector> list, PVector v) {
//  for (PVector p : list) {
//    if ((p.x == v.x) && (p.y == v.y)) {
//       return true;
//    }
//  }
//  return false;
//}

//public void websocketSetup() { // Call this in setup //
//    //Initiates the websocket server, and listens for incoming connections on ws://localhost:8025/john
//  ws= new WebsocketServer(this, 8080,"/WebsocketHttpListenerDemo"); //ws://Localhost:8080/WebsocketHttpListenerDemo
//  Pointlist = new ArrayList();
//}

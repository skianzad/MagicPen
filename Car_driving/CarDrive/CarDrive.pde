/**
 ************************************************************************************************************************
 * @file       HelloWall2.pde
 * @author     
 * @version    V0.1.0
 * @date       4-April-2017
 * @brief      Test example for creating a virtual vertical wall using the hAPI with velocity estimation
 ************************************************************************************************************************
 * @attention
 *
 *
 ************************************************************************************************************************
 */

/* library imports *****************************************************************************************************/
import processing.serial.*;
import com.dhchoi.CountdownTimer;
import com.dhchoi.CountdownTimerService;
import processing.svg.*;
import processing.pdf.*;
import geomerative.*;

/* Device block definitions ********************************************************************************************/
Device            haply_2DoF;
byte              deviceID             = 5;
Board             haply_board;
DeviceType        device_type;
//Mechanisms      NewMech = new NewExampleMech();


/* Animation Speed Parameters *****************************************************************************************/
long              baseFrameRate        = 120; 
long              count                = 0; 


/* Simulation Speed Parameters ****************************************************************************************/
final long        SIMULATION_PERIOD    = 1; //ms
final long        HOUR_IN_MILLIS       = 36000000;
CountdownTimer    haptic_timer;


/* Graphics Simulation parameters *************************************************************************************/
PShape            pantograph, joint1, joint2, handle;
PShape            wall; 

int               pixelsPerMeter       = 4000; 
float             radsPerDegree        = 0.01745; 

float             l                    = .05;
float             L                    = .07;
float             d                    = .04;
float             r_ee                 = d/3; 
float             r_ee_contact         = d/3;

PVector           device_origin        = new PVector (0, 0) ; 


/* Physics Simulation parameters **************************************************************************************/
PVector           f_wall               = new PVector(0, 0); 
float             k_wall               = 800; //N/mm 
float             b_wall               = .1;  //kg/s 
PVector           pen_wall             = new PVector(0, 0); 
PVector           pos_wall             = new PVector(-.085, 0);


/* generic data for a 2DOF device */
/* joint space */
PVector          angles                = new PVector(0, 0);
PVector          torques               = new PVector(0, 0);

/* task space */
PVector          pos_ee                = new PVector(0, 0);
PVector          pos_ee_last           = new PVector(0,0); 
float            dt                    = SIMULATION_PERIOD/1000.0;  
PVector          vel_ee                = new PVector(0,0); 
PVector          f_ee                  = new PVector(0, 0); 
PVector           SWall                    =new PVector (0,0);
/**********************************************************************************************************************/
/*Definfing the sketching Env*/
PGraphics pgDrawing;
PShape SIM;
PShape[] bg;
PShape tst;
RShape grp;
int NP=1;
float x=width/2;
float y=height/2;
boolean flag= true;
int selected;
PShape car;
PShape accident;
boolean contact=false;



/**********************************************************************************************************************
 * Main setup function, defines parameters for physics simulation and initialize hardware setup
 **********************************************************************************************************************/
void setup() {
stroke(126);
  /* Setup for the graphic display window and drawing objects */
  /* 20 cm x 15 cm */
  size(1057, 1057, P2D); //px/m*m_d = px
  background(0);
  frameRate(baseFrameRate);
  
  car=loadShape("car.svg");
  accident=loadShape("bang.svg");
  /*Making the drawing objects*/
  pgDrawing = createGraphics(1057, 1057, SVG, "test1.svg");
  pgDrawing.beginDraw();
  pgDrawing.beginShape();
  tst=createShape();
  tst.beginShape();
  bg=new PShape[100];
  bg[1]=createShape();
  SIM=createShape(GROUP);

      //pgDrawing.beginShape();
     // pgDrawing.vertex(mouseX, mouseY);
      stroke(126);
       

  /* Initialization of the Board, Device, and Device Components */
  
  /* BOARD */
  haply_board = new Board(this, "COM5", 0);

  /* DEVICE */
  haply_2DoF = new Device(device_type.HaplyTwoDOF, deviceID, haply_board);


  /* Initialize graphical simulation components */
  
  /* set device in middle of frame on the x-axis and in the fifth on the y-axis */
  device_origin.add((width/2), (height/5) );
  
  /* create pantograph graphics */
  createpantograph();

  /* create wall graphics */
  wall=  createWall(pos_wall.x,pos_wall.y+.1,pos_wall.x,pos_wall.y); 
  wall.setStroke(color(0));
  
  /* haptics event timer, create and start a timer that has been configured to trigger onTickEvents */
  /* every TICK (1ms or 1kHz) and run for HOUR_IN_MILLIS (1hr), then resetting */
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
}



/**********************************************************************************************************************
 * Main draw function, updates simulation animation at prescribed framerate 
 **********************************************************************************************************************/
void draw() {
   move();
   mouseP();
  update_animation(angles.x*radsPerDegree, angles.y*radsPerDegree, pos_ee.x, pos_ee.y,contact);
}

void move(){
  x=mouseX;
  y=mouseY;

}
void mouseReleased() {
  println("done");
      //grp.draw(pgDrawing);
    background(250);
       bg[NP]=tst;
      tst.endShape();
     
      flag=false;

      //
      //bg =loadShape("test1.svg");
     
    //for (int i=1;i<=NP;i++){
    //  if (bg[NP]!=null) shape(bg[i],0,0); 
    //    }
   
      SIM.addChild(bg[NP]);
      //pgDrawing.shape(SIM);
      //pgDrawing.endShape();
      pgDrawing.endDraw();
      pgDrawing.dispose();
      pgDrawing.beginDraw();
      pgDrawing.beginShape();
     // shape(SIM);
       for (int i=1;i<NP;i++)
        {   shape(SIM.getChild(i),0,0); 
      }//
      NP++;
      PVector v=new PVector (0,0);
      for (int i = 0; i < SIM.getChild(0).getVertexCount(); i++) {
      v = SIM.getChild(0).getVertex(i);
      //println((v.x-(width/2))/4000-pos_ee.x, ((height/5)+v.y)/4000-pos_ee.y);
       //println(pos_ee.x*4000,pos_ee.y*4000);
      }
     tst=createShape();
     tst.beginShape();
}
void mouseP(){
  if (mousePressed)
  {
    if (mouseButton==LEFT){
   
      
      //pgDrawing.beginShape();
     // pgDrawing.vertex(mouseX, mouseY);
      stroke(126);
      tst.vertex(mouseX,mouseY);
      //line(mouseX,mouseY,pmouseX,pmouseY);
      
      flag=true;
  }else if (mouseButton==RIGHT)
    { float x_old=mouseX;
      float y_old=mouseY;
      for (int i=1;i<NP;i++)
      {
        color TS=color(100,100,100);
        bg[i].setFill(TS); 
        shape(bg[i]); 
        color c=get(mouseX,mouseY);
        bg[i].setFill(255);
        shape(bg[i]);
        if (TS==c){
          //println("yes");
          selected=i;
          //println(selected);
          bg[i].translate(mouseX-x_old,mouseY-y_old);
          x_old=mouseX;
          y_old=mouseY;
          bg[selected].setFill(100);
          shape(bg[selected]);
          }else{

          }
      }

      
    }

  }
}
/**********************************************************************************************************************
 * Haptics simulation event, engages state of physical mechanism, calculates and updates physics simulation conditions
 **********************************************************************************************************************/ 
void onTickEvent(CountdownTimer t, long timeLeftUntilFinish){
  
  if (haply_board.data_available()) {
    /*** GET END-EFFECTOR POSITION (TASK SPACE)****/
    angles.set(haply_2DoF.get_device_angles());
    
    pos_ee.set( haply_2DoF.get_device_position(angles.array()));
 
    pos_ee=angles;
    pos_ee.set(device2graphics(pos_ee));
    vel_ee.set(pos_ee.copy().sub(pos_ee_last)).div(dt); 
    pos_ee_last.set(pos_ee.copy()); 
    //pos_ee.mult(1000); 
    
    /*** PHYSICS OF THE SIMULATION ****/
    f_wall.set(0, 0); 

    //pen_wall.set((pos_wall.x - (pos_ee.x-r_ee)), 0); 
    
    //if (pen_wall.x > 0) {
    //  r_ee_contact= r_ee- pen_wall.x; 
    //  if (abs(r_ee_contact)>r_ee) r_ee_contact= r_ee;
    //  f_wall = f_wall.add((pen_wall.mult(-k_wall))).add(vel_ee.copy().mult(b_wall));
    //}

    //f_ee = (f_wall.copy()).mult(-1); 
    //f_ee.set(graphics2device(f_ee));
  }

for (int i=0;i<NP;i++){
        if (bg[i]!=null){
        for (int j = 0; j < bg[i].getVertexCount(); j++) {
        SWall.set(bg[i].getVertex(j));
        pen_wall.set((pos_ee.x)-(SWall.x-(width/2))/4000,(pos_ee.y)-(SWall.y-(height/5))/4000);
        
        if (abs(sqrt(pow((pen_wall.x),2)+pow((pen_wall.y),2)))<r_ee){
          contact=true;
            if(abs(pen_wall.x)<2*r_ee){
              //f_wall.x=f_wall.x+pen_wall.x*-k_wall+vel_ee.x*b_wall;
              f_wall.x=pen_wall.x*-k_wall;
            }
            if(abs(pen_wall.y)<2*r_ee){
              //f_wall.y=f_wall.y+pen_wall.y*-k_wall+vel_ee.y*b_wall;
              f_wall.y=pen_wall.y*k_wall;
            }
        }else{
          //f_ee.set(0,0);
          //contact=false;
        }
        
        
        
        
        //pen_wall.set((SWall.x-(width/2))/4000-(pos_ee.x-r_ee),(SWall.y-(height/5))/4000-(pos_ee.y-r_ee));
        //  if (pen_wall.x > 0 & pen_wall.x < 2* r_ee_contact & pen_wall.y> 0 & pen_wall.y< 2* r_ee_contact  ) {  
        //r_ee_contact= sqrt(pow((r_ee- pen_wall.x),2)+pow((r_ee- pen_wall.y),2)); 
        //if (abs(r_ee_contact)>r_ee) r_ee_contact= r_ee;
        //f_wall = f_wall.add((pen_wall.mult(-k_wall))).add(vel_ee.copy().mult(b_wall));}

        }
}
}

    f_ee = (f_wall.copy()).mult(-1); 
    f_ee.set(graphics2device(f_ee));
        

  haply_2DoF.set_device_torques(f_ee.array());
  torques.set(haply_2DoF.mechanisms.get_torque());
  
  haply_2DoF.device_write_torques();
}


/* Graphical and physics functions ************************************************************************************/

/**
 * Specifies the parameters for a haply_2DoF pantograph animation object
 */
void createpantograph() {
  float r_ee_ani = pixelsPerMeter*r_ee; 
  handle = createShape(ELLIPSE, 0, 0, 2*r_ee_ani, 2*r_ee_ani);
  handle.setStroke(color(0));
  strokeWeight(5);
}


/**
 * Specifies the parameters for static wall animation object
 */
PShape createWall(float x1, float y1, float x2, float y2){
  
  /* modify wall parameters to fit screen */
  x1= pixelsPerMeter*x1; 
  y1= pixelsPerMeter*y1; 
  x2=pixelsPerMeter*x2; 
  y2=pixelsPerMeter*y2; 
  
  return createShape(LINE, device_origin.x+x1, device_origin.y+y1, device_origin.x+x2, device_origin.y+y2);
}


/**
 * update animations of all virtual objects rendered 
 */
void update_animation(float th1, float th2, float x_E, float y_E,boolean contact){
  
  /* To clean up the left-overs of drawings from the previous loop */
  background(255); 
  shape(SIM);
  /* modify virtual object parameters to fit screen */
  x_E = pixelsPerMeter*x_E; 
  y_E = pixelsPerMeter*y_E; 
  th1= 3.14-th1; 
  th2 = 3.14- th2; 
  float l_ani = pixelsPerMeter*l; 
  float L_ani = pixelsPerMeter*L; 
  float d_ani = pixelsPerMeter*d; 
  
  /* Vertex A with th1 from encoder reading */
 // pantograph.setVertex(1,device_origin.x+l_ani*cos(th1), device_origin.y+l_ani*sin(th1));
  
  /* Vertex B with th2 from encoder reading */
  //pantograph.setVertex(3,device_origin.x-d_ani+l_ani*cos(th2), device_origin.y+l_ani*sin(th2)); 
  
  /* Vertex E from Fwd Kin calculations */
  //pantograph.setVertex(2,device_origin.x+x_E, device_origin.y+y_E); 
  

  /* Display the virtual objects with new parameters */
  //shape(pantograph); 
  //shape(joint1);
  //shape(joint2); 
  //shape(wall );
 
  pushMatrix(); 
  translate(device_origin.x, device_origin.y); 
  shape(car, x_E-40, y_E-10, 1.5*r_ee*pixelsPerMeter, 2*r_ee*pixelsPerMeter); 

  if (contact){ shape(accident,x_E, y_E, 2*r_ee*pixelsPerMeter, 3*r_ee*pixelsPerMeter);}
    
  stroke(0); 
  popMatrix(); 
}


/**
 * translates from device frame of reference to graphics frame of reference
 */
PVector device2graphics(PVector deviceFrame){
   
  return deviceFrame.set(-deviceFrame.x, deviceFrame.y);  
}
 
 
/**
 * translates from graphics frame of reference to device frame of reference
 */ 
PVector graphics2device(PVector graphicsFrame){
  
  return graphicsFrame.set(-graphicsFrame.x, graphicsFrame.y); 
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
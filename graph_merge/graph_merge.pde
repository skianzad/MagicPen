import org.quark.jasmine.*;
import java.util.regex.Pattern;
import controlP5.*;
import grafica.*;
import processing.serial.*;
import com.dhchoi.CountdownTimer;
import com.dhchoi.CountdownTimerService;

int graphSize;  // Width and height of graph in pixels.

// Input box fields//

int state = 0; //initialize these

String x_upper_bd = "2.0";
String x_lower_bd = "-2.0";
String custom_fn = ""; //string that comes in as custom function

String result = custom_fn;

String curr_fn; //holds function that is currently being rendered

//Position of buttons and other UI stuff//

int xoffset = 40; //by default graphlists dropdown will be at this offset position
int yoffset = 40;
int button_width = 250;
int button_height = 40;
int margin = 20;
int slider_height = 20;
int textbox_width = button_width;
int textbox_height = button_height+margin;
int small_button_width = button_width/2-5;


int cf_text_x = xoffset+button_width; // this is where the "custom function" text should go
int cf_text_y = button_height+yoffset+2*margin;

int textbox_x = xoffset; //custom function text box
int textbox_y = cf_text_y + margin+10;

int slider1_x = xoffset; //NumberPoints
int slider1_y = textbox_y + textbox_height + 2*margin;

int slider2_x = xoffset; //Delaytime
int slider2_y = slider1_y + slider_height+5;

int slider3_x = xoffset; //MaxSpeed
int slider3_y = slider2_y + slider_height+5;

int lowbd_x = slider3_x; //position of low bound on x text box
int lowbd_y = slider3_y + slider_height + 2*margin;

int upbd_x = lowbd_x + small_button_width+10; //10 is the margin
int upbd_y = lowbd_y;

int run_x = xoffset;
int run_y = lowbd_y + button_height + 3*margin;

int stop_x = xoffset;
int stop_y = run_y + button_height + margin;

// Params for graph that are controllable within UI //

int        NumberPoints = 200; //Number of points
//float      xSpace = 0.02;          //linespace between each point
float      Xintital = Float.parseFloat(x_lower_bd);
float Xfinal = Float.parseFloat(x_upper_bd);
float xSpace = (Xfinal - Xintital)/NumberPoints;
float      MaxSpeed = 50;
int        Delaytime = 5;

boolean doneDriving; //are we done doing the "drives your hand" portion?
PVector initialPosition; //position of the pen in graph coordinates, changes exactly as expected
PVector penVel_gc = new PVector(0, 0); //pen velocity in graph coords
PVector pos_curr_gc = new PVector(0, 0); //current position in graph coords
PVector pos_old_gc = new PVector(0, 0);  //old position in graph coords
int draw_count = 0;


void setup(){
  size(1000,600,P2D);
  origin.set(xoffset+button_width ,yoffset-button_height);
  textFont(loadFont("AdobeHeitiStd-Regular-24.vlw"));
  textAlign(RIGHT,TOP);
  cp5=new ControlP5(this);
  xPoints=new FloatList();
  yPoints=new FloatList();
  lastStepTime=millis();
  doneDriving = false;
  
  initialPosition = new PVector(0, 0); //set initial position
  
  avatar.add(0,0,0);
  haply_board = new Board(this,"COM4", 0); //Put your COM# port here

  /* DEVICE */
  haply_2DoF = new Device(degreesOfFreedom.HaplyTwoDOF, deviceID, haply_board);
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();

  d1=cp5.addDropdownList("Graph lists") //types of graphs that can be drawn
       
       .setPosition(xoffset, yoffset)
       .setFont(loadFont("AdobeHeitiStd-Regular-22.vlw"))
       ;
       customize(d1);
       d1.setValue(3);// customize the first list
       
   
  S1=cp5.addSlider("NumberPoints") // slider for number of points
     .setPosition(slider1_x, slider1_y)
     .setRange(100,500)
     .setSize(button_width,slider_height)
     .setValue(200)
     .setLabel("# points")
     //.setNumberOfTickMarks(7)
     .setSliderMode(Slider.FLEXIBLE)
     .setFont(loadFont("AdobeHeitiStd-Regular-18.vlw"))
     .setColorBackground(color(44, 86, 110));
     ;
     
   S2=cp5.addSlider("Delaytime") //delay time between each dot being drawn. Delaytime is the field that's being controlled by the slider
     .setPosition(slider2_x, slider2_y)
     .setRange(1,50)
     .setSize(button_width,slider_height)
     .setColorLabel(255)
     .setLabel("Delay time") //set the label
     .setValue(10) //initial position of slider
     //.setNumberOfTickMarks(7)
     .setSliderMode(Slider.FLEXIBLE)
     .setFont(loadFont("AdobeHeitiStd-Regular-18.vlw")) //for fonts: make a font in tools first, then copy paste the file name
     .setColorBackground(color(44, 86, 110));
     ;
   S3=cp5.addSlider("MaxSpeed") //delay time between each dot being drawn. Delaytime is the field that's being controlled by the slider
     .setPosition(slider3_x,slider3_y)
     .setRange(1,80)
     .setSize(button_width,slider_height)
     .setColorLabel(255)
     .setLabel("Max speed") //set the label
     .setValue(50) //initial position of slider
     //.setNumberOfTickMarks(7)
     .setSliderMode(Slider.FLEXIBLE)
     .setFont(loadFont("AdobeHeitiStd-Regular-18.vlw")) //for fonts: make a font in tools first, then copy paste the file name
     .setColorBackground(color(44, 86, 110));
     ;
     
  cp5.addTextfield("x_lower_bd")
     .setPosition(lowbd_x,lowbd_y)
     .setSize(small_button_width,button_height)
     .setFont(createFont("arial",18))
     .setAutoClear(false)
     .setColorBackground(color(240, 240, 240))
     .setColorLabel(0)
     .setLabel("  x lower bound")
     .setText("-2.0") 
     .setColorValueLabel(0)
     ;
     
  cp5.addTextfield("x_upper_bd")
     .setPosition(upbd_x, upbd_y)
     .setSize(small_button_width,button_height)
     .setFont(createFont("arial",18))
     .setAutoClear(false)
     .setColorBackground(color(240, 240, 240))
     .setColorLabel(0)
     .setLabel("  x upper bound")
     .setText("2.0")      
     .setColorValueLabel(0)
     ;
     
  cp5.addTextfield("custom_fn")
     .setPosition(textbox_x, textbox_y)
     .setSize(textbox_width,textbox_height)
     .setFont(createFont("arial",24))
     .setAutoClear(false)
     .setColorBackground(color(240, 240, 240))
     .setColorValueLabel(0)
     ;
   
     
     cp5.getController("Delaytime").getCaptionLabel().align(ControlP5.RIGHT, ControlP5.TOP).setPaddingX(0); //setting the caption locn for sliders
     cp5.getController("NumberPoints").getCaptionLabel().align(ControlP5.RIGHT, ControlP5.TOP).setPaddingX(0);
     cp5.getController("MaxSpeed").getCaptionLabel().align(ControlP5.RIGHT, ControlP5.TOP).setPaddingX(0);
     
  cp5.addButton("RUN")
     .setValue(0)
     .setPosition(run_x, run_y)
     .setSize(button_width,button_height)
     .setColorBackground(color(112, 146, 181))
     .setFont(loadFont("AdobeHeitiStd-Regular-24.vlw"))
     ;
  

  cp5.addButton("STOP")
     .setValue(100)
     .setPosition(stop_x,stop_y)
     .setSize(button_width,button_height)
     .setColorBackground(color(166, 66, 66))
     .setFont(loadFont("AdobeHeitiStd-Regular-24.vlw"))
     ;
  Xvalues();
  Yvalues(X);
  Graphing(X,Y);
  flag=true;
  
  
  offset.set(pos_ee.copy());
}


void customize(DropdownList d1) {
  // a convenience function to customize a DropdownList
  d1.setBackgroundColor(color(153, 153, 102));
  d1.setItemHeight(button_height+15);
  d1.setBarHeight(button_height-5+15);
  d1.setWidth(button_width);
  d1.setOpen(false);
    d1.addItem("Absolute ", 0);
    d1.addItem("Quadratic",1);
    d1.addItem("Sin",2);
    d1.addItem("Custom",3);
  d1.setColorBackground(color(255, 181, 181));
  d1.setColorActive(color(179, 114, 119));
   d1.setHeight((button_height+15)*2);
   d1.setScrollSensitivity(500.0f); //lower probably means less sensitive, but I can't be sure
}

void controlEvent(ControlEvent theEvent) { //called when a textbox is changed and enter is pressed
  if (theEvent.isGroup()) {
    // check if the Event was triggered from a ControlGroup
    //println("event from group : "+theEvent.getGroup().getValue()+" from "+theEvent.getGroup());
    
  } 
  else if (theEvent.isController()) {
    //println("event from controller : "+theEvent.getController().getValue()+" from "+theEvent.getController());
    //println("x_lower_bd: ", x_lower_bd);
    //println("x_upper_bd: ", x_upper_bd);
    X=new float[NumberPoints];    
    Xvalues();
    }
}


GPoint calculatePoint(float i) {
  float n=0.0;
  n=Yvalues(i);
  return new GPoint(i, n);
}


float[] Yvalues(float[] X){
 for (int x = 0; x < X.length; x++) {
   Y[x]=cos(2*3.4*X[x]);
 }
 return Y;
}

float Yvalues(float temPointx){
   int graphNumber=int(d1.getValue());
   float temPointy;
   switch (graphNumber){
       case 0:
             temPointy=abs(temPointx);
             curr_fn = "abs(temPointx)";
       break;
       case 1:
            temPointy=(temPointx*temPointx);
            curr_fn = "temPointx*temPointx";
       break;
       case 2:
            temPointy=(sin(3.4*temPointx));
            curr_fn = "sin(3.4*temPointx)";
       break;
       case 3:
            temPointy =Yvalues(new Function(temPointx));
            curr_fn = custom_fn;
       break;
       default:
            temPointy=(sin(2*3.4*temPointx));
            curr_fn = "sin(2*3.4*temPointx)";
       break;
   }
   
   return temPointy;
}

float Yvalues(Function f) {
  if (!result.equals("")) {
   return f.computeY(result);
  }
  else {
    return sin(3*f.x);
  }
}


public void RUN(){ //called when the "run" button is pressed
    //println("RUN called");

  if (!Function.valid(result) && (int(d1.getValue()) == 3)) {
    //do nothing if the typed field is empty and custom is selected
    //println("don't do anything");
  }
  else {
 // println("RUN called");
  if (flag){
    println("flag is true");
    delay(100);
    Graphing(X,Y);
    step=0;
    run=true;
    doneDriving = true;
   }
  }
}

public void STOP(){ //called when "stop" button is pressed
  Graphing(X,Y);
  run=false;
  Velocity.set(0,0);
  //result = "";
  state = 0;
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


ControlP5  cp5;
DropdownList d1,d2,d3;
Slider     S1,S2,S3;
//int        NumberPoints=400; //Number of points
//float      xSpace=0.01;          //linespace between each point
//float      Xintital=-2.0;
//float      Delta=1.0;                        
float[]    X=new float[NumberPoints];       
float[]    Y=new float[NumberPoints];

FloatList  xPoints;
FloatList  yPoints;
int        sliderValue = 100;
int        sliderTicks1 = 100;
int        sliderTicks2 = 30;
//int        Delaytime=5;
boolean    flag=false;
boolean    run=false;
int        lastStepTime=          0; 
PVector    Velocity =             new PVector(0,0); 
PVector    Position =             new PVector(0,0);
PVector    oldPosition=           new PVector(0,0);
PVector    penVelocity=           new PVector(0,0);
PVector    offset=                new PVector(0,0);
PVector    deltaPosition=          new PVector(0,0);
//float      MaxSpeed=              3;
GPointsArray avatar=new GPointsArray(1);

// Graph details
static final float RADIUS=15;      // Size of animated discs in pixels.
//static final int graphSize = 400;  // Width and height of graph in pixels.
GPlot      lineChart;
PVector    origin = new PVector(0,0);
Slider     Speed;
int        step=0;
int        stepsPerCycle=100;
/* generic data for a 2DOF device */
/* joint space */
PVector           angles                    = new PVector(0, 0);
PVector           torques                   = new PVector(0, 0);

/* task space */
PVector           pos_ee                    = new PVector(0, 0);
PVector           pos_ee_last               = new PVector(0, 0); 
PVector           f_ee                      = new PVector(0, 0); 



void keyPressed() {

}

void draw() {  
  
  graphSize = 3*height/4;
  lineChart.setDim(graphSize*1.3, graphSize);
  
  Xintital = Float.parseFloat(x_lower_bd);
  Xfinal = Float.parseFloat(x_upper_bd);
  result = custom_fn;
  
  //println("X_i = ", Xintital, "X_f = ", Xfinal);
  //println(result);
  xSpace = (Xfinal - Xintital)/NumberPoints;
  Xvalues();
  
  
  background(255);
  lineChart.beginDraw();
  lineChart.drawBackground();
  lineChart.drawBox();
  lineChart.drawXAxis();
  lineChart.drawYAxis();
  lineChart.drawTopAxis();
  lineChart.drawRightAxis();
  lineChart.drawTitle();
  lineChart.getMainLayer().drawPoints();
  lineChart.getLayer("surface").drawPoints();
  lineChart.getLayer("surface").setPointColor(color(100, 100, 255));
  lineChart.drawLines();
  lineChart.endDraw();
  forceCommand();

  if (run){
      if (millis() - lastStepTime > Delaytime) {
          if (step<NumberPoints){
          // Add the point at the end of the array
              lineChart.addPoint(0,calculatePoint(X[step]));
              if(step!=NumberPoints-1&step!=0){
                float DY=tangent(Yvalues(X[step-1]),Yvalues(X[step]),Yvalues(X[step+1]),xSpace);
                float DX=xSpace;
                updateVelocity(DX,DY);
                //println(Velocity.x,Velocity.y);
                Position.set(pos_ee.x,pos_ee.y);
                penVelocity.set(1*(Position.x-oldPosition.x)/Delaytime,1*(Position.y-oldPosition.y)/Delaytime);
                //println("PenVel",penVelocity);
                step++;
                oldPosition.set(Position.x,Position.y);
                lineChart.getLayer("surface").removePoint(0);
                lineChart.getLayer("surface").addPoint(0,calculatePoint(X[step]));
                // Remove the first point
                //lineChart.getLayer("surface").removePoint(0);
              }else{
                Velocity.set(0,0);
                penVelocity.set(0,0);
                step++;
                //offset.y=-pos_ee.y+offset.y+Yvalues(X[NumberPoints-1]);

               
                
              }
         // Remove the last point
         // lineChart.removePoint(lineChart.getPointsRef().getNPoints() - 1);
        lastStepTime = millis();
        }else{
            offset.set(pos_ee.copy());
            run=false;
          }
      }
  }else{  
     //if (millis() - lastStepTime > 1) {
         lineChart.getLayer("surface").removePoint(0);
         int range=NumberPoints+round(4*(-pos_ee.x+offset.x));
         
         float yval = (Yvalues(X[NumberPoints-1])+(-pos_ee.y+offset.y)/20);
         // /19.567793+1.89286209; //for "initial position" (aka the position of the pen on the graph)
         
         if (range<=0){
             range=1;
             lineChart.getLayer("surface").addPoint(0,new GPoint(X[range],Yvalues(X[NumberPoints-1])+(-pos_ee.y+offset.y)/20));
             initialPosition.set(X[range], yval); //trying to get the position
             deltaPosition.set(0,0);
             penVelocity.set(0,0);
             
             //initialPosition.set(X[range],(Yvalues(X[NumberPoints-1])+(-pos_ee.y+offset.y))*8); //trying to get the position
         }
         else if(range<NumberPoints){
               lineChart.getLayer("surface").addPoint(0,new GPoint(X[range],Yvalues(X[NumberPoints-1])+(-pos_ee.y+offset.y)/20));
                deltaPosition.set(0,Yvalues(X[range])-Yvalues(X[NumberPoints-1])-(-pos_ee.y+offset.y)/20);
                //println("delta",deltaPosition);
                //Calcukating the pen velocity
                initialPosition.set(X[range], yval); //trying to get the position
                Position.set(pos_ee.x,pos_ee.y);
                //penVelocity.set(7*(Position.x-oldPosition.x)/1,7*(Position.y-oldPosition.y)/1);
                penVelocity.set(1*(Position.x-oldPosition.x)/1,1*(Position.y-oldPosition.y)/1);
                oldPosition.set(Position.x,Position.y);
                
                if (draw_count % 5 == 0) {
                
                pos_curr_gc.set(initialPosition.x, initialPosition.y); //updating velocity in graph coordinates this time.
                penVel_gc.set(pos_curr_gc.x-pos_old_gc.x, pos_curr_gc.y-pos_old_gc.y);
                pos_old_gc.set(pos_curr_gc.x, pos_curr_gc.y);
                
                //println("penVel_gc: ", penVel_gc);
                
                
                }
                draw_count++;
               
               
         }else{
               range=NumberPoints-1;
               lineChart.getLayer("surface").addPoint(0,new GPoint(X[range],Yvalues(X[NumberPoints-1])+(-pos_ee.y+offset.y)/20));
               
               initialPosition.set(X[range],yval); //trying to get the position
               deltaPosition.set(0,0);
               penVelocity.set(0,0);
               
               
               
         }
         lineChart.getLayer("surface").setPointColor(color(100, 100, 255));
         Position.set(pos_ee.x,pos_ee.y);
        
       // oldPosition.set(Position.x,Position.y);
         //println(pos_ee.sub(offset),deltaPosition);
        lastStepTime = millis();
        }
 //   }
 
 //println("f_ee: ", f_ee);
 //println("curr_fn:", curr_fn);
 //println("run = ", run);
 //println("supposed position of pen: ", initialPosition);
 //println("pos_ee: ", pos_ee);
 //println("penvelocity: ", penVelocity);
  
}



public void Graphing(float[] X,float[] Y)
{
  lineChart = new GPlot(this);
  println(origin.x);
  lineChart.setPos(origin.x, origin.y);
  lineChart.setDim(graphSize*1.3, graphSize);
  // Set the plot limits (this will fix them)
  //lineChart.setXLim(-1.2*scale, 1.2*scale);
  //lineChart.setYLim(-1.2*scale, 1.2*scale);
  lineChart.activateZooming(1.3, CENTER, CENTER);
  // Set the plot title and the axis labels
  lineChart.setTitleText("Clockwise movement");
  lineChart.getXAxis().setAxisLabelText("x axis");
  lineChart.getYAxis().setAxisLabelText("y axis");
 
  lineChart.activatePanning(); // Activate the panning effect

  // Add the two set of points to the plot
  GPointsArray Xpoints=new GPointsArray(NumberPoints);
  
  //Xpoints.add(X);
  //lineChart.setPoints(X);
  lineChart.addLayer("surface", avatar);

  // Change the second layer line color
  //lineChart.getLayer("surface").setLineColor(color(100, 255, 100));
    lineChart.activateReset();

}
void Xvalues(){
  X[0]=Xintital;
  for(int i=1;i<NumberPoints;i++){
     X[i]=xSpace+X[i-1];
  }
  
}



public float tangent(float y_b,float y,float y_a,float h){ 
  float Ygradient=0; 
  Ygradient=(((y_a-y)/h)+((y-y_b)/h))/2;
  //println("gradient",Ygradient);
  return Ygradient;
}

/** this controls the forces to the pen. There are 2 models that determine the force. **/

void forceCommand(){
 if (run==true){ //if the pen is driving your hand
   f_ee.set(10*(Velocity.x-penVelocity.x),10*(Velocity.y-penVelocity.y));
  }else if(run==false && doneDriving){ //doneDriving means the driving portion is done. it is set to true as soon as the run is set to true.
                 
   //f_ee.set(0,deltaPosition.y*(-10)-penVelocity.y*(.02)); //spring model
   //println("penVelocity",deltaPosition.y);
   if (curr_fn != null && !curr_fn.equals("")) {
   
   //println("initialPosition: ", initialPosition);
   
   PVector cp = closestPerp(curr_fn, initialPosition); //finding closest perpendicular
   
   PVector force = getForce(initialPosition, cp, curr_fn); //wall model
   //force.add(getDriveForce(initialPosition, cp, curr_fn)); //add a driving force
   
   f_ee.set(-force.x, -force.y);
   //f_ee.set(0, 0);
   //println("computed force: ", force);
   
   }
   else {f_ee.set(0, 0); }
  
  }else{
    f_ee.set(0,0);
  }



}


void onTickEvent(CountdownTimer t, long timeLeftUntilFinish){
  

   
  if (haply_board.data_available()) {
    /* GET END-EFFECTOR STATE (TASK SPACE) */
        
    angles.set(haply_2DoF.get_device_angles()); 
    pos_ee.set( haply_2DoF.get_device_position(angles.array()));
    pos_ee.set(pos_ee.copy().mult(100)); 
    
  }


 
 
  //f_ee.div(1); //
  //println(f_ee);
  haply_2DoF.set_device_torques(f_ee.array());
  torques.set(haply_2DoF.mechanisms.get_torque());
  haply_2DoF.device_write_torques();
  

}


public void updateVelocity(float Vx,float Vy){
   float Vscale=Vy;
    if ((Vscale)>=0){
        Velocity.set(-MaxSpeed/sqrt(1+Vscale*Vscale),-MaxSpeed/sqrt(1+1/(Vscale*Vscale)));
      }else{
        Velocity.set(-MaxSpeed/sqrt(1+Vscale*Vscale),MaxSpeed/sqrt(1+1/(Vscale*Vscale)));
      }

}

/* Timer control event functions **************************************************************************************/

/**
 * haptic timer reset
 */
//void onFinishEvent(CountdownTimer t){
//  println("Resetting timer...");
//  haptic_timer.reset();
//  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
//}

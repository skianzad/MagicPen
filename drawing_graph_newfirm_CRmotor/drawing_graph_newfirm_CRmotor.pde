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

String x_upper_bd = "5.0";
String x_lower_bd = "-5.0";
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

// For driving //

boolean doneDriving; //are we done doing the "drives your hand" portion?
PVector currentPosition; //position of the pen in graph coordinates, changes exactly as expected
PVector penVel_gc = new PVector(0, 0); //pen velocity in graph coords
PVector pos_curr_gc = new PVector(0, 0); //current position in graph coords
PVector pos_old_gc = new PVector(0, 0);  //old position in graph coords
int draw_count = 0; //how many times draw is called
boolean forceDrive = true; //what kind of drive for the graph
ArrayList<PVector> PDpts = new ArrayList(); //these are the points that are a part of the graph
PVector pos_ee_initial = new PVector(0, 0); //initial when the program is loaded up

PVector oldVelocity = new PVector(0, 0); //for acceleration calculation
PVector currVelocity = new PVector(0, 0);
PVector acceleration = new PVector(0, 0);

/* Device block definitions ********************************************************************************************/
Device            widgetOne, widgetTwo;
byte              widgetOneID                     = 4;
byte              widgetTwoID                     = 5;

Board             haplyBoard1, haplyBoard2;
Mechanisms        pantograph1, pantograph2;
boolean           rendering_force                 = false;
int               CW = 1;
int               CCW = 0;
//long              baseFrameRate = 60;
float[] taus = new float[2];    //drawing forces

/* Simulation Speed Parameters ****************************************************************************************/
final long        SIMULATION_PERIOD          = 1; //ms
final long        HOUR_IN_MILLIS             = 36000000;
CountdownTimer    haptic_timer;
float             dt                        = SIMULATION_PERIOD/1000.0; 
/* joint space */
PVector anglesA = new PVector(0, 0);
PVector torquesA = new PVector(0, 0);
/* task space */
PVector pos_eeA = new PVector(0, 0);
PVector pos_ee_lastA = new PVector(0, 0);
PVector f_eeA = new PVector(0, 0);

/**********************************************************************************************************************/
/* Saving the sensor data *********************************************************************************************************************/
//ExBoard           experimentalBoard;
Serial            portEx;
StringList TimeStamp;
StringList SenData;
StringList XData;
StringList YData;
StringList STime;
float inByte = 0;
int COND;
float twangle=0;
/********************************************************************************************/

ControlP5  cp5;
DropdownList d1,d2,d3;
Slider     S1,S2,S3;
//int        NumberPoints=400; //Number of points
//float      xSpace=0.01;          //linespace between each point
//float      =-2.0;
//float      Delta=1.0;                        
float[]    X=new float[NumberPoints];       //x values
float[]    Y=new float[NumberPoints];       //y values

// Position drive, which point to attract to //
int PDStep = 1;


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

/***********************************************************************************************************************************/

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
  
  
  
  currentPosition = new PVector(0, 0); //set initial position
  
  avatar.add(0,0,0);
  //haply_board = new Board(this,"COM3", 0); //Put your COM# port here
  //portEx = new Serial(this,"COM4", 57600);
  /* DEVICE */
  
  haplyBoard1 = new Board(this, "COM5", 0);
 // haplyBoard2 = new Board(this, "COM3", 0);
  
  pantograph1 = new Pantagraph();
  pantograph2 = new Pantagraph();
  
  widgetOne = new Device(widgetOneID, haplyBoard1);
  widgetOne.set_mechanism(pantograph1);
  widgetOne.add_actuator(1, CW, 1);
  widgetOne.add_actuator(2, CCW, 2);
  widgetOne.add_encoder(1, CW, 180, 13824, 1);
  widgetOne.add_encoder(2, CCW, 0, 13824, 2);
  widgetOne.device_set_parameters();
  
  //widgetTwo = new Device(widgetTwoID, haplyBoard2);
  //widgetTwo.set_mechanism(pantograph1);
  //widgetTwo.add_actuator(1, CW, 1);
  //widgetTwo.add_actuator(2, CCW, 2);
  //widgetTwo.add_encoder(1, CW, 180, 13824, 1);
  //widgetTwo.add_encoder(2, CCW, 0, 13824, 2);
  //widgetTwo.device_set_parameters();
  
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
     .setLabel("  x l bound")
     .setText(x_lower_bd) 
     .setColorValueLabel(0)
     ;
     
  cp5.addTextfield("x_upper_bd")
     .setPosition(upbd_x, upbd_y)
     .setSize(small_button_width,button_height)
     .setFont(createFont("arial",18))
     .setAutoClear(false)
     .setColorBackground(color(240, 240, 240))
     .setColorLabel(0)
     .setLabel("  x u bound")
     .setText(x_upper_bd)      
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
  //println(pos_ee);
  

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
  pos_ee_initial.set(pos_ee.x, pos_ee.y);
}

void controlEvent(ControlEvent theEvent) { //called when a textbox is changed and enter is pressed
  if (theEvent.isGroup()) {
    // check if the Event was triggered from a ControlGroup
    //println("event from group : "+theEvent.getGroup().getValue()+" from "+theEvent.getGroup());
    
  } 
  else if (theEvent.isController()) {
    //println("event from controller : "+theEvent.getController().getValue()+" from "+theEvent.getController());
    X=new float[NumberPoints];    
    Xvalues();
    }
}


GPoint calculatePoint(float i) {
  float n=0.0;
  n=Yvalues(i);
  return new GPoint(i, n);
}

// Don't use this one...//
float[] Yvalues(float[] X){
 for (int x = 0; x < X.length; x++) {
   Y[x]=cos(2*3.4*X[x]);
 }
 return Y;
}

// This function is correct //

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
            temPointy=(sin(temPointx));
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
   
    Graphing(X,Y);
    step=0;
    doneDriving = true;
   //Experimental board saving data.
   // portEx.clear();
    delay(100);
    delay(2000);
   // portEx.write('a');
    println("runn");
    TimeStamp=new StringList();
    SenData=new StringList();
    XData=new StringList();
    YData=new StringList();
    
    run=true;
   }
  }
  
  //updatePDpts();
  pos_ee_initial = pos_ee.copy();
}

public void STOP(){ //called when "stop" button is pressed
  Graphing(X,Y);
  run=false;
  Velocity.set(0,0);
  //result = "";
  state = 0;
  pos_ee_initial = pos_ee.copy();
   Graphing(X,Y);
  run=false;
  Velocity.set(0,0);
  //result = "";
  state = 0;
  //Experimental board saving data
     //portEx.clear();
     //delay(100);
     //portEx.write('b');
     String[] Result=TimeStamp.array();
     String TimeSave=join(Result,",");
     String[] list = split(TimeSave, ' ');
     saveStrings("Time.txt",list);
     String[] Sensor=SenData.array();
     String SensSave=join(Sensor,",");
     String[] list1 = split(SensSave, ' ');
     saveStrings("Sens.txt",list1);
     Sensor=XData.array();
     SensSave=join(Sensor,",");
     list1 = split(SensSave, ' ');
     saveStrings("X.txt",list1);
     println(list1);
     Sensor=YData.array();
     SensSave=join(Sensor,",");
     list1 = split(SensSave, ' ');
     saveStrings("Y.txt",list1);
     println(list1);
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






void draw() {  
  
  //println(pos_ee);
  
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

  if (run){
      if (millis() - lastStepTime > Delaytime) {
          if (step<NumberPoints){
          // Add the point at the end of the array
              //lineChart.addPoint(0,calculatePoint(X[step]));
              if(step!=NumberPoints-1&step!=0){
                float DY=tangent(Yvalues(X[step-1]),Yvalues(X[step]),Yvalues(X[step+1]),xSpace);
                float DX=xSpace;
                //updateVelocity(DX,DY);
                //println(Velocity.x,Velocity.y);
               // Position.set(pos_ee.x,pos_ee.y);
                //penVelocity.set(1*(Position.x-oldPosition.x)/Delaytime,1*(Position.y-oldPosition.y)/Delaytime);
                //println("PenVel",penVelocity);
                step++;
                //oldPosition.set(Position.x,Position.y);
              //  lineChart.getLayer("surface").removePoint(0);
                //lineChart.getLayer("surface").addPoint(0,calculatePoint(X[step]));
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
            //run=false;
          }
      }
  }
  
        
        //println("pos_ee ", pos_ee);
        //println("velocity: ", penVelocity);
        //println("accel: ", acceleration)
        
        // now, currentPosition actually has the pos_ee but in graph scale. here we are updating currentPosition field
        
        float K = 0.1;
        
        currentPosition.set(0, 0);
        currentPosition.sub(pos_ee_initial.copy().mult(K)).add(pos_ee.copy().mult(K)).add(Xintital, Yvalues(Xintital));
        //println("currentPosition: ", currentPosition);
        //println("pos_ee_initial: ", pos_ee_initial);
        lineChart.addPoint(currentPosition.x,currentPosition.y);
        
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

// initialize the array X, which holds the X-values for the graph
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

/** this controls the forces to the pen. Currently there is one model of control: position tracking. **/

// constants
float C1 = 0.5; //position
float C2 = 0; //velocity
float C3 = 0.00003; //acceleration
float thresh = 0.5;

void forceCommand(){
 if (run==true && currentPosition.x <= Xfinal){ //if the pen is driving your hand, using tangent-force drive
 
    float yval = Yvalues(currentPosition.x);
    PVector tangentForce = new PVector(currentPosition.x + 0.01, Yvalues(currentPosition.x+0.01));
    tangentForce.sub(new PVector(currentPosition.x, Yvalues(currentPosition.x)))
                .normalize()
                .mult(.5);
    //println("tangentForce: ", tangentForce);
    f_ee.x=tangentForce.x;
    f_ee.y=tangentForce.y;
    println("tangentForce: ", f_ee);
 
   }
   
  else { 
    f_ee.set(0, 0);
}
}


void onTickEvent(CountdownTimer t, long timeLeftUntilFinish){

  forceCommand();
  
  float[] deviceAngles;
  float[] devicePositions;
  float[] forceArray1 = new float[2];
  float[] forceArray2 = new float[2];
  float[] torquesArray1; 
  float[] torquesArray2;
  
  rendering_force = true;
  
  if(haplyBoard1.data_available()){
    
    widgetOne.device_read_data();
    
    deviceAngles = widgetOne.get_device_angles();
    devicePositions = widgetOne.get_device_position(deviceAngles);
    
    anglesA.set(deviceAngles[0], deviceAngles[1]);
    pos_eeA.set(devicePositions[0], devicePositions[1]);
    pos_eeA.set(pos_eeA.copy().mult(100));
    pos_ee.set(pos_eeA);
    
}
  
  f_eeA.set(f_ee);
  f_eeA.div(1000);
  torquesArray1 = widgetOne.set_device_torques(f_ee.array());
  torquesA.set(torquesArray1[0], torquesArray1[1]);
  widgetOne.device_write_torques();

  

}



///////////////////////////
///////////////////////////////////experimental system/
//void serialEvent (Serial myport) {
//   if (myport == portEx){
//             // get the ASCII string:
//            String inString = myport.readStringUntil('\n');
          
//            if (inString != null) {
//              // trim off any whitespace:
//              inString = trim(inString);
//              // convert to an int and map to the screen height:
//              inByte = float(inString);
//              //println(inString.charAt(0));
              
//              if (flag==true){
//               int m=millis();
//                      if (COND==1){
//                      TimeStamp.append(str(m));
//                      SenData.append(inString);
//                      if ((float(inString))>=180){
//                      twangle=float(inString)-360;
//                      }
//                        else{
//                      twangle=float(inString);
//                        }

//                      println(twangle);
//                }else if(COND==2){
//                  XData.append(inString);
//                }else if(COND==3){
//                  YData.append(inString);
//                }
//                switch (inString.charAt(0)){
//                  case 'a':
//                  COND=1;
//                  break;
//                  case 'x':
//                  COND=2;
//                  break;
//                  case 'y':
//                  COND=3;
//                  break;
//                  default:
//                  COND=0;
//                  break;
//                }
//              }
//            } 
//   }
//}
import org.quark.jasmine.*;
import java.util.regex.Pattern;
import controlP5.*;
import grafica.*;
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


ControlP5  cp5;
DropdownList d1,d2,d3;
Slider     S1,S2,S3;
//float      Delta=1.0;    


FloatList  xPoints;
FloatList  yPoints;
int        sliderValue = 100;
int        sliderTicks1 = 100;
int        sliderTicks2 = 30;

boolean    flag=false;
boolean    run=false;
int        lastStepTime=          0; 
PVector    Velocity =             new PVector(0,0); 

// Graph details
static final float RADIUS=15;      // Size of animated discs in pixels.
int graphSize;  // Width and height of graph in pixels.
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

// Text box fields//

int state = 0; //initialize these

String x_upper_bd = "2.0";
String x_lower_bd = "-2.0";
String custom_fn = "";

String result = custom_fn; 

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
float[]    X=new float[NumberPoints];       
float[]    Y=new float[NumberPoints];


void setup(){
  size(1000,600,P2D);
  origin.set(xoffset+button_width ,yoffset-button_height);
  textFont(loadFont("AdobeHeitiStd-Regular-24.vlw"));
  textAlign(RIGHT,TOP);
  cp5=new ControlP5(this);
  xPoints=new FloatList();
  yPoints=new FloatList();
  lastStepTime=millis();
  
  haply_board = new Board(this,"COM4", 0); //Put your COM# port here

  /* DEVICE */
  haply_2DoF = new Device(degreesOfFreedom.HaplyTwoDOF, deviceID, haply_board);
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();

  d1=cp5.addDropdownList("Graph lists") //types of graphs that can be drawn
       //.setPosition(100,100);
       .setPosition(xoffset, yoffset)
       .setFont(loadFont("AdobeHeitiStd-Regular-22.vlw"))
       ;
       customize(d1);
       d1.setValue(3);// customize the first list
       //ControlFont cf1 = new ControlFont(createFont("Arial",20));
   
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

   //  cp5.getController("Graph lists").getCaptionLabel().align(ControlP5.RIGHT, ControlP5.BOTTOM).setPaddingX(0);

     
     
    // create a new button with name 'buttonA'
  cp5.addButton("RUN")
     .setValue(0)
     .setPosition(run_x, run_y)
     .setSize(button_width,button_height)
     .setColorBackground(color(112, 146, 181))
     .setFont(loadFont("AdobeHeitiStd-Regular-24.vlw"))
     ;
  
  // and add another 2 buttons
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
}


void customize(DropdownList d1) {
  // a convenience function to customize a DropdownList
  d1.setBackgroundColor(color(153, 153, 102));
  d1.setItemHeight(button_height+15);
  d1.setBarHeight(button_height-5+15);
  d1.setWidth(button_width);
  d1.setOpen(false);
  //d1.setLabel("Hi",10);
  //d1.setLabel();
  //d1.CaptionLabel().style().marginTop = 3;
  //ddl.captionLabel().style().marginLeft = 3;
  //d1.valueLabel().style().marginTop = 3;
    d1.addItem("Absolute ", 0);
    d1.addItem("Quadratic",1);
    d1.addItem("Sin",2);
    d1.addItem("Custom",3);
  //ddl.scroll(0);
  d1.setColorBackground(color(255, 181, 181));
  d1.setColorActive(color(179, 114, 119));
   d1.setHeight((button_height+15)*2);
   d1.setScrollSensitivity(500.0f); //lower probably means less sensitive, but I can't be sure
}

//void keyPressed() {
//if (key==ENTER||key==RETURN) { //enter presses the run button
//    RUN();
//  } 
//  if (key== BACKSPACE && result != null && result.length() > 0) { //backspace deletes the last letter typed
//    result = result.substring(0, result.length() - 1);
//    if (result.equals("")) {
//      state = 0;
//    }
//  }
  
//}

//void keyTyped() { //this is called when a key is typed (ignores shift and stuff)
//     result = result + key;
//}

void controlEvent(ControlEvent theEvent) {
  if (theEvent.isGroup()) {
    // check if the Event was triggered from a ControlGroup
    println("event from group : "+theEvent.getGroup().getValue()+" from "+theEvent.getGroup());
    
  } 
  else if (theEvent.isController()) {
    println("event from controller : "+theEvent.getController().getValue()+" from "+theEvent.getController());
    println("x_lower_bd: ", x_lower_bd);
    println("x_upper_bd: ", x_upper_bd);
    X=new float[NumberPoints];    
    Xvalues();
    }
}

void draw() {
  graphSize = 3*height/4;
  lineChart.setDim(graphSize*1.3, graphSize);
  
  Xintital = Float.parseFloat(x_lower_bd);
  Xfinal = Float.parseFloat(x_upper_bd);
  result = custom_fn;
  
  //println("X_i = ", Xintital, "X_f = ", Xfinal);
  println(result);
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
  lineChart.endDraw();

  if (run){
      if (millis() - lastStepTime > Delaytime) {
          if (step<NumberPoints){
          // Add the point at the end of the array
              lineChart.addPoint(0,calculatePoint(X[step]));
              if(step!=NumberPoints-1&step!=0){
                float DY=tangent(Yvalues(X[step-1]),Yvalues(X[step]),Yvalues(X[step+1]),xSpace);
                float DX=xSpace;
                updateVelocity(DX,DY);
                println(Velocity.x,Velocity.y);
                step++;
          // Remove the first point
          //lineChart.removePoint(0);
              }else{
                Velocity.set(0,0);
                step++;
              }
         // Remove the last point
         // lineChart.removePoint(lineChart.getPointsRef().getNPoints() - 1);
        lastStepTime = millis();
        }
      }
  }
  switch (state) {
  case 0:
    fill(0); 
    text ("Custom function f(x): \n", cf_text_x, cf_text_y); 
    //noFill();
    //rect(textbox_x, textbox_y, textbox_width, textbox_height);
    break;
 
  case 1:
    fill(255, 2, 2); 
    text ("Thanks \n", xoffset+200, button_height+margin+50); 
    //println(result);
    
    //run = true;
    //flag = true;
     //RUN();
    
    break;
}
}


GPoint calculatePoint(float i) {
  float n=0.0;
  n=Yvalues(i);
  return new GPoint(i, n);
}

public void Graphing(float[] X,float[] Y)
{
  lineChart = new GPlot(this);
  println(origin.x);
  lineChart.setPos(origin.x, origin.y);
  lineChart.setDim(graphSize*1.3, graphSize);
  // or all in one go
  // plot = new GPlot(this, 25, 25, 300, 300);

  // Set the plot limits (this will fix them)
  //lineChart.setXLim(-1.2*scale, 1.2*scale);
  //lineChart.setYLim(-1.2*scale, 1.2*scale);
  lineChart.activateZooming(1.3, CENTER, CENTER);
  // Set the plot title and the axis labels
  lineChart.setTitleText("Clockwise movement");
  lineChart.getXAxis().setAxisLabelText("x axis");
  lineChart.getYAxis().setAxisLabelText("y axis");

  // Activate the panning effect
  lineChart.activatePanning();

  // Add the two set of points to the plot
  GPointsArray Xpoints=new GPointsArray(NumberPoints);
  //Xpoints.add(X);
  //lineChart.setPoints(X);
  //lineChart.addLayer("surface", Y);

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
       break;
       case 1:
            temPointy=(temPointx*temPointx);
       break;
       case 2:
            temPointy=(sin(3.4*temPointx));
       break;
       case 3:
            temPointy =Yvalues(new Function(temPointx));
       break;
       default:
            temPointy=(sin(2*3.4*temPointx));
       break;
   }
   
   return temPointy;
}
//public void RUN(){
//  if (flag){
//    delay(100);
//    Graphing(X,Y);
//    step=0;
//    run=true;
//   }
//}

//public void STOP(){
//  Graphing(X,Y);
//  run=false;
//  Velocity.set(0,0);
//}

public float tangent(float y_b,float y,float y_a,float h){ 
  float Ygradient=0; 
  Ygradient=(((y_a-y)/h)+((y-y_b)/h))/2;
  println("gradient",Ygradient);
  return Ygradient;
}

float Yvalues(Function f) {
  if (!result.equals("")) {
   return f.computeY(result);
  }
  else {
    return sin(3*f.x);
  }
}


public void RUN(){
    println("RUN called");

  if (!Function.valid(result) && (int(d1.getValue()) == 3)) {
    //do nothing if the typed field is empty and custom is selected
    println("don't do anything");
  }
  else {
 // println("RUN called");
  if (flag){
    println("flag is true");
    delay(100);
    Graphing(X,Y);
    step=0;
    run=true;
   }
  }
}

public void STOP(){
  Graphing(X,Y);
  run=false;
  Velocity.set(0,0);
  //result = "";
  state = 0;
}

//public float tangent(float y_b,float y,float y_a,float h){ 
//  float Ygradiant=0; 
//  Ygradiant=((y_a-y/h)+(y-y_b)/h)/2;
//  return Ygradiant;
//}



void onTickEvent(CountdownTimer t, long timeLeftUntilFinish){
  

   
  if (haply_board.data_available()) {
    /* GET END-EFFECTOR STATE (TASK SPACE) */
        
    angles.set(haply_2DoF.get_device_angles()); 
    pos_ee.set( haply_2DoF.get_device_position(angles.array()));
    pos_ee.set(pos_ee.copy().mult(100)); 
    
  }


 
  f_ee.set(Velocity.x,Velocity.y );
 //println(f_ee);
  //f_ee.div(1000); //
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
void onFinishEvent(CountdownTimer t){
  println("Resetting timer...");
  haptic_timer.reset();
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();
}

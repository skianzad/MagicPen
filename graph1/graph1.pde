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
int        NumberPoints=200; //Number of points
float      xSpace=0.02;          //linespace between each point
float      Xintital=-2.0;
//float      Delta=1.0;                        
float[]    X=new float[NumberPoints];       
float[]    Y=new float[NumberPoints];

FloatList  xPoints;
FloatList  yPoints;
int        sliderValue = 100;
int        sliderTicks1 = 100;
int        sliderTicks2 = 30;
int        Delaytime=5;
boolean    flag=false;
boolean    run=false;
int        lastStepTime=          0; 
PVector    Velocity =             new PVector(0,0); 
float      MaxSpeed=              3;
// Graph details
static final float RADIUS=15;      // Size of animated discs in pixels.
static final int graphSize = 400;  // Width and height of graph in pixels.
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

void setup(){
  size(1000,600,P2D);
  origin.set(width/3,height/8);
  textFont(loadFont("Crimson-Italic-24.vlw"));
  textAlign(RIGHT,TOP);
  cp5=new ControlP5(this);
  xPoints=new FloatList();
  yPoints=new FloatList();
  lastStepTime=millis();
  
  haply_board = new Board(this,"COM3", 0); //Put your COM# port here

  /* DEVICE */
  haply_2DoF = new Device(degreesOfFreedom.HaplyTwoDOF, deviceID, haply_board);
  haptic_timer = CountdownTimerService.getNewCountdownTimer(this).configure(SIMULATION_PERIOD, HOUR_IN_MILLIS).start();

  d1=cp5.addDropdownList("Graph lists")
       .setPosition(100,100);
       customize(d1); // customize the first list
       //ControlFont cf1 = new ControlFont(createFont("Arial",20));
   
  S1=cp5.addSlider("sliderValue")
     .setPosition(100,200)
     .setRange(0,255)
     .setSize(200,20)
     .setValue(128)
     //.setNumberOfTickMarks(7)
     .setSliderMode(Slider.FLEXIBLE)
     ;
     
     
    // create a new button with name 'buttonA'
  cp5.addButton("RUN")
     .setValue(0)
     .setPosition(100,300)
     .setSize(200,19)
     .setColorBackground(color(20,200,0))
     ;
  
  // and add another 2 buttons
  cp5.addButton("STOP")
     .setValue(100)
     .setPosition(100,320)
     .setSize(200,19)
     .setColorBackground(color(200,12,0))
     ;
  Xvalues();
  Yvalues(X);
  Graphing(X,Y);
  flag=true;
}
void customize(DropdownList d1) {
  // a convenience function to customize a DropdownList
  d1.setBackgroundColor(color(190));
  d1.setItemHeight(60);
  d1.setBarHeight(30);
  d1.setWidth(200);
  d1.setOpen(false);
  //d1.setLabel("Hi",10);
  //d1.setLabel();
  //d1.CaptionLabel().style().marginTop = 3;
  //ddl.captionLabel().style().marginLeft = 3;
  //d1.valueLabel().style().marginTop = 3;
    d1.addItem("Absolute ", 0);
    d1.addItem("Quadratic",1);
    d1.addItem("Sin",2);
  //ddl.scroll(0);
  d1.setColorBackground(color(204,102,40));
  d1.setColorActive(color(80, 220,100));
}

void keyPressed() {

}

void controlEvent(ControlEvent theEvent) {
  if (theEvent.isGroup()) {
    // check if the Event was triggered from a ControlGroup
    println("event from group : "+theEvent.getGroup().getValue()+" from "+theEvent.getGroup());
    
  } 
  else if (theEvent.isController()) {
    println("event from controller : "+theEvent.getController().getValue()+" from "+theEvent.getController());
}
}

void draw() {
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
       default:
            temPointy=(sin(2*3.4*temPointx));
       break;
   }
   
   return temPointy;
}
public void RUN(){
  if (flag){
    delay(100);
    Graphing(X,Y);
    step=0;
    run=true;
   }
}

public void STOP(){
  Graphing(X,Y);
  run=false;
  Velocity.set(0,0);
}

public float tangent(float y_b,float y,float y_a,float h){ 
  float Ygradient=0; 
  Ygradient=(((y_a-y)/h)+((y-y_b)/h))/2;
  println("gradient",Ygradient);
  return Ygradient;
}





void onTickEvent(CountdownTimer t, long timeLeftUntilFinish){
  

   
  if (haply_board.data_available()) {
    /* GET END-EFFECTOR STATE (TASK SPACE) */
        
    angles.set(haply_2DoF.get_device_angles()); 
    pos_ee.set( haply_2DoF.get_device_position(angles.array()));
    pos_ee.set(pos_ee.copy().mult(100)); 
    
  }


 
  f_ee.set(Velocity.x,Velocity.y );
 println(f_ee);
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
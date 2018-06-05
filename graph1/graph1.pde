import org.quark.jasmine.*;

import controlP5.*;
import grafica.*;
import java.util.regex.Pattern;



ControlP5  cp5;
DropdownList d1,d2,d3;
Slider     S1,S2,S3;
int        NumberPoints=400; //Number of points
float      Xintital=-2.0;
float      Delta=1.0;                        //linespace between each point
float[]    X=new float[NumberPoints];       
float[]    Y=new float[NumberPoints];
float      xSpace=0.01;
FloatList  xPoints;
FloatList  yPoints;
int        sliderValue = 100;
int        sliderTicks1 = 100;
int        sliderTicks2 = 30;
int        Delaytime=10;
boolean    flag=false;
boolean    run=false;
float      scale=          5;
int lastStepTime=          0;    
// Graph details
static final float RADIUS=15;      // Size of animated discs in pixels.
static final int graphSize = 400;  // Width and height of graph in pixels.
GPlot      lineChart;
PVector    origin = new PVector(0,0);
Slider     Speed;
int        step=0;
int        stepsPerCycle=100;

// Text box fields//

int state = 0; 
String result=""; 


void setup(){
  size(1000,600,P2D);
  origin.set(width/3,height/8);
  textFont(loadFont("Crimson-Italic-24.vlw"));
 // textSize(30);
  textAlign(RIGHT,TOP);
  cp5=new ControlP5(this);
  xPoints=new FloatList();
  yPoints=new FloatList();
  lastStepTime=millis();

  
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
     .setSize(200,50)
     .setColorBackground(color(20,200,0))
     ;
  
  // and add another 2 buttons
  cp5.addButton("STOP")
     .setValue(100)
     .setPosition(100,370)
     .setSize(200,50)
     .setColorBackground(color(200,12,0))
     ;
     
    // cp5.setControlFont(new ControlFont(createFont("Arial", 20), 20));
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
 
  if (key==ENTER||key==RETURN) {
 
    state = 1;
    RUN();
  } 
  if (key== BACKSPACE && result != null && result.length() > 0) {
    result = result.substring(0, result.length() - 1);
    if (result.equals("")) {
      state = 0;
    }
  }
  
}

void keyTyped() {
  result = result + key;
}

void controlEvent(ControlEvent theEvent) {
  if (theEvent.isGroup()) {
    // check if the Event was triggered from a ControlGroup
    //println("event from group : "+theEvent.getGroup().getValue()+" from "+theEvent.getGroup());
    
  } 
  else if (theEvent.isController()) {
    //println("event from controller : "+theEvent.getController().getValue()+" from "+theEvent.getController());
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
   // println("let's run -- draw");
    
      if (millis() - lastStepTime > Delaytime) {
          if (step<NumberPoints){
          // Add the point at the end of the array
              lineChart.addPoint(0,calculatePoint(X[step]));
              if(step>=1){
                
              }
              //println(step,X[step],Y[step]);
              step++;
          // Remove the first point
          //lineChart.removePoint(0);
           }
         // Remove the last point
         // lineChart.removePoint(lineChart.getPointsRef().getNPoints() - 1);
        lastStepTime = millis();
      }
  }
  
  
  
  switch (state) {
  case 0:
    fill(0); 
    text ("Custom function f(x): \n"+result, width/5, height/5+15); 
    break;
 
  case 1:
    fill(255, 2, 2); 
    text ("Thanks \n"+result, width/5, height/5+15); 
    //println(result);
    
    //run = true;
    //flag = true;
     //RUN();
    
    break;
  }
}


GPoint calculatePoint(float i) {
  float n=0.0;
  n=Yvalues(new Function(i));
  return new GPoint(i, n);
}

public void Graphing(float[] X,float[] Y)
{
  lineChart = new GPlot(this);
  //println(origin.x);
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
            temPointy=(sin(2*3.4*temPointx));
       break;
       default:
            temPointy=(sin(2*3.4*temPointx));
       break;
   }
   
   return temPointy;
}

float Yvalues(Function f) {
  if (!result.equals("")) {
   return f.computeY(result);
  }
  else {
    return Yvalues(f.x);
  }
}


public void RUN(){
  println("RUN called");
  if (flag){
    println("flag is true");
    delay(100);
    Graphing(X,Y);
    step=0;
    run=true;
   }
}

public void STOP(){
  Graphing(X,Y);
  run=false;
  
  //result = "";
  state = 0;
}

public float tangent(float y_b,float y,float y_a,float h){ 
  float Ygradiant=0; 
  Ygradiant=((y_a-y/h)+(y-y_b)/h)/2;
  return Ygradiant;
}

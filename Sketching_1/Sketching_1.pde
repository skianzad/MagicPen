import processing.svg.*;
import processing.pdf.*;
import geomerative.*;
PGraphics pgDrawing;
PShape SIM;
PShape[] bg;
PShape tst;
RShape grp;
int NP=1;
float x=width/2;
float y=height/2;
boolean flag= true; 


void setup() {
  size(600, 800);
  background(250);
  //RG.init(this);
  strokeWeight(8);
  pgDrawing = createGraphics(600, 800, SVG, "test1.svg");
  pgDrawing.beginDraw();
  //pgDrawing.beginShape();
  tst=createShape();
  tst.beginShape();
  bg=new PShape[100];
  bg[1]=createShape();
  SIM=createShape(GROUP); 
}


void draw() {
   
   move();
   mouseP();
}
void move(){
  x=mouseX;
  y=mouseY;

}
void mouseReleased() {
  println("done");
      //grp.draw(pgDrawing);
   
       bg[NP]=tst;
      tst.endShape();
      background(250);
      flag=false;

      //
      //bg =loadShape("test1.svg");
     
      for (int i=1;i<=NP;i++)
        {   if (bg[NP]!=null) shape(bg[i],0,0); 
        }
   
      SIM.addChild(bg[NP]);
      pgDrawing.shape(SIM);
      //pgDrawing.endShape();
      pgDrawing.endDraw();
      pgDrawing.dispose();
      pgDrawing.beginDraw();
      pgDrawing.beginShape();
     // shape(SIM);
       //for (int i=0;i<NP;i++)
       // {   shape(SIM.getChild(i),0,0); 
      //}
      NP++;
      PVector v=new PVector (0,0);
      for (int i = 0; i < SIM.getChild(0).getVertexCount(); i++) {
      v = SIM.getChild(0).getVertex(i);
      println(v);
      }
     tst=createShape();
     tst.beginShape();
}
void mouseP(){
  if (mousePressed)
  {
    if (mouseButton==LEFT){
      //beginShape();
      //pgDrawing.vertex(mouseX, mouseY);
      tst.vertex(mouseX,mouseY);
      line(mouseX,mouseY,pmouseX,pmouseY);
      //stroke(126);
      flag=true;
  }else if (mouseButton==RIGHT&&flag)
    { 
      
      
    }

  }
}
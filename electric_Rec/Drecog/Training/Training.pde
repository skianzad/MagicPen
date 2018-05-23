ArrayList <PVector> Pointlists;
StringList xPoints;
StringList yPoints;
PVector Po;
String pointSave;
Table table;
Table train;
char lable='N';




void setup(){
background(255);
size(500,500); 
train=new Table();
Pointlists=new ArrayList();
Po=new PVector();
yPoints= new StringList();
xPoints= new StringList();
table= new Table();
table.addColumn("X/Y");  
table.addColumn("Lable");






}
void draw(){

}

void mouseDragged(){
Pointlists.add(new PVector(mouseX,mouseY));
xPoints.append(str(mouseX));
xPoints.append(str(mouseY));
}
void mouseReleased(){
  for (int i=1;i<Pointlists.size();i++){
    Po=Pointlists.get(i);
  }
String[] ResultX=xPoints.array();
xPoints.clear();

pointSave=join(ResultX,",");
//pointSave=pointSave+";";
 String[] list = split(pointSave, ' ');
 saveStrings("point.txt",list);
 //String[] rpoints=loadStrings("point.txt");
 //String total=join(rpoints);
 //println(rpoints);
 TableRow row = table.addRow();
 row.setString("X/Y", pointSave);
 row.setString("Lable", str(lable));
 saveTable(table,"table.csv"); 
}

void keyPressed() {
lable=key;
  if (key==32){
     train=loadTable("table.csv","header");
     TableRow row = train.getRow(0);
     String ps=(row.getString("X/Y"));
      String[] pts=split(ps,',');
      int[]points=int(pts);
      println(points);
  }
}
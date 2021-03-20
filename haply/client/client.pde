import processing.net.*; 

Client myClient;
String dataStr;
 
void setup() { 
  size(800, 800); 
  background(102);
  
  myClient = new Client(this, "192.168.0.103", 8080); 
  println("Connected");
}

/* extract x coord, y coord and pressure
 * from pen data string
 */
float[] extractPenData(String dataStr) {
  /* extract data */
  String dataStrArr[]= dataStr.split("/");
  String coordsStr = dataStrArr[0];
  String pressureStr = dataStrArr[1];
  float pressure = Float.parseFloat(pressureStr);
  String coordsStrArr[] = coordsStr.split(",");
  float xCoord = Float.parseFloat(coordsStrArr[0]);
  float yCoord = Float.parseFloat(coordsStrArr[1]);
  
  /* assemble returned array */
  float[] dataArr = new float[3];
  dataArr[0] = xCoord;
  dataArr[1] = yCoord;
  dataArr[2] = pressure;
  return dataArr;
}
 
void draw() {
  // transmit request
  myClient.write("data");
  
  // wait for response
  while (myClient.available() == 0); 
  
  // decode response
  dataStr = myClient.readString();
  //println(dataStr);
  float[] dataArr = extractPenData(dataStr);
  
  // draw
  if (dataArr[2] > 10.0) {
    stroke(255);
    point(dataArr[0], dataArr[1]);
  }
} 

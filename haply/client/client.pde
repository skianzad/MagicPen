import processing.net.*; 

Client myClient;
String dataStr;

/* set up the canvas and the WiFi client
 */
void setup() { 
  size(800, 800); 
  background(102);
  
  myClient = new Client(this, "192.168.0.103", 8080); 
  println("Connected");
}


/* extract list of x and y coordinates from the data
 * string and assign to the given xCoords and yCoords
 * arguments accordingly.
 * for a stroke of N points, dataStr should be formatted as 
 * x_0,y_0/x_1,y_1/.../x_(N-1),y_(N-1)/
 */
void decodeStrokeData(String dataStr, ArrayList<Float>xCoords, ArrayList<Float>yCoords) {
  String dataStrArr[]= dataStr.split("/");
  
  for (int i=0; i<dataStrArr.length - 1; i++) {
    //println(dataStrArr[i]);
    String coordsStrArr[] = dataStrArr[i].split(",");
    float x = Float.parseFloat(coordsStrArr[0]);
    float y = Float.parseFloat(coordsStrArr[1]);
    xCoords.add(x);
    yCoords.add(y);
  }
  
  return;
}


/* WiFi client to request and receive stroke data.
 * The client would not initiate a new request before
 * the server has transmitted data for the previous.
 */
void draw() {
  // transmit request
  myClient.write("data");
  
  // wait for response
  while (myClient.available() == 0); 
  println("received response");
  
  // decode response
  String dataStr = myClient.readString();
  //println(dataStr);
  ArrayList<Float> xCoords = new ArrayList<Float>();
  ArrayList<Float> yCoords = new ArrayList<Float>();
  decodeStrokeData(dataStr, xCoords, yCoords);
  
  // draw
  int numPts = xCoords.size();
  for (int i = 1; i < numPts; i++) {
    float lastX = xCoords.get(i-1);
    float lastY = yCoords.get(i-1);
    float currX = xCoords.get(i);
    float currY = yCoords.get(i);
    stroke(255);
    line(lastX, lastY, currX, currY);
  }
} 

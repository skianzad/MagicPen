const byte numChars = 10;
char receivedChars[numChars]; // an array to store the received data
String speed;
boolean newData = false;

void setup() {
 Serial.begin(115200);
}

void loop() {
 recvWithEndMarker();
 showNewData();
}

void recvWithEndMarker() {
 static byte ndx = 0;
 char endMarker = 'z';
 char rc;
 
 // if (Serial.available() > 0) {
           while (Serial.available() > 0 && newData == false) {
 rc = Serial.read();
 Serial.print(rc);

 if (rc != endMarker) {
 receivedChars[ndx] = rc;
 ndx++;
 if (ndx >= numChars) {
 ndx = numChars - 1;
 }
 }
 else {
 receivedChars[ndx] = '\0'; // terminate the string
 ndx = 0;
 newData = true;
 }
 }
}

void showNewData() {
 if (newData == true) {
     if (receivedChars[0]=='a'){
//       Serial.print("This is right motor ... ");
       speed="";
       speed.concat(receivedChars[1]);
       speed.concat(receivedChars[2]);
       speed.concat(receivedChars[3]);
//       Serial.println(speed);
     }else if(receivedChars[0]=='b'){
//       Serial.print("This is left motor ... ");
       speed="";
       speed.concat(receivedChars[1]);
       speed.concat(receivedChars[2]);
       speed.concat(receivedChars[3]);
//       Serial.println(speed);
     }else{
//      Serial.write(receivedChars);
     }
    
  newData = false;
  }
}

#include <string.h>


char *input; //Input
char *del="{}bcd:;";
char *del1='a';
char *token; //Input
char *token1;
void setup() {
  Serial.begin(9600);
    
}

void loop() {
  if (Serial.available()){
      input=Serial.read();
      *token = strtok(input,del);
      *token1 = strtok(input,del1);
      Serial.print(*token);
      Serial.print(*token1);

          }
}
 


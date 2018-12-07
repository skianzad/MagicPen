You should be able to run the car_race.pde program using wifi if you copy and paste the files in this folder to replace their original versions (It works on my laptop).
In addition,  I commented out the only line in Encoder.cpp since it causes compilation issues. Uncomment that line if it is necessary.

For the connection between Arduino DUE and ESP8266, I connected the serial1 port on DUE (Pin 18 and 19 for TX and RX respectively) to the RX and TX pin on ESP8266.
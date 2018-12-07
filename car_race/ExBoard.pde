import processing.core.PApplet;
import processing.serial.*;

public class ExBoard{

  
  private Serial       port;
  private PApplet     applet;  
  
  private byte         deviceID;
  private int         number_of_parameters     = 0;
  private byte[]      actuator_positions       = {0, 0, 0, 0};
  
  
  /**
   * Constructs a Board linking to the specified serial port at the given serial data speed (baud rate)
   * 
   * @param    app the parent Applet this class runs inside (this is your Processing sketch)
   * @param    portname serial port name that the hardware board is connected to (eg, "com10")
   * @param    speed the baud rate of serial data transfer
   */
  public ExBoard(PApplet app, String portName, int baud){
    this.applet = app;
    port = new Serial(applet, portName, baud);
    port.clear();
  }
}
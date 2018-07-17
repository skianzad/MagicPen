/**
 **********************************************************************************************************************
 * @file       Board.java
 * @author    
 * @version    V0.1.0
 * @date       01-March-2017
 * @brief      Board class definition
 **********************************************************************************************************************
 * @attention
 *
 *
 **********************************************************************************************************************
 */

import processing.core.PApplet;
import processing.serial.*;

public class Board{

	
	private Serial 	    port;
	private PApplet     applet;	
	
	private byte 	      deviceID;
	private int 	      number_of_parameters     = 0;
	private byte[]      actuator_positions       = {0, 0, 0, 0};
	
	
  /**
   * Constructs a Board linking to the specified serial port at the given serial data speed (baud rate)
   * 
   * @param    app the parent Applet this class runs inside (this is your Processing sketch)
   * @param    portname serial port name that the hardware board is connected to (eg, "com10")
   * @param    speed the baud rate of serial data transfer
   */
	public Board(PApplet app, String portName, int baud){
		this.applet = app;
		port = new Serial(applet, "COM3", baud);
		port.clear();
	}
	
   
  /**
   * Formats and transmits the float data array over the serial port
   * 
   * @param     type type of communication taking place
   * @param     deviceID ID of device transmitting the information
   * @param     positions the motor positions the data is meant for
   * @param     data main data payload to be transmitted
   */
	public void transmit(byte type, byte deviceID, byte[] positions, float[] data){
		
		
		byte[] outData = new byte[2 + 4*data.length];
		byte[] segments = new byte[4];
		
		outData[0] = format_header(type, positions);
		outData[1] = deviceID;
		this.deviceID = deviceID;
		
		
		int j = 2;
		for(int i = 0; i < data.length; i++){
			segments = FloatToBytes(data[i]);
			System.arraycopy(segments, 0, outData, j, 4);
			j = j + 4;
		}
		
		this.port.write(outData);
	}
	
	
  /**
   * Receives data from the serial port and formats said data to return a float data array
   * 
   * @param     type type of communication taking place
   * @param     deviceID ID of the device receiving the information
   * @param     positions the motor positions the data is meant for
   * @return    formatted float data array from the received data
   */
	public float[] receive(byte type, byte deviceID, byte[] positions){
		
		int size = set_buffer_length(type, positions);
		
		byte[] inData = new byte[1 + 4*size];
		byte[] segments = new byte[4];
		
		float[] data = new float[size];
		
		this.port.readBytes(inData);
		
		if(inData[0] != deviceID){
			System.err.println("Error, another device expects this data!");
		}
		
		int j = 1;
		
		for(int i = 0; i < size; i++){
			System.arraycopy(inData, j, segments, 0, 4);
			data[i] = BytesToFloat(segments);
			j = j + 4;
		}
		
		return data;
	}
	
	
  /**
   * @return   a boolean indicating if data is available from the serial port
   */
	public boolean data_available(){
		
		boolean available = false;
		
		if(port.available() > 0){
			available = true;
		}
		
		return available;
	}

   
  /**
   * Set serial buffer length for receiving incoming data
   *
   * @param   length number of bytes expected in read buffer
   */
	private void set_buffer(int length){
		this.port.buffer(length);
	}
	
	
  /**
   * Determines how much data should incoming and sets buffer lengths accordingly
   *
   * @param    type type of communication taking place
   * @param    positions the motor positions the data is meant for
   * @return   number of active motors
   */
	private int set_buffer_length(byte type, byte[] positions){
		
		int m_active = 0;
		
		for(int i = 0; i < 4; i++){
			if(positions[i] > 0){
				m_active++;
			}
		}
		
		switch(type){
			case 0: // setup command
				port_check(positions);
				set_buffer(5);	
				m_active = 1;
				break;	
			case 1: // read encoder data
				set_buffer(1+4*m_active);
				break;
		}
		
		return m_active;
	}
	
	
  /**
   * Determines if actuator ports are in use and prints warnings accordingly
   *
   * @param    positions the motor positions being set
   */
	private void port_check(byte[] positions){
		
		for( int i = 0; i < 4; i++){
			if(actuator_positions[i] > 0 && positions[i] > 0){
				System.err.println("Warning, hardware actuator " + i + " was in use and will be overridden");
			}
			
			actuator_positions[i] = positions[i];
		}
	}
	
	
  /**
   * Formats header control byte for transmission over serial
   *
   * @param    type type of communication taking place
   * @param    positions the motor positions the data is meant for
   * @return   formatted header control byte
   */ 
	private byte format_header(byte type, byte[] positions){
		
		int header = 0;
    
		for(int i = 0; i < positions.length; i++){
	    
			header = header >> 1;		
  
			if(positions[i] > 0){
				header = header | 0x0008;
			}
		}

		header = header | (type << 4);
		
		return (byte)header;
	}
	
	
  /**
   * Translates a float point number to its raw binary format and stores it across four bytes
   *
   * @param    val floating point number
   * @return   array of 4 bytes containing raw binary of floating point number
   */ 
	private byte[] FloatToBytes(float val){
  
		byte[] segments = new byte[4];
  
		int temp = Float.floatToRawIntBits(val);
  
		segments[3] = (byte)((temp >> 24) & 0xff);
		segments[2] = (byte)((temp >> 16) & 0xff);
		segments[1] = (byte)((temp >> 8) & 0xff);
		segments[0] = (byte)((temp) & 0xff);

		return segments;
  
	}


  /**
   * Translates a binary of a float point to actual float point
   *
   * @param    segment array containing raw binary of floating point
   * @return   translated floating point number
   */ 	
	private float BytesToFloat(byte[] segment){
  
		int temp = 0;
  
		temp = (temp | (segment[3] & 0xff)) << 8;
		temp = (temp | (segment[2] & 0xff)) << 8;
		temp = (temp | (segment[1] & 0xff)) << 8;
		temp = (temp | (segment[0] & 0xff)); 
  
		float val = Float.intBitsToFloat(temp);
  
		return val;
	}	
	
}
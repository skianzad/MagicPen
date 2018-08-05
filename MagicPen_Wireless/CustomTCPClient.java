import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.net.InetSocketAddress;

/* A simple TCP client that sends data to server and reads response from server */

public class CustomTCPClient {
    Socket socket = null;
    /*OutputStreamWriter osw = null;
    InputStreamReader isr = null;*/
    private DataInputStream dis;
    private DataOutputStream dos;
    
    public void InitSocket(String serverAddr, int port) throws UnknownHostException, IOException, ClassNotFoundException, InterruptedException {
    	//establish socket connection to server; creating the socket with a timeout.
		System.out.println("Initializing socket connection to server...");
		socket = new Socket();
		socket.connect(new InetSocketAddress(serverAddr, port), 5000);
    }
    
    /*public void sendData(String data) throws IOException {
		System.out.println("Sending data to the server...");
    	osw = new OutputStreamWriter(socket.getOutputStream());
      BufferedWriter bw = new BufferedWriter(osw);
    	bw.write(data + "\n");
      bw.flush();
    	System.out.println("Data sent");
    }*/
    
    public void sendData(byte[] buffer) throws IOException {
		System.out.println("Sending data to the server...");
    	dos = new DataOutputStream(socket.getOutputStream());
    	dos.write(buffer);
    	System.out.println("Data sent");
    }
    
    /*public String readResponse() throws IOException, ClassNotFoundException {
    	isr = new InputStreamReader(socket.getInputStream());
      BufferedReader br = new BufferedReader(isr);
    	//while(ois.available() == 0); // This does not work well
    	String response = (String) br.readLine();
    	return response;
    }*/
    
    public void readResponse(byte[] buffer) throws IOException, ClassNotFoundException {
    	dis = new DataInputStream(socket.getInputStream());
    	dis.read(buffer);
    }
	
	public boolean available() throws IOException, ClassNotFoundException{
		dis = new DataInputStream(socket.getInputStream());
		if(dis.available() > 0) {
			return true;
		} else {
			return false;
		}
	}
    
    public void closeIOStream() throws IOException {
    	dis.close();
    	dos.close();
    }

    public void closeSocket() throws IOException {
    	socket.close();
    }
    
  // Example code
	/*public static void main(String[] args) throws Exception {
		// get the localhost IP address, if server is running on some other IP, you need to use that
		String host = "192.168.43.195";
	  int port = 8080;
	    
		CustomTCPClient client = new CustomTCPClient();
		client.InitSocket(host, port);
		client.sendData("hello");
		
		// read resposne from server. I am not sure if there needs to be some delay but this works fine for me
		String resp = client.readResponse();
		System.out.println( resp);
		
		// Close IOstreams and socket after done using them
		client.closeIOStream();
		client.closeSocket();
	}*/
}
	

package chatApp;

import java.awt.*;
import java.io.*;
import java.net.*;
import javax.swing.*;

public class client extends JFrame{
	
	private JFrame frame;
	private JTextField textField;
	private JTextArea chatWindow;
	private ServerSocket server;
	private Socket connection;
	private ObjectOutputStream output;
	private ObjectInputStream input;
	
	public client(){
		super("Client");
		frame = new JFrame();
		//frame.setLayout(new FlowLayout());
		frame.setSize(300,300);
		frame.setVisible(true);
		//frame.setLayout(new FlowLayout());
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
        String text = null;
		chatWindow = new JTextArea(text,15,10);
		chatWindow.setPreferredSize(new Dimension(200, 200));
		chatWindow.setEditable(false);
		frame.add(new JScrollPane(chatWindow),BorderLayout.NORTH);
		
		textField = new JTextField();
		textField.setText("client");
		textField.setEditable(false);
		frame.add(textField,BorderLayout.SOUTH);
		
		
		//frame.add(pane);
	}
	
	public void runAllService(){
		while(true){
			try {
				server = new ServerSocket(4444,111);
				startConnection(server);
				setUpStreams();
				manageMessages();
				
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	private void startConnection(ServerSocket server){
		showMessage("Waiting to connection to a client...");
		connection = server.accept();
		showMessage("Connected to " + connection.getInetAddress().getHostName());
	}
	
	private void setUpStreams() throws IOException{
		output = new ObjectOutputStream(connection.getOutputStream());
		output.flush();
		input = new ObjectInputStream(connection.getInputStream());
		showMessage("Streams are ready to go.");
	}

	private void manageMessages(){
		String message = "You are now connected to me";
		sendMessage(message);
		do{
			message = input.readObject().toString();
			showMessage(message);
		}while(!message.equals(""));
	}
	
	private void closeConnection() throws IOException{
		showMessage("Closing conncetion");
		output.close();
		input.close();
		connection.close();
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		client c1 = new client();
		
		runAllService();

	}
}

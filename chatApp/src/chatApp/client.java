package chatApp;

import java.awt.*;
import javax.swing.*;

public class client extends JFrame{
	
	private JFrame frame;
	private JTextField textField;
	private JTextArea chatWindow;
	private JPanel pane;
	
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

	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		client c1 = new client();

	}
}

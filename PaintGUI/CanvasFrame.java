import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class CanvasFrame extends JFrame{
	private final PaintPanel _PaintPanel;
	
	/* Constructor derives from superclass JFrame, sets a title, creates a new 600x600 Paint Panel object
	 * and centers it, as well as creating various buttons. The buttons use the protocol explained on the
	 * class page example, overriding the parent action listener method by creating a new event responder
	 * that performs the specified task of the button. This is method three in the example.
	 */
	
	
	
	/*
	 * Citation:
	 * 	The button action listeners were exemplified in the MainFrame example on the CIS 212 page. They override
	 * 	the super ActionListener method to modify global variables in the PaintPanel class. This technique is also
	 * 	explained in the (10-19.java) GUI example as an efficient method for handling button actions.
	 */
	public CanvasFrame(){
		super("Java Paint Frame: Christopher Johnson");
		setLayout(new BorderLayout());
		
		_PaintPanel = new PaintPanel();
		_PaintPanel.setPreferredSize(new Dimension(600,600));
		add(_PaintPanel, BorderLayout.CENTER);
		
		// Black Button
		JButton blackButton = new JButton("Black");
		blackButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.setCanvasColor(Point.blackColor);
			}
		});
		
		// Green Button
		JButton greenButton = new JButton("Green");
		greenButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.setCanvasColor(Point.greenColor);
			}
		});
		
		// Yellow Button
		JButton yellowButton = new JButton("Yellow");
		yellowButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.setCanvasColor(Point.yellowColor);
			}
		});
		
		// Gray Button
		JButton grayButton = new JButton("Gray");
		grayButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.setCanvasColor(Point.grayColor);
			}
		});
		
		/* Packing the color buttons into a JPanel object, orienting them vertically, and placing them
		*  on the left side of the Paint Panel object
		*/
		JPanel colorPanel = new JPanel(new GridLayout(4,1));
		colorPanel.add(blackButton);
		colorPanel.add(greenButton);
		colorPanel.add(yellowButton);
		colorPanel.add(grayButton);
		add(colorPanel, BorderLayout.WEST);
		
		// Small Size Button
		JButton smallButton = new JButton("Small");
		smallButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.setCanvasSize(Point.smallSize);
			}
		});
		
		// Medium Size Button
		JButton mediumButton = new JButton("Medium");
		mediumButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.setCanvasSize(Point.mediumSize);
			}
		});
		
		// Large Size Button
		JButton largeButton = new JButton("Large");
		largeButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.setCanvasSize(Point.largeSize);
			}
		});
		
		// Clear Button
		JButton clearButton = new JButton("Clear");
		clearButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event){
				_PaintPanel.clear();
			}
		});
		
		/* Packing the size buttons into a JPanel object, orienting them vertically, and placing them
		*  on the right side of the Paint Panel object
		*  
		*  Citation:
		*  	The GridLayout and Dimension methods are exemplified in the Paint and Shape Painting examples
		*  	on the CIS 212 WebPage (10-21c.java and 10-24c.java). They are an efficient way of establishing
		*   GUI geometry. The East/West layout is based off of the sample picture for the project.
		*/
		JPanel sizePanel = new JPanel(new GridLayout(4,1));
		sizePanel.add(smallButton);
		sizePanel.add(mediumButton);
		sizePanel.add(largeButton);
		sizePanel.add(clearButton);
		add(sizePanel, BorderLayout.EAST);
	}
}

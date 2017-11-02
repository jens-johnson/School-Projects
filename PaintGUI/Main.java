import javax.swing.JFrame;


/*
 * NOTE:
 * 
 * All of the citations I make are based off of the CIS 212 example page, which can be found at:
 *      
 *      https://classes.cs.uoregon.edu/17S/cis212/examples.htm
 */

// Main class simply creates a new canvas object to be called when executed in the console
public class Main {
	public static void main(String[] args){
		CanvasFrame frame = new CanvasFrame();
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.pack();
		frame.setVisible(true);
	}
}

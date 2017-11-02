import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ArrayList;
import javax.swing.JPanel;

public class PaintPanel extends JPanel {
	
	// Instance variables for the list of points of the panel, the current color, and the size of the drawing
	private ArrayList<Point> _points;
	private Color _canvasColor;
	private int _canvasSize;
	
	// Constructs a new Paint Panel, with default black, small paint size
	public PaintPanel(){
		_points = new ArrayList<Point>();
		_canvasColor = Point.blackColor;
		_canvasSize = Point.smallSize;
		
		/* Mouse adapter listens for the mouse being dragged, adds a point to the points array and draws
		*  it on the canvas
		*/
		
		/*
		 * Citation:
		 * 	Mouse adapter listeners inspired by the PaintPanel example on the CIS 212 examples page (10-21b.java)
		 *  This override for listener method strategy was also inspired by the other GUI example (10-19a.java) as
		 *  an efficient strategy for adapting user response.
		 */
		MouseAdapter adapter = new MouseAdapter(){
			@Override
			public void mouseDragged(MouseEvent event){
				_points.add(new Point(event.getX(),event.getY(),_canvasColor,_canvasSize));
				repaint();
			}
		};
		
		addMouseListener(adapter);
		addMouseMotionListener(adapter);	
	}
	
	/* Override method of the super paintComponent method called by JPanel repaint(), paints each point in
	*  the array its respective color using the draw() method from the point class.
	*  
	*  Citation:
	*  	The paintComponent override was exemplified in the PaintPanel (10-21b.java) on the CIS 212 WebPage. 
	*  	The repaint(); method takes advantage of this override to perform the modified task. 
	*/
	@Override
	public void paintComponent(Graphics canvas){
		super.paintComponent(canvas);
		for (Point point: _points){
			canvas.setColor(point.getColor());
			point.draw(canvas);
		}
	}
	
	
	// Setter methods called by the CanvasFrame GUI buttons to determine the active color/draw size
	public void setCanvasColor(Color color){
		_canvasColor = color;
	}
	public void setCanvasSize(int size){
		_canvasSize = size;
	}
	
	/* Clear method simply clears the point array, and repaints the canvas, i.e. clears all of the drawings off
	*  of it
	*/
	public void clear(){
		_points.clear();
		repaint();
	}
	
}

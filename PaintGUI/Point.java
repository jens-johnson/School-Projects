import java.awt.Color;
import java.awt.Graphics;

public class Point {
	
	// Hex Color Codes for the different paint colors
	public static final Color blackColor = Color.decode("#000000");
	public static final Color greenColor = Color.decode("#00802b");
	public static final Color yellowColor = Color.decode("#ffff00");
	public static final Color grayColor = Color.decode("#d9d9d9");
	
	// Integer values for the pixel height and width of the paint points
	public static final int smallSize = 10;
	public static final int mediumSize = 20;
	public static final int largeSize = 50;
	
	private final int _x;
	private final int _y;
	private final Color _color;
	private final int _size;
	
	// Constructs a point
	public Point(int x, int y, Color color, int size){
		this._x = x;
		this._y = y;
		this._color = color;
		this._size = size;
	}
	
	// Getters for the point's respective location, color, and size
	public int getX(){
		return this._x;
	}
	
	public int getY(){
		return this._y;
	}
	
	public Color getColor(){
		return this._color;
	}
	
	public int getSize(){
		return this._size;
	}
	
	
	
	// Takes a graphics object and draws the point on it using its position and size attributes
	
	// Note, I chose an oval as the point object, because it comes across clearer than a rectangle on a canvas
	public void draw(Graphics drawPoint){
		drawPoint.fillOval(_x, _y, _size, _size);
	}
}

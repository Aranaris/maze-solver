from tkinter import Tk, BOTH, Canvas

class Window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.__root = Tk()
		self.__root.title = 'test'
		self.canvas = Canvas(self.__root)
		self.canvas.pack()
		self.running = False
		self.__root.protocol("WM_DELETE_WINDOW", self.close)

	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update()
	
	def wait_for_close(self):
		self.running = True
		while self.running:
			self.redraw()

	def close(self):
		self.running = False

	def draw_line(self, line, fill_color):
		line.draw(self.canvas, fill_color)

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __repr__(self) -> str:
		return f"({self.x}, {self.y})"

class Line:
	def __init__(self, start, end):
		self.start = start
		self.end = end

	def draw(self, canvas, fill_color):
		canvas.create_line(
			self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2
		)
		canvas.pack()

def main():
	win = Window(800, 600)
	point1 = Point(0, 0)
	point2 = Point(100, 100)
	line = Line(point1, point2)
	win.draw_line(line, 'red')
	win.wait_for_close()

	
if __name__ == '__main__':
	main()

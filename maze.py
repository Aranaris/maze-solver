from tkinter import Tk, BOTH, Canvas

class Window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.__root = Tk()
		self.__root.title = 'test'
		self.canvas = Canvas(self.__root, {'bg':'white'})
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

class Cell:
	def __init__(self, top_left, bottom_right, win):
		self.has_left_wall = True
		self.has_right_wall = True
		self.has_top_wall = True
		self.has_bottom_wall = True
		self._top_left = top_left
		self._top_right = Point(bottom_right.x, top_left.y)
		self._bottom_left = Point(top_left.x, bottom_right.y)
		self._bottom_right = bottom_right
		self._win = win
		self.center = Point((top_left.x + bottom_right.x) // 2, (top_left.y + bottom_right.y) // 2)

	def draw(self):
		walls = []
		if self.has_left_wall:
			walls.append(Line(self._top_left, self._bottom_left))
		if self.has_right_wall:
			walls.append(Line(self._top_right, self._bottom_right))
		if self.has_top_wall:
			walls.append(Line(self._top_left, self._top_right))
		if self.has_bottom_wall:
			walls.append(Line(self._bottom_left, self._bottom_right))
		for wall in walls:
			self._win.draw_line(wall, 'black')

	def draw_move(self, to_cell, undo=False):
		color = ''
		if not undo:
			color = 'red'
		else:
			color = 'gray'

		cell_path = Line(self.center, to_cell.center)
		self._win.draw_line(cell_path, color)

def main():
	win = Window(400, 400)
	point1 = Point(0, 0)
	point2 = Point(100, 100)
	point3 = Point(100, 0)
	point4 = Point(200, 100)
	cell1 = Cell(point1, point2, win)
	cell2 = Cell(point3, point4, win)
	
	cell1.draw()
	cell2.draw()

	cell1.draw_move(cell2)

	win.wait_for_close()

	
if __name__ == '__main__':
	main()

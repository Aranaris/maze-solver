from tkinter import Tk, BOTH, Canvas
import time

class Window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.__root = Tk()
		self.__root.title = 'test'
		self.canvas = Canvas(self.__root, {'bg':'white', 'width':self.width, 'height':self.height})
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
	def __init__(self, win=None):
		self.has_left_wall = True
		self.has_right_wall = True
		self.has_top_wall = True
		self.has_bottom_wall = True
		self._x1 = None
		self._y1 = None
		self._x2 = None
		self._y2 = None
		self.center = None
		self._win = win
	
	def set_coords(self, top_left, bottom_right):
		self._x1 = top_left.x
		self._y1 = top_left.y
		self._x2 = bottom_right.x
		self._y2 = bottom_right.y
		self.center = Point((top_left.x + bottom_right.x) // 2, (top_left.y + bottom_right.y) // 2)

	def draw(self):
		self._top_left = Point(self._x1, self._y1)
		self._top_right = Point(self._x2, self._y1)
		self._bottom_left = Point(self._x1, self._y2)
		self._bottom_right = Point(self._x2, self._y2)
			
		walls = []
		fill_color = ''
		if self.has_left_wall:
			fill_color = 'black'
		else:
			fill_color = 'white'
		walls.append({
			'line': Line(self._top_left, self._bottom_left),
			'fill': fill_color,
			'side': 'left'
			})
		if self.has_right_wall:
			fill_color = 'black'
		else:
			fill_color = 'white'
		walls.append({
			'line': Line(self._top_right, self._bottom_right),
			'fill': fill_color,
			'side': 'right'
			})
		if self.has_top_wall:
			fill_color = 'black'
		else:
			fill_color = 'white'
		walls.append({
			'line': Line(self._top_left, self._top_right),
			'fill': fill_color,
			'side': 'top'
			})
		if self.has_bottom_wall:
			fill_color = 'black'
		else:
			fill_color = 'white'
		walls.append({
			'line': Line(self._bottom_left, self._bottom_right),
			'fill': fill_color,
			'side': 'bottom'
			})
			
		for wall in walls:
			self._win.draw_line(wall['line'], wall['fill'])

	def draw_move(self, to_cell, undo=False):
		color = ''
		if not undo:
			color = 'red'
		else:
			color = 'gray'

		cell_path = Line(self.center, to_cell.center)
		self._win.draw_line(cell_path, color)

class Maze:
	def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
		self._x1 = x1
		self._y1 = y1
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y
		self._win = win
		self._cells = []
		
		self._create_cells()
		self._break_entrance_and_exit()
	
	def _create_cells(self):
		for i in range(self.num_cols):
			col = []
			for j in range(self.num_rows):
				new_cell = Cell(self._win)
				if self._win is not None:
					self._draw_cell(new_cell, i, j)
					self._animate()
				col.append(new_cell)
			self._cells.append(col)

		
	def _draw_cell(self, cell, i, j):
		x1 = self._x1 + i * self.cell_size_x
		x2 = self._x1 + (i+1) * self.cell_size_x
		y1 = self._y1 + j * self.cell_size_y
		y2 = self._y1 + (j+1) * self.cell_size_y
		top_left = Point(x1, y1)
		bottom_right = Point(x2, y2)
		cell.set_coords(top_left, bottom_right)
		cell.draw()

	def _animate(self):
		self._win.redraw()
		time.sleep(.05)
		
	def _break_entrance_and_exit(self):
		if len(self._cells) > 0:
			self._cells[0][0].has_top_wall = False
			self._cells[0][0].draw()
			self._cells[-1][-1].has_bottom_wall = False
			self._cells[-1][-1].draw()

def main():
	win = Window(800, 600)
	Maze(10, 10, 10, 12, 50, 50, win)
	win.wait_for_close()

	
if __name__ == '__main__':
	main()

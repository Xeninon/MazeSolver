from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Title"
        self.__canvas = Canvas(master=self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH)
        self.__isrunning = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__isrunning = True
        while self.__isrunning:
            self.redraw()
    
    def close(self):
        self.__isrunning = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, P1, P2):
        self.P1 = P1
        self.P2 = P2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.P1.x, self.P1.y, self.P2.x, self.P2.y, fill=fill_color, width=2)

class Cell():
    def __init__(self, P1, P2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = P1.x
        self._x2 = P2.x
        self._y1 = P1.y
        self._y2 = P2.y
        self._win = win
        self.visited = False
    
    def draw(self, fill_color):
        left_x = min(self._x1, self._x2)
        right_x = max(self._x1, self._x2)
        top_y = min(self._y1, self._y2)
        bottom_y = max(self._y1, self._y2)
        top_line = Line(Point(left_x, top_y),Point(right_x, top_y))
        bottom_line = Line(Point(left_x, bottom_y),Point(right_x, bottom_y))
        left_line = Line(Point(left_x, top_y),Point(left_x, bottom_y))
        right_line = Line(Point(right_x, top_y),Point(right_x, bottom_y))
        if self.has_left_wall:
            self._win.draw_line(left_line, fill_color)
        else:
            self._win.draw_line(left_line, "#d9d9d9")
        if self.has_right_wall:
            self._win.draw_line(right_line, fill_color)
        else:
            self._win.draw_line(right_line, "#d9d9d9")
        if self.has_top_wall:
            self._win.draw_line(top_line, fill_color)
        else:
            self._win.draw_line(top_line, "#d9d9d9")
        if self.has_bottom_wall:
            self._win.draw_line(bottom_line, fill_color)
        else:
            self._win.draw_line(bottom_line, "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"
        P1 = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        P2 = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)
        line = Line(P1, P2)
        self._win.draw_line(line, color)

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = [[] for _ in range(num_cols)]
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                P1 = Point(self._x1 + (i * self._cell_size_x), self._y1 + (j * self._cell_size_y))
                P2 = Point(self._x1 + ((i + 1) * self._cell_size_x), self._y1 + ((j + 1) * self._cell_size_y))
                self._cells[i].append(Cell(P1, P2, self._win))
                if self._win is not None:
                    self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw("black")
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        NW_cell = self._cells[0][0]
        SE_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        NW_cell.has_top_wall = False
        SE_cell.has_bottom_wall = False
        self._draw_cell(0,0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_directions = []
            if i != 0 and not self._cells[i - 1][j].visited:
                possible_directions.append(("left", i - 1, j))
            if i != self._num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append(("right", i + 1, j))
            if j != 0 and not self._cells[i][j - 1].visited:
                possible_directions.append(("up", i, j - 1))
            if j != self._num_rows - 1 and not self._cells[i ][j + 1].visited:
                possible_directions.append(("down", i, j + 1))
            if len(possible_directions) == 0:
                self._draw_cell(i, j)
                return
            direction, x, y = random.choice(possible_directions)
            if direction == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[x][y].has_bottom_wall = False
            if direction == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[x][y].has_top_wall = False
            if direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[x][y].has_left_wall = False
            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[x][y].has_right_wall = False
            self._break_walls_r(x, y)

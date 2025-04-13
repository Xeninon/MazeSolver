from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, P1, P2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = P1.x
        self._x2 = P2.x
        self._y1 = P1.y
        self._y2 = P2.y
        self._win = win
    
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
        if self.has_right_wall:
            self._win.draw_line(right_line, fill_color)
        if self.has_top_wall:
            self._win.draw_line(top_line, fill_color)
        if self.has_bottom_wall:
            self._win.draw_line(bottom_line, fill_color)

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"
        P1 = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        P2 = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)
        line = Line(P1, P2)
        self._win.draw_line(line, color)

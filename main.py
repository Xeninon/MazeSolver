from objects import *

def main():
    win = Window(800, 600)
    P1 = Point(100, 100)
    P2 = Point(300, 300)
    P3 = Point(300, 100)
    P4 = Point(500, 300)
    cell = Cell(P1, P2, win)
    cell2 = Cell(P3, P4, win)
    cell.has_right_wall = False
    cell2.has_left_wall = False
    cell.draw("black")
    cell2.draw("black")
    cell.draw_move(cell2)
    win.wait_for_close()
main()
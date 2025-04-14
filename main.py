from objects import *

def main():
    win = Window(1200, 900)
    maze = Maze(10, 10, 25, 25, 45, 30, win)
    maze.solve()
    win.wait_for_close()
main()
from objects import *

def main():
    win = Window(800, 600)
    Maze(10, 10, 10, 10, 75, 50, win)
    win.wait_for_close()
main()
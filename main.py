from graphics import *
from grid import *
import time



def main():
    win = Window(900, 900)

    p1 = Point(0, 0)
    p2 = Point(900, 900)
    grid = Grid(p1, p2, win)
    #time.sleep(10)
    grid.simulate_life()
    
    
    win.wait_for_close()
   



if __name__ == "__main__":
    main()    
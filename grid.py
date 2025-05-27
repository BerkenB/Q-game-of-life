from graphics import *
import numpy as np
import random
import time
from scipy.signal import convolve2d

class Grid:
    def __init__(self, p1, p2, win, seed = None):
        self.__p1 = p1
        self.__p2 = p2
        self.__win = win if win != None else None
        self.__segmentation_ratio = 100
        self.__state_tensor = np.random.choice([0, 1, 2, 3], size=(self.__segmentation_ratio, self.__segmentation_ratio),
                                              p=[0.7, 0.1, 0.1, 0.1]
                                              )
        

        #print("STATE", self.__state_tensor)
        self.__position_tensor = None
        np.random.seed(seed)

        self.__build_grid_tensor()
        self.__win.redraw()
    
    def __build_grid_tensor(self):
        row = int((self.__p2.x - self.__p1.x) / self.__segmentation_ratio)
        col = int((self.__p2.y - self.__p1.y) / self.__segmentation_ratio)
        position_tensor = np.empty(self.__state_tensor.shape, dtype=object)
        for i in range(self.__segmentation_ratio):
            for j in range(self.__segmentation_ratio):
                position_tensor[i, j] = ((self.__p1.x + j * row, self.__p1.y + i * row), (self.__p1.x + (j+1) * row, self.__p1.y + (i+1) * row))
        self.__position_tensor = position_tensor
            
    def __state_iterator(self):
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        mask1 = (self.__state_tensor==1).astype(int)
        mask2 = (self.__state_tensor==2).astype(int)
        mask3 = (self.__state_tensor==3).astype(int)
        count1 = convolve2d(mask1, kernel, mode='same', boundary='wrap')
        count2 = convolve2d(mask2, kernel, mode='same', boundary='wrap')
        count3 = convolve2d(mask3, kernel, mode='same', boundary='wrap')

        next_grid = np.zeros_like(self.__state_tensor)
        grid = self.__state_tensor
        for i in range(self.__segmentation_ratio):
            for j in range(self.__segmentation_ratio):
                state = grid[i, j]
                # Survival for live cells
                if state == 1 and (count1[i, j] in (2, 3)):
                    next_grid[i, j] = 1
                elif state == 2 and (count2[i, j] in (2, 3)):
                    next_grid[i, j] = 2
                elif state == 3 and (count3[i, j] in (2, 3)):
                    next_grid[i, j] = 3
                else:
                    # Birth on exactly 3 neighbors of a state
                    if state == 0:
                        if count1[i, j] == 3:
                            next_grid[i, j] = 1
                        elif count2[i, j] == 3:
                            next_grid[i, j] = 2
                        elif count3[i, j] == 3:
                            next_grid[i, j] = 3
                        elif count1[i, j] == 6:
                            next_grid[i, j] = 1
                        elif count2[i, j] == 6:
                            next_grid[i, j] = 2
                        elif count3[i, j] == 6:
                            next_grid[i, j] = 3
                    else:
                        next_grid[i, j] = 0
        return next_grid
    
    def simulate_life(self):
        canvas = self.__win.get_canvas()

        for _ in range(1000):
            canvas.delete("all")
            next_state_tensor = self.__state_iterator()
            #print("NEXT:", next_state_tensor)
            rows, cols = next_state_tensor.shape
            rects = []
            for i in range(rows):
                for j in range(cols):
                    if next_state_tensor[i, j] == 0:
                        rects.append(self.__win.draw_rectangle(self.__position_tensor[i, j][0][0],
                                                self.__position_tensor[i, j][0][1],
                                                self.__position_tensor[i, j][1][0],
                                                self.__position_tensor[i, j][1][1], "black", "black"))
                    elif next_state_tensor[i, j] == 1:
                        rects.append(self.__win.draw_rectangle(self.__position_tensor[i, j][0][0],
                                                self.__position_tensor[i, j][0][1],
                                                self.__position_tensor[i, j][1][0],
                                                self.__position_tensor[i, j][1][1], "yellow", "yellow"))
                    elif next_state_tensor[i, j] == 2:
                        rects.append(self.__win.draw_rectangle(self.__position_tensor[i, j][0][0],
                                                self.__position_tensor[i, j][0][1],
                                                self.__position_tensor[i, j][1][0],
                                                self.__position_tensor[i, j][1][1], "blue", "blue"))
                    else:
                        rects.append(self.__win.draw_rectangle(self.__position_tensor[i, j][0][0],
                                                self.__position_tensor[i, j][0][1],
                                                self.__position_tensor[i, j][1][0],
                                                self.__position_tensor[i, j][1][1], "red", "red"))
            self.__win.redraw()
            
            #print("POSITIONS: ", self.__position_tensor)
            #time.sleep(0.0001)
            self.__state_tensor = next_state_tensor
            


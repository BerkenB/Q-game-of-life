from tkinter import Tk, BOTH, Canvas, Button

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg = "black",  width=width, height=height)
        self.__canvas.pack(fill = BOTH, expand = 1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def get_canvas(self):
        return self.__canvas
    def close_window(self):
        self.__root.destroy()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def draw_rectangle(self, x1, y1, x2, y2, fill_color, outline_color):
        self.__canvas.create_rectangle(x1, y1, x2, y2, fill = fill_color, outline = outline_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill = fill_color, width = 2
        )
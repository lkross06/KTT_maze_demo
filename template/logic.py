import tkinter as tk
from time import sleep
import maze as m

class Logic:

    def __init__(self):
        self.wall = "w"
        self.empty = "."
        self.start = "s"
        self.end = "e"

        self.root = tk.Tk() #the window itself
        self.root.title("maze demo")

        self.n = 8
        self.cell_size = 35 #number of pixels in each square
        self.canvas = tk.Canvas(
            self.root,
            width = self.n * self.cell_size, 
            height = self.n * self.cell_size
        )

        self.ppos = None #[r,c] in maze
        self.pdir = "east" #start facing right

        self.maze = None #2D array representing maze
        self.win = False

        self.load_maze1()

        #start main loop
        self.root.mainloop()

    def _redraw(self):

        #redraw all the cells
        for row in range(self.n):
            for col in range(self.n):
                
                #top-left coord
                x0 = col * self.cell_size
                y0 = row * self.cell_size

                #bottom-right coord
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                color = self._get_cell_color(self.maze[row][col])
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

        #get coords for player
        x0 = self.ppos[1] * self.cell_size
        y0 = self.ppos[0] * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size

        #redraw player
        points = self._get_triangle_points(x0, y0, x1, y1) #gets the triangle points depending on direction
        self.canvas.create_polygon(points, fill="green", outline="green")

        if self.win:
            self.canvas.create_text(
                (self.n * self.cell_size) / 2, 
                self.cell_size/2, #centers the text on the middle of the top left text box
                text="YOU WIN!", 
                fill="yellow", 
                font=('Helvetica ' + str(int(self.cell_size * 0.5)) + ' bold')
            )

    def _get_triangle_points(self, x0, y0, x1, y1):

        #make an indent that is 1/n th of the cell width
        m = 5
        indent = (1/m) * self.cell_size

        s = (3/m) * self.cell_size #width of smaller cell

        x0 += indent
        y0 += indent
        x1 -= indent
        y1 -= indent

        if self.pdir == "north":
            return [
                x0 + (s/2), y0,
                x0, y1,
                x1, y1
            ]
        elif self.pdir == "south":
            return [
                x0, y0,
                x1, y0,
                x0 + (s/2), y1
            ]
        elif self.pdir == "east":
            return [
                x1, y0 + (s/2),
                x0, y0,
                x0, y1
            ]
        elif self.pdir == "west":
            return [
                x0, y0 + (s/2),
                x1, y0,
                x1, y1
            ]

    def _find_start(self): #find the starting cell (or first occurence), return as [r,c]
        for row in range(self.n):
            for col in range(self.n):
                if self.maze[row][col] == self.start:
                    return [row, col]

    def _get_cell_color(self, sq): #returns the corresponding cell color depending on the maze square value

        legend = {
            self.wall:"black",
            self.empty:"white",
            self.start:"blue",
            self.end:"red"
        }

        color = legend.get(sq)
        if color == None:
            color = "white" #if theres an unknown value, just return blank space
        return color
    
    def _update_canvas(self):
        
        self.canvas.destroy()
        self.win = False #reset win and player coords

        #add canvas to tkinter root
        self.canvas = tk.Canvas(
            self.root,
            width = self.n * self.cell_size, 
            height = self.n * self.cell_size
        )
        self.canvas.pack()

        #update player position
        self.ppos = self._find_start()

        #draw everything onto the canvas
        self._redraw()
        
    def load_maze1(self):
        self.cell_size = 35 #35 * 8 = 280
        self.n = 8
        self.maze = m.maze1

        self._update_canvas()

    def load_maze2(self):
        self.cell_size = 28 #28 * 10 = 280
        self.n = 10
        self.maze = m.maze2

        self._update_canvas()
    
    def load_maze3(self):
        self.cell_size = 20 #20 * 14 = 280
        self.n = 14
        self.maze = m.maze3

        self._update_canvas()
            
    def turn_left(self):
        if self.pdir == "east":
            self.pdir = "north"
        elif self.pdir == "north":
            self.pdir = "west"
        elif self.pdir == "west":
            self.pdir = "south"
        elif self.pdir == "south":
            self.pdir = "east"

        self._redraw()

    def turn_right(self):
        if self.pdir == "east":
            self.pdir = "south"
        elif self.pdir == "south":
            self.pdir = "west"
        elif self.pdir == "west":
            self.pdir = "north"
        elif self.pdir == "north":
            self.pdir = "east"

        self._redraw()

    def move_forward(self):

        next_pos = [] #coords of the cell in front of the player
        next_cell = None #value of the cell

        #we don't have to check to make sure that the player is in the bounds of the maze
        #since each maze will have a ring of walls around it
        if self.pdir == "north":
            next_pos = [self.ppos[0] - 1, self.ppos[1]] #go up 1 row
        elif self.pdir == "south":
            next_pos = [self.ppos[0] + 1, self.ppos[1]] #go down 1 row
        elif self.pdir == "east":
            next_pos = [self.ppos[0], self.ppos[1] + 1] #go up 1 column
        elif self.pdir == "west":
            next_pos = [self.ppos[0], self.ppos[1] - 1] #go down 1 column

        next_cell = self.maze[next_pos[0]][next_pos[1]]

        if next_cell == self.wall: #if there's a wall, don't move
            return
        
        self.ppos = next_pos

        if self.maze[self.ppos[0]][self.ppos[1]] == self.end:
            self.win = True
        else:
            self.win = False

        self._redraw()

    def wall_in_front(self):

        next_pos = [] #coords of the cell in front of the player
        next_cell = None #value of the cell

        #we don't have to check to make sure that the player is in the bounds of the maze
        #since each maze will have a ring of walls around it
        if self.pdir == "north":
            next_pos = [self.ppos[0] - 1, self.ppos[1]] #go up 1 row
        elif self.pdir == "south":
            next_pos = [self.ppos[0] + 1, self.ppos[1]] #go down 1 row
        elif self.pdir == "east":
            next_pos = [self.ppos[0], self.ppos[1] + 1] #go up 1 column
        elif self.pdir == "west":
            next_pos = [self.ppos[0], self.ppos[1] - 1] #go down 1 column

        next_cell = self.maze[next_pos[0]][next_pos[1]]

        return next_cell == self.wall
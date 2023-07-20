import tkinter as tk
from time import sleep

def update_canvas(m, ca, r, c, pp):

    #redraw all the cells
    for row in range(r):
        for col in range(c):
            
            #top-left coord
            x0 = col * cell_size
            y0 = row * cell_size

            #bottom-right coord
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            color = get_cell_color(m[row][col])
            ca.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    #get coords for player
    x0 = pp[1] * cell_size
    y0 = pp[0] * cell_size
    x1 = x0 + cell_size
    y1 = y0 + cell_size

    #redraw player
    points = get_triangle_points(x0, y0, x1, y1) #gets the triangle points depending on direction
    ca.create_polygon(points, fill="green", outline="green")

def get_triangle_points(x0, y0, x1, y1):

    #make an indent that is 1/n th of the cell width
    n = 5
    indent = (1/n) * cell_size

    s = (3/n) * cell_size #width of smaller cell

    x0 += indent
    y0 += indent
    x1 -= indent
    y1 -= indent

    if player_dir == "north":
        return [
            x0 + (s/2), y0,
            x0, y1,
            x1, y1
        ]
    elif player_dir == "south":
        return [
            x0, y0,
            x1, y0,
            x0 + (s/2), y1
        ]
    elif player_dir == "east":
        return [
            x1, y0 + (s/2),
            x0, y0,
            x0, y1
        ]
    elif player_dir == "west":
        [
            x0, y0 + (s/2),
            x1, y0,
            x1, y1
        ]

def find_start(m, r, c): #find the starting cell (or first occurence), return as [r,c]
    for row in range(r):
        for col in range(c):
            if m[row][col] == st:
                return [row, col]

def get_cell_color(sq): #returns the corresponding cell color depending on the maze square value

    legend = {
        wall:"black",
        null:"white",
        st:"blue",
        end:"red"
    }
    color = legend.get(sq)
    if color == None:
        color = "white" #if theres an unknown value, just return blank space
    return color

def choose_maze(n): #n between 1-3 for different mazes
    maze1 = [
        ['w', 'w', 'w', 'w', 'w', 'w', 'w'],
        ['w', 'e', '.', '.', 'w', '.', 'w'],
        ['w', 'w', 'w', '.', '.', '.', 'w'],
        ['w', '.', 'w', 'w', '.', 'w', 'w'],
        ['w', '.', '.', '.', '.', '.', 'w'],
        ['w', 'w', '.', 'w', 'w', '.', 'w'],
        ['w', 's', '.', 'w', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w'],
    ]
    maze2 = [
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
        ['w', '.', '.', '.', 'w', '.', '.', '.', 'w'],
        ['w', '.', 'w', '.', '.', '.', 'w', '.', 'w'],
        ['w', 'w', 'w', 'w', '.', 'w', 'w', 'e', 'w'],
        ['w', '.', '.', 'w', '.', '.', 'w', 'w', 'w'],
        ['w', 'w', '.', 'w', 'w', '.', 'w', '.', 'w'],
        ['w', '.', '.', '.', 'w', '.', '.', '.', 'w'],
        ['w', 's', 'w', '.', '.', '.', 'w', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
    ]
    maze3 = [
        ['w', 'w', 'w', 'w', 'w', 'w', 'w'],
        ['w', '.', '.', '.', 'w', 'e', 'w'],
        ['w', '.', 'w', '.', '.', '.', 'w'],
        ['w', '.', 'w', 'w', '.', 'w', 'w'],
        ['w', '.', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', '.', 'w'],
        ['w', 's', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w'],
    ]
    
    if n == 1:
        start(maze1)
    elif n == 2:
        start(maze2)
    elif n == 3:
        start(maze3)
    else:
        raise ValueError()
    
def turn_left():
    print("turn left")
    if player_dir == "east":
        player_dir == "north"
    elif player_dir == "north":
        player_dir == "west"
    elif player_dir == "west":
        player_dir == "south"
    elif player_dir == "south":
        player_dir == "east"

def turn_right():
    print("turn right")
    if player_dir == "east":
        player_dir == "south"
    elif player_dir == "south":
        player_dir == "west"
    elif player_dir == "west":
        player_dir == "north"
    elif player_dir == "north":
        player_dir == "east"

def move_forward():
    print("move forward")

    next_pos = [] #coords of the cell in front of the player
    next_cell = None #value of the cell

    #we don't have to check to make sure that the player is in the bounds of the maze
    #since each maze will have a ring of walls around it
    if player_dir == "north":
        next_pos = [player_pos[0] - 1, player_pos[1]] #go up 1 row
    elif player_dir == "south":
        next_pos = [player_pos[0] + 1, player_pos[1]] #go down 1 row
    elif player_dir == "east":
        next_pos = [player_pos[0], player_pos[1] + 1] #go up 1 column
    elif player_dir == "west":
        next_pos = [player_pos[0], player_pos[1] - 1] #go down 1 column

    next_cell = maze[next_pos[0]][next_pos[1]]

    if next_cell == wall: #if there's a wall, don't move
        return
    
    player_pos = next_pos
    
    if player_pos == end:
        print("you win!") #TODO: make a better win

    update_canvas(maze, canvas, rows, cols, player_pos)

def start(m):
    maze = m
    rows = len(m)
    cols = len(m[0])

    #add canvas to tkinter root
    canvas = tk.Canvas(root, width=(cols * cell_size), height=(rows * cell_size))
    canvas.pack()

    #update player position
    player_pos = find_start(maze, rows, cols)

    #draw everything onto the canvas
    update_canvas(maze, canvas, rows, cols, player_pos)

    #start main loop
    root.mainloop() #TODO: nothing runs after this bc tkinter is event-based. button to run program?

"""
spaces in the maze are represented by these characters:
w   wall
.   null/empty space
s   start
e   end
"""
wall = "w"
null = "."
st = "s"
end = "e"

root = tk.Tk() #the window itself
root.title("maze demo")

canvas = None
rows = None
cols = None
cell_size = 40 #number of pixels in each square

maze = None #2D array representing maze

player_pos = None #[r,c] in maze
player_dir = "east" #start facing right

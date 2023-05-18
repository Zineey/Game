from tkinter import messagebox, Tk
import pygame as pg
import sys


pg.init()

height, width = 500, 500
screen = pg.display.set_mode((height,width))
columns = 20
rows = 20
margin = 2

box_width = width//columns
box_height = height//rows

grid = []
queue = []
path = []

clock = pg.time.Clock()

class Grid:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.goal = False
        self.wall = False
        self.queued = False
        self.visited = False
        self.neighbors = []
        self.prior = None
    
    # Drawing grid
    def draw(self, win, color):
        pg.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - margin, box_height - margin))

    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Grid(i,j))
    grid.append(arr)

# Generate the neighbors
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbors()


# Try Grenerating random start and random end
start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def main():
    start_search = False
    set_goal = False
    searching = True
    goal = None

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()   
                sys.exit()
    
            # Mouse event handler
            elif event.type == pg.MOUSEMOTION:
                x = pg.mouse.get_pos()[0]
                y = pg.mouse.get_pos()[1]
                # On mouse click get index for i and j
                if event.buttons[0]:
                    i = x//box_width
                    j = y//box_height
                    grid[i][j].wall = True
                if event.buttons[2] and not set_goal:
                    i = x//box_width
                    j = y//box_height
                    goal = grid[i][j]
                    goal.goal = True
                    set_goal = True
            
            if event.type == pg.KEYDOWN and set_goal:
                    start_search = True

        if start_search:
                if len(queue) > 0 and searching:
                    curr_box = queue.pop(0)
                    curr_box.visited = True
                    if curr_box == goal:
                        searching = False
                        while curr_box.prior != start_box:
                            path.append(curr_box.prior)
                            curr_box = curr_box.prior
                    else:
                        for neighbor in curr_box.neighbors:
                            if not neighbor.queued and not neighbor.wall:
                                neighbor.queued = True
                                neighbor.prior = curr_box
                                queue.append(neighbor)
                else:
                    if searching:
                        Tk().wm_withdraw()
                        messagebox.showinfo("No Solution", "There is no possible solution!")
                        searching = False

        screen.fill((255,255,255))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(screen,(0,0,0))

                if box.queued:
                    box.draw(screen, (245,222,179))
                if box.visited:
                    box.draw(screen, (250,235,215))
                if box in path:
                    box.draw(screen, (139,69,19))


                if box.start:
                    box.draw(screen, (0,255,0))
                if box.wall:
                    box.draw(screen, (0,69,0))
                if box.goal:
                    box.draw(screen, (0,0,255))


        clock.tick(60)
        pg.display.flip()

main()
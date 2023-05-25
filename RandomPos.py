import random
# function for generating random position ng player and goal state in the maze without overlapping wall ( 1 ) 
def randomPos(maze):
    height = len(maze)
    width = len(maze[0])
    while True:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if maze[y][x] != 1:
            return (x, y)   
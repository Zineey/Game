import pygame 
import sys
from MapGenerator import mapGenerator
from RandomPos import randomPos
from tkinter import messagebox
from heapq import heappush, heappop

# Define colors
# WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

pygame.init() 
running = True
clock = pygame.time.Clock()


WIDTH = 750
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Not a Horror Game!")

CELL_SIZE = 28
GRID_WIDTH = WIDTH//CELL_SIZE
GRID_HEIGHT = HEIGHT//CELL_SIZE


# bg = pygame.image.load('assets/bg.png')

player = pygame.image.load('assets/player.png')
player = pygame.transform.scale(player, (CELL_SIZE, CELL_SIZE))

goal = pygame.image.load('assets/goal.gif')
goal = pygame.transform.scale(goal, (CELL_SIZE, CELL_SIZE))

wall = pygame.image.load('assets/wall.webp')
wall = pygame.transform.scale(wall, (CELL_SIZE, CELL_SIZE))

# Generates random maze
maze = mapGenerator(27, 27)
GRID_WIDTH = len(maze[0])
GRID_HEIGHT = len(maze)

# Generates random position for player and goal
player_pos = randomPos(maze)
goal_pos = randomPos(maze)

# Algorithm Start
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def aStar(start, goal):
    queue = []
    heappush(queue, (0, start))
    visited = {}
    g_score = {start: 0}

    while queue:
        cur_node = heappop(queue)[1]

        if cur_node == goal:
            path = []
            while cur_node in visited:
                path.append(cur_node)
                cur_node = visited[cur_node]
            return path[::-1]

        for next_node in [(cur_node[0] - 1, cur_node[1]), (cur_node[0] + 1, cur_node[1]),
                          (cur_node[0], cur_node[1] - 1), (cur_node[0], cur_node[1] + 1)]:
            
            if next_node[0] >= 0 and next_node[0] < GRID_WIDTH and next_node[1] >= 0 and next_node[1] < GRID_HEIGHT:
                new_cost = g_score[cur_node] + 1

                if maze[next_node[1]][next_node[0]] != 1 and (next_node not in g_score or new_cost < g_score[next_node]):
                    g_score[next_node] = new_cost
                    priority = new_cost + heuristic(next_node, goal)
                    heappush(queue, (priority, next_node))
                    visited[next_node] = cur_node

show_Solution = False
path = []

while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                show_Solution = True
            if event.key == pygame.K_r:
                if messagebox.askyesno("Restart", "Are you sure you want to restart? This will generate new Map") == True: 
                    maze = mapGenerator(27, 27)
                    GRID_WIDTH = len(maze[0])
                    GRID_HEIGHT = len(maze)
                    player_pos = randomPos(maze)
                    goal_pos = randomPos(maze)
                    show_Solution = False
                    path = []
                else:
                    pass

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] != 1:
            player_pos = (player_pos[0], player_pos[1] - 1)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if player_pos[1] < GRID_HEIGHT - 1 and maze[player_pos[1] + 1][player_pos[0]] != 1:
            player_pos = (player_pos[0], player_pos[1] + 1)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]: 
        if player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] != 1:
            player_pos = (player_pos[0] - 1, player_pos[1])
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
        if player_pos[0] < GRID_WIDTH - 1 and maze[player_pos[1]][player_pos[0] + 1] != 1:
            player_pos = (player_pos[0] + 1, player_pos[1])

    
    if show_Solution:
        path = aStar(player_pos, goal_pos)
        show_Solution = False


    screen.fill(BLACK)
    # screen.blit(bg, (0, 0))

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                screen.blit(wall, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    screen.blit(player, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    screen.blit(goal, (goal_pos[0] * CELL_SIZE, goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if path:
        show_Solution = True
        for i in range(len(path) - 1):
            start = (path[i][0] * CELL_SIZE + CELL_SIZE // 2, path[i][1] * CELL_SIZE + CELL_SIZE // 2)
           
            end = (path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2, path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(screen, GREEN, start, end, 3)

    if player_pos == goal_pos:
        if messagebox.askyesno("Play Again?", "Do you want to play again?") == False:
            messagebox.showinfo("Thanks for Playing!", "Thanks for playing!")
            running = False
        else:
            maze = mapGenerator(27, 27)
            GRID_WIDTH = len(maze[0])
            GRID_HEIGHT = len(maze)
            player_pos = randomPos(maze)
            goal_pos = randomPos(maze)
            show_Solution = False
            path = []

    clock.tick(15)

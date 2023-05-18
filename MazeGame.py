import pygame 
import sys
import random
from MapGenerator import generate_maze
from tkinter import messagebox

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

pygame.init()
running = True
show_path = False
path = []

clock = pygame.time.Clock()

WIDTH = 750
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love is Colorblind")

CELL_SIZE = 28
GRID_WIDTH = WIDTH//CELL_SIZE
GRID_HEIGHT = HEIGHT//CELL_SIZE

player = pygame.image.load('assets/player.png')
player = pygame.transform.scale(player, (30, 30))

goal = pygame.image.load('assets/goal.png')
goal = pygame.transform.scale(goal, (30, 30))

X = random.randint(0,CELL_SIZE-1)
Y = random.randint(0,CELL_SIZE-1)
player_pos = (X, Y)

X = random.randint(0,CELL_SIZE-1)
Y = random.randint(0,CELL_SIZE-1)
goal_pos = (X, Y)


# Generates random maze
maze = generate_maze(27, 27)


GRID_WIDTH = len(maze[0])
GRID_HEIGHT = len(maze)

while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                show_path = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] != 1:
        player_pos = (player_pos[0], player_pos[1] - 1)
    elif keys[pygame.K_s] and player_pos[1] < GRID_HEIGHT - 1 and maze[player_pos[1] + 1][player_pos[0]] != 1:
        player_pos = (player_pos[0], player_pos[1] + 1)
    elif keys[pygame.K_a] and player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] != 1:
        player_pos = (player_pos[0] - 1, player_pos[1])
    elif keys[pygame.K_d] and player_pos[0] < GRID_WIDTH - 1 and maze[player_pos[1]][player_pos[0] + 1] != 1:
        player_pos = (player_pos[0] + 1, player_pos[1])


    screen.fill(BLACK)




    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE , y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # elif maze[y][x] == 2:
            #     screen.blit(goal_state, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    screen.blit(player, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    screen.blit(goal, (goal_pos[0] * CELL_SIZE, goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if player_pos == goal_pos:
        messagebox.showinfo("Wow You just found your Love of your Life", "Ultimate Green Flag!!" )
        running = False

    clock.tick(10)

import pygame 
import sys
import random
from MapGenerator import mapGenerator
from RandomPos import randomPos
from tkinter import messagebox

# Define colors
# WHITE = (255, 255, 255)
# BROWN = (139, 69, 19)
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

player = pygame.image.load('assets/player.png')
player = pygame.transform.scale(player, (CELL_SIZE, CELL_SIZE))

goal = pygame.image.load('assets/goal.png')
goal = pygame.transform.scale(goal, (CELL_SIZE, CELL_SIZE))

# Generates random maze
maze = mapGenerator(27, 27)

# Generates random position for player and goal
player_pos = randomPos(maze)
goal_pos = randomPos(maze)


GRID_WIDTH = len(maze[0])
GRID_HEIGHT = len(maze)

while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_t:
        #         show_path = True

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


    screen.fill(BLACK)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, GREEN, (x * CELL_SIZE , y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    screen.blit(player, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    screen.blit(goal, (goal_pos[0] * CELL_SIZE, goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if player_pos == goal_pos:
        messagebox.showinfo("You Win!", "*BOO!*")
        running = False

    clock.tick(10)

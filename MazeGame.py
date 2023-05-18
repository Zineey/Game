import pygame 
import sys
import random
from MapGenerator import generate_maze

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

pygame.init()
running = True
clock = pygame.time.Clock()

WIDTH = 750
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

CELL_SIZE = 25
GRID_WIDTH = WIDTH//CELL_SIZE
GRID_HEIGHT = HEIGHT//CELL_SIZE

maze = generate_maze(GRID_HEIGHT, GRID_WIDTH)


GRID_WIDTH = len(maze[0])
GRID_HEIGHT = len(maze)

while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    screen.fill(BLACK)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE , y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # elif maze[y][x] == 2:
            #     screen.blit(goal_state, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    

    clock.tick(10)

import pygame
import heapq
import random
from tkinter import messagebox, Tk

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 700, 770
window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Love is Color Blind")

# Define cell size and grid dimensions
CELL_SIZE = 26
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
font = pygame.font.Font(None,30)
font2 = pygame.font.Font(None,30)

# Player
player = pygame.image.load('cat.png')
player = pygame.transform.scale(player, (30, 30))

# Goal
goal_state = pygame.image.load('cat love.png')
goal_state = pygame.transform.scale(goal_state, (30, 30))


# Define player starting position and goal position
# player_pos = (0, 4)
X = random.randint(0,CELL_SIZE-1)
Y = random.randint(0,CELL_SIZE-1)
player_pos = (X, Y)

goal_pos = (GRID_WIDTH - 1, GRID_HEIGHT - 1)


def generate_maze(rows, cols):
    # Initialize maze matrix with all walls
    maze = [[1] * cols for _ in range(rows)]

    # Set starting position and stack for backtracking
    stack = [(1, 1)]
    maze[1][1] = 0

    # Directions: (row, col)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while stack:
        current_row, current_col = stack[-1]
        neighbors = []

        # Check available neighbors
        for direction in directions:
            next_row = current_row + 2 * direction[0]
            next_col = current_col + 2 * direction[1]

            if 0 < next_row < rows and 0 < next_col < cols and maze[next_row][next_col] == 1:
                neighbors.append((next_row, next_col))

        if neighbors:
            # Choose random neighbor
            next_row, next_col = random.choice(neighbors)

            # Remove wall between current and next cell
            maze[current_row + (next_row - current_row) // 2][current_col + (next_col - current_col) // 2] = 0

            # Mark next cell as visited
            maze[next_row][next_col] = 0

            # Add next cell to stack
            stack.append((next_row, next_col))
        else:
            # Dead end reached, backtrack
            stack.pop()

    # Set goal state as 2
    maze[rows - 2][cols - 2] = 2

    return maze

# Example usage
rows = 29
cols = 29
maze = generate_maze(rows, cols)

# Determine dimensions of the maze
GRID_WIDTH = len(maze[0])
GRID_HEIGHT = len(maze)

def heuristic(a, b):
    """Calculate the Manhattan distance heuristic between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    """A* algorithm implementation."""
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and maze[next_y][next_x] != 1:
                new_g_score = g_score[current] + 1

                if next_pos not in g_score or new_g_score < g_score[next_pos]:
                    g_score[next_pos] = new_g_score
                    priority = new_g_score + heuristic(goal, next_pos)
                    heapq.heappush(open_set, (priority, next_pos))
                    came_from[next_pos] = current

    return None  # No path found

# Game loop
running = True
clock = pygame.time.Clock()
solve_maze = False
path = []
while running:
    pygame.display.update()
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                solve_maze = True
            elif solve_maze == True and event.key == pygame.K_t:
                solve_maze = False

    # Handle player movement
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] != 1:
        player_pos = (player_pos[0], player_pos[1] - 1)
    elif keys[pygame.K_s] and player_pos[1] < GRID_HEIGHT - 1 and maze[player_pos[1] + 1][player_pos[0]] != 1:
        player_pos = (player_pos[0], player_pos[1] + 1)
    elif keys[pygame.K_a] and player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] != 1:
        player_pos = (player_pos[0] - 1, player_pos[1])
    elif keys[pygame.K_d] and player_pos[0] < GRID_WIDTH - 1 and maze[player_pos[1]][player_pos[0] + 1] != 1:
        player_pos = (player_pos[0] + 1, player_pos[1])
    
    # Solve maze using A* algorithm
    if solve_maze:
        path = a_star(player_pos, goal_pos)
        solve_maze = False  # Reset the flag
    
    # Clear the screen
    window.fill(BLACK)
    
    # Draw maze
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(window, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == 2:
                window.blit(goal_state, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                # pygame.draw.rect(window, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    
    # Draw player
    window.blit(player, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # pygame.draw.rect(window, GREEN, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
     # Draw guiding line
    if path:
        solve_maze = True
        for i in range(len(path) - 1):
            start = (path[i][0] * CELL_SIZE + CELL_SIZE // 2, path[i][1] * CELL_SIZE + CELL_SIZE // 2)
           
            end = (path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2, path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(window, RED, start, end, 3)
    # Update the display
    

    # Quit the game if the maze is solved
    if player_pos == goal_pos:
        Tk().wm_withdraw()
        messagebox.showinfo("Meow", "Hapi Hapi Hapi!" )
        running = False    
    clock.tick(10)

# Quit the game
pygame.quit()
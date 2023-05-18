import random
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

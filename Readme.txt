Assets Na laaaaang then we're done here

Ito yung Map Generator na may spikes kung gusto

# def mapGenerator(rows,cols):
#     maze = [[1] * cols for _ in range(rows)]

#     stack = [(1, 1)]
#     maze[1][1] = 0

#     # Directions: (row, col)
#     directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

#     while stack:
#         current_row, current_col = stack[-1]
#         neighbors = []

#         # Check available neighbors
#         for direction in directions:
#             next_row = current_row + 2 * direction[0]
#             next_col = current_col + 2 * direction[1]

#             if 0 < next_row < rows and 0 < next_col < cols and maze[next_row][next_col] == 1:
#                 neighbors.append((next_row, next_col))

#         if neighbors:
#             # Choose random neighbor
#             next_row, next_col = random.choice(neighbors)

#             # Remove wall between current and next cell
#             maze[current_row + (next_row - current_row) // 2][current_col + (next_col - current_col) // 2] = 0

#             # Mark next cell as visited
#             maze[next_row][next_col] = 0

#             # Add next cell to stack
#             stack.append((next_row, next_col))
#         else:
#             # Dead end reached, backtrack
#             stack.pop()

#     walls = [(i, j) for i in range(rows) for j in range(cols) if maze[i][j] == 1]

#     # Add spikes (2) randomly in the same column or row as walls
#     num_spikes = random.randint(5, 10)  # Random number of spikes between 5 and 10
#     spike_positions = random.sample(walls, num_spikes)
#     for spike_pos in spike_positions:
#         maze[spike_pos[0]][spike_pos[1]] = 2

#     return maze
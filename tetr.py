import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Define the score display position
score_position = (650, 20)


# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange = (255, 165, 0)

# Define Tetrimino shapes
tetriminoes = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1], [1, 1]],  # O-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1, 0], [0, 1, 1]],  # Z-shape
    [[0, 1, 1], [1, 1, 0]],  # S-shape
    [[1, 1, 1], [0, 0, 1]],  # L-shape
    [[1, 1, 1], [1, 0, 0]]  # J-shape
]

# Set Tetrimino colors
tetrimino_colors = [cyan, yellow, magenta, green, red, blue, orange]

# Define the game grid
grid = [[0] * 10 for _ in range(20)]  # 10x20 grid

# Set the Tetrimino position and index
tetrimino_position = [0, 0]
tetrimino_index = random.randint(0, 6)

# Set the game clock
clock = pygame.time.Clock()

# Set the game over flag
game_over = False

# Set the player's score
score = 0

# Function to draw the grid
def draw_grid():
    for row in range(20):
        for col in range(10):
            pygame.draw.rect(window, white, pygame.Rect(col * 30, row * 30, 30, 30), 1)
            if grid[row][col] != 0:
                pygame.draw.rect(window, tetrimino_colors[grid[row][col] - 1], pygame.Rect(col * 30, row * 30, 30, 30))

# Function to draw the Tetrimino
def draw_tetrimino():
    tetrimino_shape = tetriminoes[tetrimino_index]
    for row in range(len(tetrimino_shape)):
        for col in range(len(tetrimino_shape[0])):
            if tetrimino_shape[row][col] == 1:
                pygame.draw.rect(window, tetrimino_colors[tetrimino_index], pygame.Rect((tetrimino_position[1] + col) * 30, (tetrimino_position[0] + row) * 30, 30, 30))

# Function to check if Tetrimino collides with the grid or other Tetriminos
def check_collision(tetrimino_shape=None, position=None):
    if tetrimino_shape is None:
        tetrimino_shape = tetriminoes[tetrimino_index]
    if position is None:
        position = tetrimino_position
    for row in range(len(tetrimino_shape)):
        for col in range(len(tetrimino_shape[0])):
            if tetrimino_shape[row][col] == 1:
                if position[0] + row >= 20 or position[1] + col < 0 or position[1] + col >= 10 or grid[position[0] + row][position[1] + col] != 0:
                    return True
    return False

# Function to rotate the Tetrimino
def rotate_tetrimino():
    global tetrimino_index
    rotated_tetrimino_shape = list(zip(*reversed(tetriminoes[tetrimino_index])))
    if tetrimino_position[1] + len(rotated_tetrimino_shape[0]) > 10:
        tetrimino_position[1] = 10 - len(rotated_tetrimino_shape[0])
    if not check_collision(rotated_tetrimino_shape):
        tetriminoes[tetrimino_index] = rotated_tetrimino_shape

# Function to place the Tetrimino in the grid
def place_tetrimino():
    tetrimino_shape = tetriminoes[tetrimino_index]
    for row in range(len(tetrimino_shape)):
        for col in range(len(tetrimino_shape[0])):
            if tetrimino_shape[row][col] == 1:
                grid[tetrimino_position[0] + row][tetrimino_position[1] + col] = tetrimino_index + 1

# Function to clear completed rows
def clear_rows():
    global score
    completed_rows = []
    for row in range(len(grid)):
        if all(grid[row]):
            completed_rows.append(row)
    for row in completed_rows:
        grid.pop(row)
        grid.insert(0, [0] * 10)
        score += 10 * len(completed_rows)

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetrimino_position[1] -= 1
                if check_collision():
                    tetrimino_position[1] += 1
            elif event.key == pygame.K_RIGHT:
                tetrimino_position[1] += 1
                if check_collision():
                    tetrimino_position[1] -= 1
            elif event.key == pygame.K_DOWN:
                tetrimino_position[0] += 1
                if check_collision():
                    tetrimino_position[0] -= 1
            elif event.key == pygame.K_UP:
                rotate_tetrimino()

    if not check_collision():
        tetrimino_position[0] += 1
    else:
        tetrimino_position[0] -= 1  # Move the Tetrimino up by 1 row instead of setting game_over to True

        place_tetrimino()
        clear_rows()
        tetrimino_position = [0, 3]
        tetrimino_index = random.randint(0, 6)

        if check_collision():
            game_over = True

    # Clear the window
    window.fill(black)

    # Draw the grid and Tetrimino
    draw_grid()
    draw_tetrimino()
    

    # Display the score
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render("Score: " + str(score), True, white)
    window.blit(score_text, score_position)

    # Update the display
    pygame.display.flip()

    # Set the game speed
    clock.tick(5)


# Game over message
font = pygame.font.SysFont("Arial", 36)
game_over_message = font.render("Game Over", True, red)
game_over_rect = game_over_message.get_rect(center=(width / 2, height / 2))
window.blit(game_over_message, game_over_rect)

# Show the final score
score_message = font.render("Score: " + str(score), True, white)
score_rect = score_message.get_rect(center=(width / 2, height / 2 + 50))
window.blit(score_message, score_rect)

# Update the display
pygame.display.flip()

# Wait for a while before quitting
pygame.time.wait(2000)

# Quit the game
pygame.quit()

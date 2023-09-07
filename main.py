from minesweeper import sprites
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display

# Beg, Int, Adv grid size init
beginner_grid = [10, 10, 40]
intermediate_grid = [16, 16, 40]
advanced_grid = [30, 16, 99]

tile_size = 16  # Size of each tile in pixels
grid_size = 20   # Size of the grid
screen_width = 300
screen_height = 372.5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Choose Difficulty")

# Create a TileBuilder with the monochrome sprite sheet
monochrome = sprites.TileSheets(sprites.TileSheets.monochrome)
builder = sprites.TileBuilder(monochrome)

# Build the grey tile
grey_tile = builder.build()

# Colors
WHITE = (255, 255, 255)
GREY = (126, 126, 126)

# Define difficulty boxes
beginner_box = pygame.Rect(50, 100, 200, 50)
intermediate_box = pygame.Rect(50, 200, 200, 50)
advanced_box = pygame.Rect(50, 300, 200, 50)

# Initialize the selected difficulty to None
selected_difficulty = None

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if beginner_box.collidepoint(event.pos):
                selected_difficulty = 0
            elif intermediate_box.collidepoint(event.pos):
                selected_difficulty = 1
            elif advanced_box.collidepoint(event.pos):
                selected_difficulty = 2

    if selected_difficulty == 0:
        screen_width = beginner_grid[0] * tile_size
        screen_height = beginner_grid[1] * tile_size
        # blit gameboard
    elif selected_difficulty == 1:
        screen_width = intermediate_grid[0] * tile_size
        screen_height = intermediate_grid[1] * tile_size
        # blit gameboard
    elif selected_difficulty == 1:
        screen_width = advanced_grid[0] * tile_size
        screen_height = advanced_grid[1] * tile_size
        # blit gameboard

    # Draw the difficulty boxes
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREY, beginner_box)
    pygame.draw.rect(screen, GREY, intermediate_box)
    pygame.draw.rect(screen, GREY, advanced_box)

    # Add text labels for difficulty levels
    font = pygame.font.Font(None, 30)
    title_text = font.render("MINESWEEPER", True, (255, 0, 0))
    beginner_text = font.render("Beginner", True, (0, 0, 0))
    intermediate_text = font.render("Intermediate", True, (0, 0, 0))
    advanced_text = font.render("Advanced", True, (0, 0, 0))
    screen.blit(title_text, (75, (115/2)-30))
    screen.blit(beginner_text, (60, 115))
    screen.blit(intermediate_text, (60, 215))
    screen.blit(advanced_text, (60, 315))

    pygame.display.flip()

# Now you can use selected_difficulty to proceed with the chosen difficulty level.

# Quit Pygame
pygame.quit()

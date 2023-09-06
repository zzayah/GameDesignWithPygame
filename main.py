from minesweeper import sprites
import pygame

# Initialize Pygame
pygame.init()

# Set up the display
tile_size = 16  # Size of each tile in pixels
grid_size = 10   # Size of the grid
screen_width = tile_size * grid_size
screen_height = tile_size * grid_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grey Tiles Grid")

# Create a TileBuilder with the monochrome sprite sheet
monochrome = sprites.TileSheets(sprites.TileSheets.monochrome)
builder = sprites.TileBuilder(monochrome)

# Build the grey tile
grey_tile = builder.build()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the grid of grey tiles
    for row in range(grid_size):
        for col in range(grid_size):
            screen.blit(grey_tile.unopened, (col * tile_size, row * tile_size))

    pygame.display.flip()

# Quit Pygame
pygame.quit()

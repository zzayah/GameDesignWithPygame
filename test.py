import pygame

def get_image_from_spritesheet(x, y):
    # Initialize Pygame
    pygame.init()

    # Load the spritesheet image
    spritesheet = pygame.image.load('2000.png')

    # Define the dimensions of individual images and the number of rows and columns
    image_width = 16
    image_height = 16
    columns = 8
    rows = 2

    # Calculate the coordinates of the top-left corner of the desired image
    x_pos = x * image_width
    y_pos = y * image_height

    # Create a surface and copy the desired image onto it
    image_surface = pygame.Surface((image_width, image_height))
    image_surface.blit(spritesheet, (0, 0), (x_pos, y_pos, image_width, image_height))

    # Return the extracted image as a surface
    return image_surface

x_coord = 3  # X-coordinate of the desired image
y_coord = 1  # Y-coordinate of the desired image

image_surface = get_image_from_spritesheet(x_coord, y_coord)
import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
trans_surf = DISPLAYSURF.convert_alpha()
pygame.display.set_caption('Hello World!')

# set up the colors

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 0, 255)

DISPLAYSURF.fill(BLUE)

# Draw circles and ellipse
pygame.draw.circle(DISPLAYSURF, WHITE, (150, 100), 20)
pygame.draw.circle(DISPLAYSURF, WHITE, (250, 100), 20)
pygame.draw.ellipse(DISPLAYSURF, WHITE, (125, 150, 150, 50))

# Create a transparent circle surface
transparent_circle_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(transparent_circle_surf, (255, 255, 255, 128), (20, 20), 20)

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()


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
fpsClock = pygame.time.Clock()

FPS = 30 # frames per second setting

# Draw circles and ellipse
# pygame.draw.circle(DISPLAYSURF, WHITE, (150, 100), 20)
# pygame.draw.circle(DISPLAYSURF, WHITE, (250, 100), 20)


# Draw a transparent circle
transparent_circle_surf = pygame.Surface((400, 300), pygame.SRCALPHA)
pygame.draw.circle(transparent_circle_surf, (255, 255, 255, 128), (150, 100), 20)
pygame.draw.circle(transparent_circle_surf, (255, 255, 255, 128), (250, 100), 20)

DISPLAYSURF.blit(transparent_circle_surf, (0, 0))

play = True

ellipseRad = 100
ellipse = pygame.draw.ellipse(DISPLAYSURF, WHITE, (125, 150, 150, ellipseRad))
direction = 'up'

while True: # main game loop
    for event in pygame.event.get():

        # Play sound once upon boot
        while play:
            soundObj = pygame.mixer.Sound('beep-02.mp3')
            soundObj.play()
            import time
            time.sleep(1)  # wait and let the sound play for 1 second
            soundObj.stop()
            play = False

        if direction == 'up':
            ellipseRad += 5
            if ellipseRad == 300:
                direction = "down"
        elif direction == 'down':
            ellipseRad -= 5
            if ellipseRad == 50:
                direction = "up"

        DISPLAYSURF.blit(ellipse, (0, 0))

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

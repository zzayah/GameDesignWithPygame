import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
CHANGESURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CHANGESURF.fill(BLUE)
fpsClock = pygame.time.Clock()

FPS = 30 # frames per second setting

eyebrow_surf = pygame.display.set_mode((400, 300))
pygame.draw.rect(eyebrow_surf, RED, (0, 0, 50, 30))

# Draw a transparent circle
transparent_circle_surf = pygame.Surface((400, 300), pygame.SRCALPHA)
pygame.draw.circle(transparent_circle_surf, (255, 255, 255, 128), (150, 100), 20)
pygame.draw.circle(transparent_circle_surf, (255, 255, 255, 128), (250, 100), 20)

CHANGESURF.blit(transparent_circle_surf, (0, 0))
CHANGESURF.blit(eyebrow_surf, (0, 0))


play = True
ellipseRad = 100
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
            if ellipseRad == 200:
                direction = "down"
        elif direction == 'down':
            ellipseRad -= 5
            if ellipseRad == 10:
                direction = "up"

        # Create a surface to draw the ellipse
        ellipse_surf = pygame.Surface((400, 300), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surf, WHITE, (125, 150, 150, ellipseRad))

        CHANGESURF.fill(BLUE)  # Clear the display
        CHANGESURF.blit(eyebrow_surf, (0, 0))
        CHANGESURF.blit(transparent_circle_surf, (0, 0)) # Blit the circles
        CHANGESURF.blit(ellipse_surf, (0, 0))  # Blit the ellipse

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)

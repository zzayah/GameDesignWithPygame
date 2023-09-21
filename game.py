import pygame


def load_sprite(self, pic_number):
    image_start_x, image_start_y, image_end_x, image_end_y = 0, 0, 0, 16
    image = pygame.image.load("2000.png")

    if pic_number <= 7:
        image_start_x = pic_number * 16
        image_end_x = pic_number * 16 + 16
    elif 8 < pic_number <= 15:
        image_start_x = (pic_number - 9) * 16
        image_end_x = (pic_number - 9) * 16 + 16
        image_start_y = 16
        image_end_y = 32
    else:
        print(f"invalid input to load_sprite: {pic_number}")

    sprite = image.subsurface(pygame.Rect(image_start_x, image_start_y, image_end_x, image_end_y))

    return sprite

class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(self.screenSize)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        topLeft = (0, 0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize(0[1])):
                self.screen.blit(load_sprite(0), topLeft)





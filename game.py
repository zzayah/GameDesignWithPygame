import pygame


def load_sprite(pic_number):
    image_start_x, image_start_y, image_end_x, image_end_y = 0, 0, 16, 16  # Default values for the first case
    image = pygame.image.load("2000.png")
    image_width, image_height = image.get_width(), image.get_height()

    if pic_number <= 7:
        image_start_x = pic_number * 16
        image_end_x = pic_number * 16 + 16
    elif 8 <= pic_number <= 15:
        image_start_x = (pic_number - 8) * 16
        image_end_x = ((pic_number - 8) * 16) + 16
        image_start_y = 16
        image_end_y = 32
    else:
        print(f"invalid input to load_sprite: {pic_number}")

    # Ensure the coordinates are within the bounds of the image
    # image_start_x = min(max(image_start_x, 0), image_width)
    # image_start_y = min(max(image_start_y, 0), image_height)
    # image_end_x = min(max(image_end_x, 0), image_width)
    # image_end_y = min(max(image_end_y, 0), image_height)

    sprite = image.subsurface(pygame.Rect(image_start_x, image_start_y, image_end_x - image_start_x, image_end_y - image_start_y))

    return sprite


class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = 16
    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
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
            for col in range(self.board.getSize()[1]):
                self.screen.blit(load_sprite(10), topLeft)
                topLeft = topLeft[0] + self.pieceSize, topLeft[1]
            topLeft = 0, topLeft [1] + self.pieceSize





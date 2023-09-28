import pygame
from time import sleep

def load_sprite(pic_number):
    # Define the dimensions of each sprite in the grid
    sprite_width, sprite_height = 16, 16

    # Load the image
    image = pygame.image.load("2000.png")
    image_width, image_height = image.get_width(), image.get_height()

    # Calculate the number of columns in the image grid
    num_columns = image_width // sprite_width

    # Calculate the row and column of the sprite based on pic_number
    row = pic_number // num_columns
    col = pic_number % num_columns

    # Calculate the coordinates of the sprite
    image_start_x = col * sprite_width
    image_start_y = row * sprite_height
    image_end_x = image_start_x + sprite_width
    image_end_y = image_start_y + sprite_height

    # Ensure the coordinates are within the bounds of the image
    image_start_x = min(max(image_start_x, 0), image_width)
    image_start_y = min(max(image_start_y, 0), image_height)
    image_end_x = min(max(image_end_x, 0), image_width)
    image_end_y = min(max(image_end_y, 0), image_height)

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
        pygame.display.set_caption("Minesweeper")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                # if event.type == pygame.MOUSE
                    self.handleClick(position, rightClick)
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                sound = pygame.mixer.Sound("win.wav")
                sound.play()
                sleep(4)
            elif self.board.getLost():
                sound = pygame.mixer.Sound("lose.wav")
                sound.play()
                sleep(4)

        pygame.quit()

    def draw(self):
        topLeft = (0, 0)
        # GREY_LIGHT = (192, 192, 192)
        # GREY_DARK = (128, 128, 128)
        # grey_surf = pygame.Surface(self.screenSize)
        # grey_surf.fill(GREY_DARK)
        # self.screen.blit(grey_surf, (0, 0))
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize, topLeft[1]
            topLeft = 0, topLeft[1] + self.pieceSize

    def getImage(self, piece):

        if piece.getFlagged() and not piece.getClicked():
            return load_sprite(2)
        
        if piece.getClicked():
            if piece.getHasBomb():
                return load_sprite(6)
            elif piece.getNumAround() == 0:
                return load_sprite(1)
            elif piece.getNumAround() > 0:
                return load_sprite(piece.getNumAround()+7)
            
        return load_sprite(0)
        
    def handleClick(self, position, rightClick):
        if self.board.lost:
            return
        index = position[1] // self.pieceSize, position[0] // self.pieceSize
        piece = self.board.getPiece(index)
        self.board.handleClick(piece, rightClick)
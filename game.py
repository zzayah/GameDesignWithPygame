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
        self.sound_played = False  # Track if sound has been played
        self.smileRect = pygame.Rect((self.screenSize[0] // 2) - 16, 10, 32, 32)
        self.gameEnabled = True

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("Minesweeper")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if self.gameEnabled:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        position = pygame.mouse.get_pos()
                        rightClick = pygame.mouse.get_pressed()[2]
                        self.handleClick(position, rightClick)
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        position = pygame.mouse.get_pos()
                        self.handleClickGameDisabled(position)
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        topLeft = (50, 50)
        GREY_LIGHT = (192, 192, 192)
        GREY_DARK = (128, 128, 128)
        grey_surf = pygame.Surface(self.screenSize)
        grey_surf.fill(GREY_DARK)
        self.screen.blit(grey_surf, (0, 0))

        if not (self.board.lost and self.board.won):
            smile_status = "smile"
        elif not self.board.won or self.board.lost:
            smile_status = "dead_face"

        pygame.draw.rect(self.screen, GREY_LIGHT, self.smileRect, 1)

        smile = pygame.image.load(f"{smile_status}.png")
        smile = pygame.transform.scale(smile, (32, 32))
        self.screen.blit(smile, ((self.screenSize[0] // 2) - 16, 10))

        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize, topLeft[1]
            topLeft = 50, topLeft[1] + self.pieceSize

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
        index = (position[1] - 50) // self.pieceSize, (position[0] - 50) // self.pieceSize
        print(position[1])
        print(position[0])
        print(index)
    
        if index[0] < 0 or index[0] >= self.board.getSize()[0] or index[1] < 0 or index[1] >= self.board.getSize()[1]:
            return
        else:
            piece = self.board.getPiece(index)
            self.board.handleClick(piece, rightClick)

    def handleClickGameDisabled(self, position):
        if self.smileRect.collidepoint(position):
            self.board.handleClickGameDisabled(position)
            # reset all instances of game class
            self.sound_played = False
            self.gameEnabled = True


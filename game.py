import pygame
import threading
import time
import math


def load_sprite(pic_number, imgName):
    """
    Load and extract a sprite from an image file based on pic_number and imgName.

    Args:
        pic_number (int): The index of the sprite to extract.
        imgName (str): The name of the image file.

    Returns:
        pygame.Surface: The extracted sprite.
    """
    # Define the dimensions of each sprite in the grid
    if imgName == "2000":
        sprite_width, sprite_height = 16, 16
    elif imgName == "2000clock":
        sprite_width, sprite_height = 13, 23

    # Load the image
    image = pygame.image.load(f"{imgName}.png")
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

    sprite = image.subsurface(
        pygame.Rect(image_start_x, image_start_y, image_end_x - image_start_x, image_end_y - image_start_y))

    return sprite


class Game():
    def __init__(self, board, screenSize):
        """
        Initialize the Minesweeper game.

        Args:
            board (Board): The game board.
            screenSize (tuple): The size of the game window.
        """
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = 16
        self.sound_played = False
        self.smile_rect = pygame.Rect((self.screenSize[0] // 2) - 16, 10, 32, 32)
        self.gameEnabled = True
        self.smile_status = "smile"
        self.clock = (0, 0, 0)
        self.clock_update_time = 1000  # Update the clock every 1000 milliseconds (1 second)
        self.last_clock_update = pygame.time.get_ticks()
        self.firstClick = True
        self.numBombsRemaining = 0
        self.won = False

    def run(self):
        """
        Run the Minesweeper game loop.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("Minesweeper")
        running = True
        first_click = True  # Add a flag to track the first click

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)

                    self.numBombsRemaining = self.board.numBombs - self.board.numFlags
                    actualBombsRemaining = self.board.numBombs - self.board.correctFlags
                    if actualBombsRemaining == 0 and self.board.numFlags == self.board.numBombs:
                        self.won = True

            self.draw()
            pygame.display.flip()
        pygame.quit()

    def updateClock(self):
        """
        Update the in-game clock.
        """
        now = pygame.time.get_ticks()
        if now - self.last_clock_update >= 1000:  # Update only once every second
            self.clock = (self.clock[0], self.clock[1], self.clock[2] + 1)

            if self.clock[2] == 10:
                self.clock = (self.clock[0], self.clock[1] + 1, 0)

            if self.clock[1] == 10:
                self.clock = (self.clock[0] + 1, 0, self.clock[2])

            if self.clock[0] == 10:
                self.clock = (0, self.clock[1], self.clock[2])

            self.last_clock_update = now

    def draw(self):
        """
        Draw the game interface.
        """

        topLeft = (50, 50)
        GREY_LIGHT = (192, 192, 192)
        GREY_DARK = (128, 128, 128)
        grey_surf = pygame.Surface(self.screenSize)
        grey_surf.fill(GREY_DARK)
        self.screen.blit(grey_surf, (0, 0))

        if self.won:
            self.smile_status = "cool_face"
        elif not (self.board.lost):
            self.smile_status = "smile"
        else:
            self.smile_status = "dead_face"

        smile = pygame.image.load(f"{self.smile_status}.png")
        smile = pygame.transform.scale(smile, (32, 32))
        self.screen.blit(smile, ((self.screenSize[0] // 2) - 16, 10))
        pygame.draw.rect(self.screen, GREY_LIGHT, self.smile_rect, 1)

        # Corrected the updateClock placement - only update once per frame

        if not self.firstClick and not self.won and not self.board.lost:
            self.updateClock()
            self.firstClick = False

        if not self.firstClick:
            third = load_sprite(self.clock[2], "2000clock")
            second = load_sprite(self.clock[1], "2000clock")
            first = load_sprite(self.clock[0], "2000clock")

            self.screen.blit(third, (self.screenSize[0] // 2 + 50, 10))
            self.screen.blit(second, (self.screenSize[0] // 2 + 37, 10))
            self.screen.blit(first, (self.screenSize[0] // 2 + 24, 10))
        else:
            zero = load_sprite(0, "2000clock")
            self.screen.blit(zero, (self.screenSize[0] // 2 + 50, 10))
            self.screen.blit(zero, (self.screenSize[0] // 2 + 37, 10))
            self.screen.blit(zero, (self.screenSize[0] // 2 + 24, 10))

        # mine counter
        if not self.won:
            num_mines_str = str(self.numBombsRemaining)
            num_mines_tuple = tuple(map(int, num_mines_str))
            if len(num_mines_tuple) == 3:
                if self.firstClick:
                    zero = load_sprite(0, "2000clock")
                    self.screen.blit(zero, (self.screenSize[0] // 2 - 66, 10))
                    self.screen.blit(zero, (self.screenSize[0] // 2 - 53, 10))
                    self.screen.blit(zero, (self.screenSize[0] // 2 - 40, 10))
                else:
                    first = load_sprite(num_mines_tuple[0], "2000clock")
                    second = load_sprite(num_mines_tuple[1], "2000clock")
                    third = load_sprite(num_mines_tuple[2], "2000clock")
                    self.screen.blit(first, (self.screenSize[0] // 2 - 66, 10))
                    self.screen.blit(second, (self.screenSize[0] // 2 - 53, 10))
                    self.screen.blit(third, (self.screenSize[0] // 2 - 40, 10))
            elif len(num_mines_tuple) == 2:
                if self.firstClick:
                    zero = load_sprite(0, "2000clock")
                    self.screen.blit(zero, (self.screenSize[0] // 2 - 53, 10))
                    self.screen.blit(zero, (self.screenSize[0] // 2 - 40, 10))
                else:
                    first = load_sprite(num_mines_tuple[0], "2000clock")
                    second = load_sprite(num_mines_tuple[1], "2000clock")
                    self.screen.blit(first, (self.screenSize[0] // 2 - 53, 10))
                    self.screen.blit(second, (self.screenSize[0] // 2 - 40, 10))
            elif len(num_mines_tuple) == 1:
                if self.firstClick:
                    zero = load_sprite(0, "2000clock")
                    self.screen.blit(zero, (self.screenSize[0] // 2 - 53, 10))
                    self.screen.blit(zero, (self.screenSize[0] // 2 - 40, 10))
                else:
                    first = load_sprite(0, "2000clock")
                    second = load_sprite(num_mines_tuple[0], "2000clock")
                    self.screen.blit(first, (self.screenSize[0] // 2 - 53, 10))
                    self.screen.blit(second, (self.screenSize[0] // 2 - 40, 10))
        else:
            zero = load_sprite(0, "2000clock")
            self.screen.blit(zero, (self.screenSize[0] // 2 - 53, 10))
            self.screen.blit(zero, (self.screenSize[0] // 2 - 40, 10))

        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize, topLeft[1]
            topLeft = 50, topLeft[1] + self.pieceSize

    def getImage(self, piece):
        """
        Get the image for a game piece.

        Args:
            piece (Piece): The game piece.

        Returns:
            pygame.Surface: The image of the game piece.
        """

        # blits flag if right click
        if piece.getFlagged() and not piece.getClicked() and not self.board.lost:
            return load_sprite(2, "2000")

        # blits piece is clicked and has bomb print the red bomb
        if piece.getHasBomb() and piece.getClicked():
            return load_sprite(6, "2000")

        # if lost, has bomb, has a flag, and not clicked, blits flag
        if self.board.lost and piece.getHasBomb() and piece.getFlagged() and not piece.getClicked():
            return load_sprite(2, "2000")
        elif self.board.lost and piece.getHasBomb() and piece.getFlagged():
            return load_sprite(7, "2000")
        elif self.board.lost and piece.getHasBomb():
            return load_sprite(5, "2000")

        if piece.getClicked():
            if piece.getNumAround() == 0:
                return load_sprite(1, "2000")
            elif piece.getNumAround() > 0:
                return load_sprite(piece.getNumAround() + 7, "2000")

        return load_sprite(0, "2000")

    def handleClick(self, position, rightClick):
        """
        Handle mouse clicks on the game board.

        Args:
            position (tuple): The position of the mouse click.
            rightClick (bool): True if it's a right-click, False otherwise.
        """

        index = ((position[1] - 50) // self.pieceSize, (position[0] - 50) // self.pieceSize)

        if self.firstClick and not self.smile_rect.collidepoint(position):

            # Generate a new random board until the first clicked cell and its neighbors are safe
            while True:
                self.board.resetBoard()
                piece = self.board.getPiece(index)

                # Check if the first clicked cell and its neighbors are safe
                if not piece.getHasBomb() and all(
                    not neighbor.getHasBomb() for neighbor in self.board.getListOfNeighbors(index)
                ):
                    break

            pygame.time.set_timer(pygame.USEREVENT, self.clock_update_time)  # Set up a custom event for clock updates

            self.board.handleClick(piece, rightClick, index)

            self.firstClick = False
            self.board.lost = False
            self.board.won = False
            self.board.numClicked = 0
            self.sound_played = False
            self.gameEnabled = True
            self.clock = (0, 0, 0)
            return

        if self.board.lost and self.smile_rect.collidepoint(position):
            pygame.time.set_timer(pygame.USEREVENT, self.clock_update_time)  # Set up a custom event for clock updates

            self.won = False

            self.board.handleClickGameDisabled()
            self.board.lost = False
            self.sound_played = False
            self.gameEnabled = True

            self.firstClick = True

            self.clock = (0, 0, 0)
            return
        elif self.board.lost:
            return

        if self.smile_rect.collidepoint(position):
            self.won = False
            self.board.handleClickGameDisabled()
            self.board.lost = False
            self.sound_played = False
            self.gameEnabled = True

            self.firstClick = True

            self.clock = (0, 0, 0)
        elif index[0] < 0 or index[0] >= self.board.getSize()[0] or index[1] < 0 or index[1] >= self.board.getSize()[1]:
            return
        else:
            piece = self.board.getPiece(index)
            self.board.handleClick(piece, rightClick, index)
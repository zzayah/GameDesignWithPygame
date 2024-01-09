import pygame as pg

class Main:
    def __init__(self, board_size):
        self.filename = "snake_sprites.png"
        size_mapping = {
            "small": (1, 1),
            "medium": (17, 17),
            "large": (25, 25)
        }
        self.board_size = size_mapping.get(board_size, (0, 0))

        if self.board_size == (0, 0):
            print("input error: board_size not recognized")
            pg.quit()
        
        # init green_board
        for i in range(0, self.board_size[0]):
            for j in range(0, self.board_size[1]):
                break

        self.screen = pg.display.set_mode((self.board_size[0]*64)+40, (self.board_size[1]*64)+40)

    def set_board(self):
        # fill screen with green3
        self.screen.fill((87, 138, 52))

        # blit 
        for i in range(0, 17):
            for j in range(0, 17):
                break
    
    def run(self):
        pg.init()
        running = True
        while running:
            for event in pg.event.get():
                if event.type() == pg.QUIT:
                    running = False
        pg.quit()

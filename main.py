import pygame as pg

class Main:
    def __init__(self, board_size):
        # board_size must be a tuple, representing the width (x) then height (y) of the board
        self.filename = "snake_sprites.png"

        # green2 and green1 init
        self.green2 = pg.image.load("green2.png")
        self.green1 = pg.image.load("green1.png")

        self.board_size = (board_size)

        if not (10 < self.board_size[0] < 26):
            print("invalid board_size input")
            pg.quit()

        self.screen = pg.display.set_mode((((self.board_size[0]*64)+40), ((self.board_size[1]*64)+40)))

    def do_periodic(self):
        # blit tiles
        counter = 0
        for i in range(0, self.board_size[1]):
            for j in range(0, self.board_size[0]):
                if not (self.board_size[0] % 2 == 0 or self.baord_size[1] % 2 == 0):
                    if not (counter % 2 != 0):
                        self.screen.blit(self.green2, ((j*64)+20, (i*64)+20))
                    else:
                        self.screen.blit(self.green1, ((j*64)+20, (i*64)+20))
                else:
                    if counter % 2 != 0:
                        self.screen.blit(self.green2, ((j*64)+20, (i*64)+20))
                    else:
                        self.screen.blit(self.green1, ((j*64)+20, (i*64)+20))
                counter += 1
    
    def run(self):
        pg.init()
        pg.display.set_caption("Snake")
        self.screen.fill((87, 138, 52))
        running = True
        while running:
            for event in pg.event.get():
                if event == pg.QUIT:
                    running = False
            self.do_periodic()
            pg.display.flip()
        pg.quit()

main = Main((14, 14))
main.run()

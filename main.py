import pygame as pg

class Main:
    def __init__(self, board_size):
        # board_size must be a tuple, representing the width (x) then height (y) of the board
        self.filename = "snake_sprites.png"

        self.snake_pos = [[0 for _ in range(board_size)] for _ in range(board_size)]

        self.snake_pos[int(board_size/2)][1] = 1
        self.snake_pos[int(board_size/2)][2] = 300
        self.snake_pos[int(board_size/2)][3] = 10

        # green2 and green1 init
        self.green2 = pg.image.load("green2.png")
        self.green1 = pg.image.load("green1.png")

        # snake sprites init
        self.snake_sprites = pg.image.load("snake_sprites.png")

        self.snake_sprite_pos = {
            # all in (x, y)

            # tail_east
            1: (256, 128, 64, 64),
            # tail_north
            2: (192, 128, 64, 64),
            # tail_west
            3: (192, 192, 64, 64),
            # tail_south
            4: (256, 192, 64, 64),
            # head_east
            10: (256, 0, 64, 64),
            # head_north
            20: (192, 0, 64, 64),
            # head_west
            30: (192, 64, 64, 64),
            # head_south
            40: (256, 64, 64, 64),
            # body_east_west
            300: (64, 0, 64, 64)
        }

        self.board_size = (board_size, board_size)

        if not (10 < self.board_size[0] < 26):
            print("invalid board_size input")
            pg.quit()

        self.screen = pg.display.set_mode((((self.board_size[0]*64)+40), ((self.board_size[1]*64)+40)))

    def do_periodic(self):
        # Blit tiles in checkerboard pattern
        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                if (i + j) % 2 == 0:
                    self.screen.blit(self.green2, ((j*64)+20, (i*64)+20))
                else:
                    self.screen.blit(self.green1, ((j*64)+20, (i*64)+20))
        
        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                if self.snake_pos[i][j] != 0:
                    snake_rect = pg.Rect(self.snake_sprite_pos[self.snake_pos[i][j]])
                    snake_piece = self.snake_sprites.subsurface(snake_rect)
                    snake_piece.set_colorkey((255, 255, 255))
                    self.screen.blit(snake_piece, ((j * 64 + 20), (i * 64 + 20)))

    
    def run(self):
        pg.init()
        pg.display.set_caption("Snake")
        self.screen.fill((87, 138, 52))
        running = True
        while running:
            for event in pg.event.get():
                if event == pg.QUIT or event == pg.K_ESCAPE:
                    running = False
            self.do_periodic()
            pg.display.flip()
        pg.quit()

main = Main((13))
main.run()

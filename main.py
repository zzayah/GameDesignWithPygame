import pygame as pg

class Main:
    def __init__(self, board_size):
        # board_size must be a tuple, representing the width (x) then height (y) of the board
        self.filename = "snake_sprites.png"
        self.snake_parts_processed = 0

        self.snake_pos = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.marker_ary = [["" for _ in range(board_size)] for _ in range(board_size)]

        self.snake_pos[int(board_size/2)][1] = ((int(board_size/2), 1), "right")
        self.snake_pos[int(board_size/2)][2] = ((int(board_size/2), 2), "right")
        self.snake_pos[int(board_size/2)][3] = ((int(board_size/2), 3), "right")

        # snake head location
        self.snake_head = ((int(board_size/2), 3), "right")

        # green2 and green1 init
        self.green2 = pg.image.load("green2.png")
        self.green1 = pg.image.load("green1.png")

        # red and blue init
        self.red = pg.image.load("red.png")
        self.blue = pg.image.load("blue.png")
        self.gold = pg.image.load("gold.png")

        # snake sprites init
        # self.snake_sprites = pg.image.load("snake_sprites.png")

        # clock var
        self.old_time = 0
        self.new_time = 0
        
        # lost/win var
        self.lost = False
        self.won = False

        # snake length
        self.snake_length = 3

        # input direction
        self.input_direction = "right"

        # self.snake_sprite_pos = {
        #     # all in (x, y)
        #     # tail_east
        #     1: (256, 128, 64, 64),
        #     # tail_north
        #     2: (192, 128, 64, 64),
        #     # tail_west
        #     3: (192, 192, 64, 64),
        #     # tail_south
        #     4: (256, 192, 64, 64),
        #     # head_east
        #     10: (256, 0, 64, 64),
        #     # head_north
        #     20: (192, 0, 64, 64),
        #     # head_west
        #     30: (192, 64, 64, 64),
        #     # head_south
        #     40: (256, 64, 64, 64),
        #     # body_east_west
        #     300: (64, 0, 64, 64)
        # }

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
                    self.screen.blit(self.red, ((j * 64 + 20), (i * 64 + 20)))

    def handle_input(self, event):

        new_ary = [[0 for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]

        if event:
            for i in range(self.board_size[1]):
                for j in range(self.board_size[0]):
                    if self.snake_pos[i][j] != 0:
                        if self.snake_pos[i][j][1] == "right":
                            if self.marker_ary == "up":
                                self.snake_pos[i][j][1] = "up"
                                new_ary[i][j+1] = self.snake_pos[i][j]
                            elif self.marker_ary == "down":
                                self.snake_pos[i][j][1] = "down"
                                new_ary[i][j-1] = self.snake_pos[i][j]

                        elif self.snake_pos[i][j][1] == "left":
                            new_ary[i][j-1] = self.snake_pos[i][j]
                        elif self.snake_pos[i][j][1] == "up":
                            new_ary[i-1][j] = self.snake_pos[i][j]
                        elif self.snake_pos[i][j][1] == "down":
                            new_ary[i+1][j] = self.snake_pos[i][j]
            self.snake_pos = new_ary
        else:
            for i in range(self.board_size[1]):
                for j in range(self.board_size[0]):
                    if self.snake_pos[i][j] != 0:
                        if self.snake_pos[i][j][1] == "right":
                            new_ary[i][j+1] = self.snake_pos[i][j]
                        elif self.snake_pos[i][j][1] == "left":
                            new_ary[i][j-1] = self.snake_pos[i][j]
                        elif self.snake_pos[i][j][1] == "up":
                            new_ary[i-1][j] = self.snake_pos[i][j]
                        elif self.snake_pos[i][j][1] == "down":
                            new_ary[i+1][j] = self.snake_pos[i][j]
            self.snake_pos = new_ary

    def run(self):
        pg.init()
        pg.display.set_caption("Snake")
        self.screen.fill((87, 138, 52))
        running = True
        while running:
            event_occured = False
            if self.lost == True:
                print('lost')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.input_direction = "up"
                        event_occured = True
                    elif event.key == pg.K_DOWN:
                        self.input_direction = "down"
                        event_occured = True
                    elif event.key == pg.K_LEFT:
                        self.input_direction = "left"
                        event_occured = True
                    elif event.key == pg.K_RIGHT:
                        self.input_direction = "right"
                        event_occured = True

            self.new_time = pg.time.get_ticks()

            if self.new_time - 1000 > self.old_time and event_occured == True:
                if self.input_direction == "up":
                    self.snake_head = ((self.snake_head[0][0] + 1, self.snake_head[0][1]), "up")
                elif self.input_direction == "down":
                    self.snake_head = ((self.snake_head[0][0] - 1, self.snake_head[0][1]), "down")
                elif self.input_direction == "left":
                    self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] - 1), "left")
                elif self.input_direction == "right":
                    self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] + 1), "right")
                self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]] = self.snake_head
                # abstract to function
                self.handle_input(True)
                # restart counter
                self.old_time = self.new_time
            elif self.new_time - 1000 > self.old_time:
                self.handle_input(False)
                self.old_time = self.new_time

            self.do_periodic()
            pg.display.flip()
        pg.quit()

main = Main((13))
main.run()

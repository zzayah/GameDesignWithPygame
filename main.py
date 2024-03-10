import pygame as pg
import random


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
        self.filled = False
        self.lost_message = ""

        # fruit
        self.fruit_location = (int(2*board_size/3), int(board_size/2))

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

        # optimization variables
        self.startup_flip_executed = False
        self.event_occured = False

        self.check_fruit_iter = 0

        self.board_size = (board_size, board_size)

        if not (10 < self.board_size[0] < 26):
            print("invalid board_size input")
            pg.quit()

        self.screen = pg.display.set_mode((((self.board_size[0]*64)+40), ((self.board_size[1]*64)+40)))

    def init_set_board(self): # Solves issue of a blank screen on startup // ran before the main loop
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
        
        self.screen.blit(self.gold, ((self.fruit_location[0] * 64 + 20), (self.fruit_location[1] * 64 + 20)))


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

    
    def handle_input(self):
        new_ary = [[0 for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]

        # Iterate over each cell in the board
        for d in range(self.board_size[1]):
            for r in range(self.board_size[0]):
                # Check if there's a snake part at this position
                if self.snake_pos[r][d] != 0:
                    pos, current_direction = self.snake_pos[r][d]                    
                    new_direction = self.marker_ary[pos[0]][pos[1]]
                    # Update direction based on the marker
                    if new_direction == "left" and current_direction != "right":
                        current_direction = "left"
                    elif new_direction == "right" and current_direction != "left":
                        current_direction = "right"
                    elif new_direction == "up" and current_direction != "down":
                        current_direction = "up"
                    elif new_direction == "down" and current_direction != "up":
                        current_direction = "down"
                        
                    # Update snake position with the new direction
                    match(current_direction):
                        case "left":
                            pos = (pos[0], pos[1] - 1)
                        case "right":
                            pos = (pos[0], pos[1] + 1)
                        case "up":
                            pos = (pos[0] - 1, pos[1])
                        case "down":
                            pos = (pos[0] + 1, pos[1])
                        case _:
                            print("error")
                            break

                    if pos[0] < 0 or pos[0] >= self.board_size[1] or pos[1] < 0 or pos[1] >= self.board_size[0]:
                        self.lost_message = "You hit the wall!"
                        self.lost = True
                        return  # Exit the method to avoid further processing

                    new_ary[pos[0]][pos[1]] = (pos, current_direction)

        self.snake_pos = new_ary

    def check_fruit(self):
        # Flag to check if the fruit is inside the snake
        fruit_inside_snake = False

        # Iterate over the entire snake_pos array
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                # Check if the current cell is part of the snake
                if self.snake_pos[row][col] != 0:
                    # Check if the fruit is in the same position as this part of the snake
                    if (col, row) == self.fruit_location:
                        fruit_inside_snake = True
                        break  # No need to check further if we've found the fruit inside the snake

            if fruit_inside_snake:
                break

        # If the fruit is inside the snake, relocate it
        if fruit_inside_snake:
            self.place_fruit()  # This will find a new location for the fruit

    def place_fruit(self):
        if self.fruit_location is None:
            while True:
                i = random.randint(3, self.board_size[1] - 4)
                j = random.randint(3, self.board_size[0] - 4)
                if self.snake_pos[i][j] == 0 and self.marker_ary[i][j] == "":
                    self.fruit_location = (i, j)
                    break
        if self.fruit_location is not None:
            self.screen.blit(self.gold, ((self.fruit_location[0] * 64 + 20), (self.fruit_location[1] * 64 + 20)))

    def lost_screen(self):
        if not self.filled:
            tansparent_white = pg.Surface((self.board_size[0]*64+40, self.board_size[1]*64+40), pg.SRCALPHA)
            tansparent_white.fill((255, 255, 255, 128))
            self.screen.blit(tansparent_white, (0, 0))
            self.filled = True
        font = pg.font.Font(None, 80)
        text = font.render(self.lost_message, True, (0, 0, 0))
        #blit the text centered in the screen
        self.screen.blit(text, (self.board_size[0]*32-200, self.board_size[1]*32-50))

    def run(self):
        pg.init()
        pg.display.set_caption("Snake")
        self.screen.fill((87, 138, 52))
        running = True
        self.init_set_board()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            if self.lost == True:
                self.lost_screen()
                pg.display.flip()
            else:
                event_occured = False
                self.check_fruit()

                self.new_time = pg.time.get_ticks()

                self.event_occured = self.new_time - 250 > self.old_time

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == pg.KEYDOWN and not self.event_occured:
                        if event.key == pg.K_UP and self.snake_head[1] != "down":
                            self.input_direction = "up"
                        elif event.key == pg.K_DOWN and self.snake_head[1] != "up":
                            self.input_direction = "down"
                        elif event.key == pg.K_LEFT and self.snake_head[1] != "right":
                            self.input_direction = "left"
                        elif event.key == pg.K_RIGHT and self.snake_head[1] != "left":
                            self.input_direction = "right"

                if self.event_occured and not self.lost and not self.won:
                    # check if lost
                    if self.snake_head[0][0] < 0 or self.snake_head[0][0] >= self.board_size[1] or self.snake_head[0][1] < 0 or self.snake_head[0][1] >= self.board_size[0]:
                        self.lost = True
                        
                    if self.snake_length == self.board_size[0] * self.board_size[1]:
                        # self.won_message = "player 1 wins!"
                        # self.won_message = "player 2 wins!"
                        self.won = True
                    if self.input_direction == "left" and self.snake_head[1] != "right":
                        if self.snake_head[1] == "left" and self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]-1] != 0:
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] - 1), "left")
                        self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]+1] = self.snake_head[1]
                    elif self.input_direction == "right" and self.snake_head[1] != "left":
                        if self.snake_pos[1] == "right" and self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]+1] != 0:
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] + 1), "right")
                        self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]-1] = self.snake_head[1]
                    elif self.input_direction == "up" and self.snake_head[1] != "down":
                        if self.snake_head[1] == "up" and self.snake_pos[self.snake_head[0][0]-1][self.snake_head[0][1]] != 0:
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0] - 1, self.snake_head[0][1]), "up")
                        self.marker_ary[self.snake_head[0][0]+1][self.snake_head[0][1]] = self.snake_head[1]
                    elif self.input_direction == "down" and self.snake_head[1] != "up":
                        try:
                            if (self.snake_head[1] == "down" and self.snake_pos[self.snake_head[0][0]+1][self.snake_head[0][1]] != 0):
                                self.lost = True
                        except IndexError:
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0] + 1, self.snake_head[0][1]), "down")                    
                        self.marker_ary[self.snake_head[0][0]-1][self.snake_head[0][1]] = self.snake_head[1]

                    if self.fruit_location != None and self.snake_head[0] == (self.fruit_location[1], self.fruit_location[0]):
                        match(self.snake_head[1]):
                            case "right":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "right")
                                self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] + 1), "right")
                                self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]-1] = self.snake_head[1]
                            case "left":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "left")
                                self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] - 1), "left")
                                self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]+1] = self.snake_head[1]
                            case "up":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "up")
                                self.snake_head = ((self.snake_head[0][0] - 1, self.snake_head[0][1]), "up")
                                self.marker_ary[self.snake_head[0][0]+1][self.snake_head[0][1]] = self.snake_head[1]
                            case "down":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "down")
                                self.snake_head = ((self.snake_head[0][0] + 1, self.snake_head[0][1]), "down")
                                self.marker_ary[self.snake_head[0][0]-1][self.snake_head[0][1]] = self.snake_head[1]
                        self.snake_length += 1
                        self.fruit_location = None

                    # abstract to function
                    self.handle_input()
                    # restart counter
                    self.old_time = self.new_time

                    self.startup_flip_executed = True
                    # self.debug()
                    self.do_periodic()
                    self.place_fruit()
                    pg.display.flip()

                if not self.startup_flip_executed:
                    pg.display.flip()
            
        pg.quit()

main = Main((13))
main.run()
